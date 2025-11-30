import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from compilador import Compilador


class InterfaceGrafica:
    """Interface Gráfica para o Compilador"""

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("🔧 Compilador de Expressões Matemáticas")
        self.raiz.geometry("1000x700")
        self.raiz.configure(bg="#1e1e2e")

        self.configurar_estilos()
        self.criar_widgets()

    def configurar_estilos(self):
        """Configura os estilos da interface"""
        estilo = ttk.Style()
        estilo.theme_use('clam')

        cor_fundo = "#1e1e2e"
        cor_frente = "#cdd6f4"
        cor_destaque = "#89b4fa"

        estilo.configure('Title.TLabel',
                         background=cor_fundo,
                         foreground=cor_destaque,
                         font=('Helvetica', 16, 'bold'))

        estilo.configure('Section.TLabel',
                         background=cor_fundo,
                         foreground=cor_frente,
                         font=('Helvetica', 10, 'bold'))

    def criar_widgets(self):
        """Cria todos os widgets da interface"""
        frame_principal = tk.Frame(self.raiz, bg="#1e1e2e")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        rotulo_titulo = ttk.Label(frame_principal,
                                  text="🔧 COMPILADOR DE EXPRESSÕES MATEMÁTICAS",
                                  style='Title.TLabel')
        rotulo_titulo.pack(pady=(0, 20))

        frame_entrada = tk.Frame(frame_principal, bg="#313244", relief=tk.RIDGE, bd=2)
        frame_entrada.pack(fill=tk.X, pady=(0, 10))

        rotulo_entrada = ttk.Label(frame_entrada,
                                   text="📝 Digite a expressão:",
                                   style='Section.TLabel')
        rotulo_entrada.pack(anchor=tk.W, padx=10, pady=(10, 5))

        self.campo_expressao = tk.Entry(frame_entrada,
                                        font=('Courier', 14),
                                        bg="#45475a",
                                        fg="#cdd6f4",
                                        insertbackground="#cdd6f4",
                                        relief=tk.FLAT,
                                        bd=5)
        self.campo_expressao.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.campo_expressao.insert(0, "3 + 5 * 2")
        self.campo_expressao.bind('<Return>', lambda e: self.compilar_expressao())

        frame_botoes = tk.Frame(frame_entrada, bg="#313244")
        frame_botoes.pack(pady=(0, 10))

        btn_compilar = tk.Button(frame_botoes,
                                 text="▶ COMPILAR",
                                 command=self.compilar_expressao,
                                 bg="#89b4fa",
                                 fg="#1e1e2e",
                                 font=('Helvetica', 12, 'bold'),
                                 relief=tk.FLAT,
                                 padx=30,
                                 pady=10,
                                 cursor='hand2')
        btn_compilar.pack(side=tk.LEFT, padx=5)

        btn_limpar = tk.Button(frame_botoes,
                               text="🗑 LIMPAR",
                               command=self.limpar_saida,
                               bg="#f38ba8",
                               fg="#1e1e2e",
                               font=('Helvetica', 12, 'bold'),
                               relief=tk.FLAT,
                               padx=30,
                               pady=10,
                               cursor='hand2')
        btn_limpar.pack(side=tk.LEFT, padx=5)

        frame_exemplos = tk.Frame(frame_entrada, bg="#313244")
        frame_exemplos.pack(pady=(0, 10))

        ttk.Label(frame_exemplos,
                  text="📚 Exemplos:",
                  style='Section.TLabel').pack(side=tk.LEFT, padx=5)

        exemplos = ["3 + 5 * 2", "(10 + 5) * 3", "100 / (2 + 3) - 5", "2.5 * 4 + 1.5"]

        for exemplo in exemplos:
            btn = tk.Button(frame_exemplos,
                            text=exemplo,
                            command=lambda e=exemplo: self.definir_exemplo(e),
                            bg="#45475a",
                            fg="#cdd6f4",
                            font=('Courier', 9),
                            relief=tk.FLAT,
                            padx=10,
                            pady=5,
                            cursor='hand2')
            btn.pack(side=tk.LEFT, padx=2)

        self.notebook = ttk.Notebook(frame_principal)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.criar_aba("📊 Resultado", "resultado")
        self.criar_aba("🔤 Tokens", "tokens")
        self.criar_aba("🌳 AST", "ast")
        self.criar_aba("⚙️ TAC", "tac")
        self.criar_aba("⚡ Otimizado", "otimizado")
        self.criar_aba("💾 Assembly", "assembly")

    def criar_aba(self, titulo, nome):
        """Cria uma aba com área de texto"""
        frame = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(frame, text=titulo)

        widget_texto = scrolledtext.ScrolledText(frame,
                                                 font=('Courier', 11),
                                                 bg="#1e1e2e",
                                                 fg="#cdd6f4",
                                                 insertbackground="#cdd6f4",
                                                 relief=tk.FLAT,
                                                 padx=10,
                                                 pady=10)
        widget_texto.pack(fill=tk.BOTH, expand=True)

        setattr(self, f"{nome}_texto", widget_texto)

    def definir_exemplo(self, exemplo):
        """Define um exemplo no campo de entrada"""
        self.campo_expressao.delete(0, tk.END)
        self.campo_expressao.insert(0, exemplo)

    def limpar_saida(self):
        """Limpa todas as áreas de saída"""
        for nome in ['resultado', 'tokens', 'ast', 'tac', 'otimizado', 'assembly']:
            widget_texto = getattr(self, f"{nome}_texto")
            widget_texto.delete(1.0, tk.END)

    def compilar_expressao(self):
        """Compila a expressão e exibe os resultados"""
        expressao = self.campo_expressao.get().strip()

        if not expressao:
            messagebox.showwarning("Aviso", "Por favor, digite uma expressão!")
            return

        try:
            self.limpar_saida()

            compilador = Compilador(expressao)
            resultado = compilador.compilar()

            self.resultado_texto.insert(tk.END, "=" * 50 + "\n")
            self.resultado_texto.insert(tk.END, f"EXPRESSÃO: {expressao}\n")
            self.resultado_texto.insert(tk.END, "=" * 50 + "\n\n")
            self.resultado_texto.insert(tk.END, f"✅ RESULTADO: {resultado}\n\n")
            self.resultado_texto.insert(tk.END, "=" * 50 + "\n")

            self.tokens_texto.insert(tk.END, "ANÁLISE LÉXICA - TOKENS\n")
            self.tokens_texto.insert(tk.END, "=" * 50 + "\n\n")
            for token in compilador.tokens:
                self.tokens_texto.insert(tk.END, f"{token}\n")

            self.ast_texto.insert(tk.END, "ANÁLISE SINTÁTICA - ÁRVORE SINTÁTICA ABSTRATA\n")
            self.ast_texto.insert(tk.END, "=" * 50 + "\n\n")
            self.ast_texto.insert(tk.END, f"{compilador.ast}\n")

            self.tac_texto.insert(tk.END, "CÓDIGO INTERMEDIÁRIO (TAC)\n")
            self.tac_texto.insert(tk.END, "=" * 50 + "\n\n")
            for instr in compilador.instrucoes_tac:
                self.tac_texto.insert(tk.END, f"{instr}\n")

            self.otimizado_texto.insert(tk.END, "CÓDIGO OTIMIZADO\n")
            self.otimizado_texto.insert(tk.END, "=" * 50 + "\n\n")
            for instr in compilador.instrucoes_otimizadas:
                self.otimizado_texto.insert(tk.END, f"{instr}\n")

            self.assembly_texto.insert(tk.END, compilador.assembly)

            self.notebook.select(0)

        except Exception as e:
            messagebox.showerror("Erro de Compilação", str(e))