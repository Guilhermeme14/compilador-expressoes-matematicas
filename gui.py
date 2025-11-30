import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from compilador import Compilador


class InterfaceGrafica:
    """Interface Gráfica Minimalista para o Compilador"""

    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Compilador de Expressões")
        self.raiz.geometry("1100x650")

        # Paleta minimalista
        self.cores = {
            'bg': '#f5f5f7',
            'white': '#ffffff',
            'text': '#1d1d1f',
            'text_light': '#6e6e73',
            'accent': '#007aff',
            'accent_hover': '#0051d5',
            'success': '#34c759',
            'border': '#d2d2d7',
            'shadow': '#00000010'
        }

        self.raiz.configure(bg=self.cores['bg'])
        self.criar_interface()

    def criar_interface(self):
        # Container principal com padding generoso
        principal = tk.Frame(self.raiz, bg=self.cores['bg'])
        principal.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # ========== TÍTULO ==========
        frame_titulo = tk.Frame(principal, bg=self.cores['bg'])
        frame_titulo.pack(fill=tk.X, pady=(0, 30))

        tk.Label(frame_titulo, text="Compilador",
                 font=("SF Pro Display", 32, "bold"),
                 bg=self.cores['bg'],
                 fg=self.cores['text']).pack(anchor=tk.W)

        tk.Label(frame_titulo, text="Analise expressões matemáticas passo a passo",
                 font=("SF Pro Text", 13),
                 bg=self.cores['bg'],
                 fg=self.cores['text_light']).pack(anchor=tk.W)

        # ========== ENTRADA ==========
        card_entrada = tk.Frame(principal, bg=self.cores['white'],
                                highlightbackground=self.cores['border'],
                                highlightthickness=1)
        card_entrada.pack(fill=tk.X, pady=(0, 25))

        interno_entrada = tk.Frame(card_entrada, bg=self.cores['white'])
        interno_entrada.pack(fill=tk.X, padx=25, pady=20)

        # Input
        self.campo_expressao = tk.Entry(interno_entrada,
                                        font=("SF Mono", 18),
                                        bg=self.cores['white'],
                                        fg=self.cores['text'],
                                        insertbackground=self.cores['accent'],
                                        relief=tk.FLAT,
                                        bd=0)
        self.campo_expressao.pack(fill=tk.X, ipady=8)
        self.campo_expressao.insert(0, "3 + 5 * 2")
        self.campo_expressao.bind('<Return>', lambda e: self.compilar_expressao())

        # Linha separadora
        tk.Frame(interno_entrada, height=1,
                 bg=self.cores['border']).pack(fill=tk.X, pady=(8, 15))

        # Botões e exemplos
        controles = tk.Frame(interno_entrada, bg=self.cores['white'])
        controles.pack(fill=tk.X)

        # Botões
        frame_botoes = tk.Frame(controles, bg=self.cores['white'])
        frame_botoes.pack(side=tk.LEFT)

        btn_compilar = tk.Button(frame_botoes, text="Compilar",
                                 command=self.compilar_expressao,
                                 bg=self.cores['accent'],
                                 fg='white',
                                 font=("SF Pro Text", 11, "bold"),
                                 relief=tk.FLAT,
                                 bd=0,
                                 padx=25,
                                 pady=10,
                                 cursor='hand2',
                                 activebackground=self.cores['accent_hover'])
        btn_compilar.pack(side=tk.LEFT, padx=(0, 10))

        btn_limpar = tk.Button(frame_botoes, text="Limpar",
                               command=self.limpar_saida,
                               bg=self.cores['bg'],
                               fg=self.cores['text'],
                               font=("SF Pro Text", 11),
                               relief=tk.FLAT,
                               bd=0,
                               padx=25,
                               pady=10,
                               cursor='hand2')
        btn_limpar.pack(side=tk.LEFT)

        # Exemplos
        exemplos = ["3 + 5 * 2", "(10 + 5) * 3", "100 / (2 + 3) - 5", "2.5 * 4 + 1.5"]

        frame_exemplos = tk.Frame(controles, bg=self.cores['white'])
        frame_exemplos.pack(side=tk.RIGHT)

        tk.Label(frame_exemplos, text="Exemplos:",
                 font=("SF Pro Text", 10),
                 bg=self.cores['white'],
                 fg=self.cores['text_light']).pack(side=tk.LEFT, padx=(0, 10))

        for ex in exemplos:
            btn = tk.Button(frame_exemplos, text=ex,
                            command=lambda e=ex: self.definir_exemplo(e),
                            bg=self.cores['bg'],
                            fg=self.cores['text_light'],
                            font=("SF Mono", 9),
                            relief=tk.FLAT,
                            bd=0,
                            padx=10,
                            pady=5,
                            cursor='hand2')
            btn.pack(side=tk.LEFT, padx=2)

        # ========== SAÍDA COM ABAS ==========
        # Container para centralizar as abas
        container_abas = tk.Frame(principal, bg=self.cores['bg'])
        container_abas.pack(fill=tk.BOTH, expand=True)

        # Frame para centralizar o notebook
        frame_centro = tk.Frame(container_abas, bg=self.cores['bg'])
        frame_centro.place(relx=0.5, rely=0, anchor='n', relwidth=1.0, relheight=1.0)

        # Estilo customizado para abas
        estilo = ttk.Style()
        estilo.theme_use('default')

        estilo.configure('Custom.TNotebook',
                         background=self.cores['bg'],
                         borderwidth=0,
                         tabmargins=[0, 0, 0, 0])

        estilo.configure('Custom.TNotebook.Tab',
                         background=self.cores['white'],
                         foreground=self.cores['text_light'],
                         padding=[20, 12],
                         font=("SF Pro Text", 10),
                         borderwidth=0,
                         anchor='center')

        estilo.map('Custom.TNotebook.Tab',
                   background=[('selected', self.cores['white'])],
                   foreground=[('selected', self.cores['accent'])],
                   font=[('selected', ("SF Pro Text", 10, "bold"))])

        estilo.layout('Custom.TNotebook.Tab', [
            ('Notebook.tab', {
                'sticky': 'nswe',
                'children': [
                    ('Notebook.padding', {
                        'side': 'top',
                        'sticky': 'nswe',
                        'children': [
                            ('Notebook.label', {'side': 'top', 'sticky': ''})
                        ]
                    })
                ]
            })
        ])

        self.notebook = ttk.Notebook(frame_centro, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Criar abas
        dados_abas = [
            ("Resultado", "resultado", "success"),
            ("Tokens", "tokens", "accent"),
            ("AST", "ast", "accent"),
            ("TAC", "tac", "accent"),
            ("Otimizado", "otimizado", "accent"),
            ("Assembly", "assembly", "accent")
        ]

        for titulo, nome, chave_cor in dados_abas:
            self.criar_aba_saida(titulo, nome, chave_cor)

    def criar_aba_saida(self, titulo, nome, chave_cor):
        """Cria uma aba de saída"""
        container = tk.Frame(self.notebook, bg=self.cores['white'])
        self.notebook.add(container, text=titulo)

        # Frame com borda
        frame_conteudo = tk.Frame(container,
                                  bg=self.cores['white'],
                                  highlightbackground=self.cores['border'],
                                  highlightthickness=1)
        frame_conteudo.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Área de texto
        widget_texto = scrolledtext.ScrolledText(
            frame_conteudo,
            font=("SF Mono", 11),
            bg=self.cores['white'],
            fg=self.cores['text'],
            insertbackground=self.cores['accent'],
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=20,
            wrap=tk.WORD,
            selectbackground=self.cores['accent'],
            selectforeground='white'
        )
        widget_texto.pack(fill=tk.BOTH, expand=True)

        setattr(self, f"{nome}_texto", widget_texto)

    def definir_exemplo(self, exemplo):
        """Define um exemplo no campo de entrada"""
        self.campo_expressao.delete(0, tk.END)
        self.campo_expressao.insert(0, exemplo)

    def limpar_saida(self):
        """Limpa todas as áreas de saída"""
        for nome in ['resultado', 'tokens', 'ast', 'tac', 'otimizado', 'assembly']:
            getattr(self, f"{nome}_texto").delete(1.0, tk.END)

    def compilar_expressao(self):
        """Compila a expressão e exibe os resultados"""
        expressao = self.campo_expressao.get().strip()

        if not expressao:
            messagebox.showinfo("Informação", "Digite uma expressão para compilar.")
            return

        try:
            self.limpar_saida()
            compilador = Compilador(expressao)
            resultado = compilador.compilar()

            # Resultado
            self.resultado_texto.tag_configure("title", font=("SF Pro Text", 12, "bold"),
                                               foreground=self.cores['text_light'])
            self.resultado_texto.tag_configure("value", font=("SF Pro Display", 36, "bold"),
                                               foreground=self.cores['success'],
                                               spacing1=10, spacing3=15)

            self.resultado_texto.insert(tk.END, "Expressão\n", "title")
            self.resultado_texto.insert(tk.END, f"{expressao}\n\n\n")
            self.resultado_texto.insert(tk.END, "Resultado\n", "title")
            self.resultado_texto.insert(tk.END, f"{resultado}\n", "value")

            # Tokens
            self.tokens_texto.tag_configure("header", font=("SF Pro Text", 13, "bold"),
                                            spacing3=15)
            self.tokens_texto.tag_configure("item", spacing1=3)

            self.tokens_texto.insert(tk.END, "Lista de Tokens:\n\n", "header")
            for i, token in enumerate(compilador.tokens, 1):
                self.tokens_texto.insert(tk.END, f"{i:2}. {token}\n", "item")

            # AST
            self.ast_texto.tag_configure("header", font=("SF Pro Text", 13, "bold"),
                                         spacing3=15)
            self.ast_texto.tag_configure("content", spacing1=5)

            self.ast_texto.insert(tk.END, "Árvore Sintática Abstrata:\n\n", "header")
            self.ast_texto.insert(tk.END, str(compilador.ast), "content")

            # TAC
            self.tac_texto.tag_configure("header", font=("SF Pro Text", 13, "bold"),
                                         spacing3=15)
            self.tac_texto.tag_configure("item", spacing1=3)

            self.tac_texto.insert(tk.END, "Código Intermediário (Three-Address Code):\n\n", "header")
            for i, instr in enumerate(compilador.instrucoes_tac, 1):
                self.tac_texto.insert(tk.END, f"{i}. {instr}\n", "item")

            # Otimizado
            self.otimizado_texto.tag_configure("header", font=("SF Pro Text", 13, "bold"),
                                               spacing3=15)
            self.otimizado_texto.tag_configure("item", spacing1=3)

            self.otimizado_texto.insert(tk.END, "Código Otimizado (Constant Folding):\n\n", "header")
            for i, instr in enumerate(compilador.instrucoes_otimizadas, 1):
                self.otimizado_texto.insert(tk.END, f"{i}. {instr}\n", "item")

            # Assembly
            self.assembly_texto.tag_configure("line", spacing1=2)

            for line in compilador.assembly.split('\n'):
                self.assembly_texto.insert(tk.END, f"{line}\n", "line")

            # Focar na aba de resultado
            self.notebook.select(0)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao compilar:\n{str(e)}")


def main():
    raiz = tk.Tk()
    app = InterfaceGrafica(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()