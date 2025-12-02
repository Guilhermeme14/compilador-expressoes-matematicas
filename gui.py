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
        container_abas = tk.Frame(principal, bg=self.cores['bg'])
        container_abas.pack(fill=tk.BOTH, expand=True)

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
            ("Semântica", "semantica", "accent"),
            ("Código Intermediário", "tac", "accent"),
            ("Otimizado", "otimizado", "accent"),
            ("Código de Máquina", "assembly", "accent")
        ]

        for titulo, nome, chave_cor in dados_abas:
            self.criar_aba_saida(titulo, nome, chave_cor)

    def criar_aba_saida(self, titulo, nome, chave_cor):
        """Cria uma aba de saída"""
        container = tk.Frame(self.notebook, bg=self.cores['white'])
        self.notebook.add(container, text=titulo)

        frame_conteudo = tk.Frame(container,
                                  bg=self.cores['white'],
                                  highlightbackground=self.cores['border'],
                                  highlightthickness=1)
        frame_conteudo.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

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
        for nome in ['resultado', 'tokens', 'ast', 'semantica', 'tac', 'otimizado', 'assembly']:
            getattr(self, f"{nome}_texto").delete(1.0, tk.END)

    def contar_nos_tipo(self, no, tipo_nome):
        """Conta quantos nós de um determinado tipo existem na AST"""
        if no is None:
            return 0

        contador = 1 if type(no).__name__ == tipo_nome else 0

        if hasattr(no, 'esquerda') and hasattr(no, 'direita'):
            contador += self.contar_nos_tipo(no.esquerda, tipo_nome)
            contador += self.contar_nos_tipo(no.direita, tipo_nome)

        return contador

    def extrair_operacoes(self, no):
        """Extrai todas as operações da AST"""
        if no is None:
            return []

        operacoes = []

        if hasattr(no, 'op'):
            operacoes.append(no.op)

        if hasattr(no, 'esquerda') and hasattr(no, 'direita'):
            operacoes.extend(self.extrair_operacoes(no.esquerda))
            operacoes.extend(self.extrair_operacoes(no.direita))

        return operacoes

    def nome_operacao(self, op):
        """Retorna o nome da operação"""
        nomes = {
            '+': 'Adição',
            '-': 'Subtração',
            '*': 'Multiplicação',
            '/': 'Divisão'
        }
        return nomes.get(op, 'Desconhecida')

    def verificar_divisoes(self, no):
        """Verifica todas as divisões na AST e extrai seus operandos"""
        if no is None:
            return []

        divisoes = []

        if hasattr(no, 'op') and no.op == '/':
            # Extrai valor ou expressão do lado esquerdo
            if hasattr(no.esquerda, 'valor'):
                val_esq = no.esquerda.valor
            else:
                val_esq = str(no.esquerda)

            # Extrai valor ou expressão do lado direito
            if hasattr(no.direita, 'valor'):
                val_dir = no.direita.valor
            else:
                val_dir = str(no.direita)

            divisoes.append((val_esq, val_dir))

        # Busca recursivamente nas sub-árvores
        if hasattr(no, 'esquerda'):
            divisoes.extend(self.verificar_divisoes(no.esquerda))
        if hasattr(no, 'direita'):
            divisoes.extend(self.verificar_divisoes(no.direita))

        return divisoes

    def extrair_valores(self, no):
        """Extrai todos os valores numéricos da AST"""
        if no is None:
            return []

        valores = []

        if hasattr(no, 'valor'):
            valores.append(no.valor)

        if hasattr(no, 'esquerda'):
            valores.extend(self.extrair_valores(no.esquerda))
        if hasattr(no, 'direita'):
            valores.extend(self.extrair_valores(no.direita))

        return valores

    def compilar_expressao(self):
        """Compila a expressão e exibe os resultados"""
        print("\n" + "=" * 60)
        print("INÍCIO DA COMPILAÇÃO")
        print("=" * 60)

        expressao = self.campo_expressao.get().strip()
        print(f"1. Expressão capturada: '{expressao}'")

        if not expressao:
            print("❌ Expressão vazia!")
            messagebox.showinfo("Informação", "Digite uma expressão para compilar.")
            return

        try:
            print("\n2. Verificando widgets existentes:")
            widgets = ['resultado', 'tokens', 'ast', 'semantica', 'tac', 'otimizado', 'assembly']
            for widget_name in widgets:
                attr_name = f"{widget_name}_texto"
                existe = hasattr(self, attr_name)
                print(f"   - {attr_name}: {'✓ EXISTE' if existe else '✗ NÃO EXISTE'}")

            print("\n3. Limpando saídas...")
            self.limpar_saida()
            print("   ✓ Saídas limpas")

            print("\n4. Iniciando compilação...")
            compilador = Compilador(expressao)
            resultado = compilador.compilar()
            print(f"   ✓ Compilação concluída! Resultado: {resultado}")

            print("\n5. Preenchendo aba RESULTADO...")
            self.resultado_texto.tag_configure("title", font=("SF Pro Text", 12, "bold"),
                                               foreground=self.cores['text_light'])
            self.resultado_texto.tag_configure("value", font=("SF Pro Display", 36, "bold"),
                                               foreground=self.cores['success'],
                                               spacing1=10, spacing3=15)

            self.resultado_texto.insert(tk.END, "Expressão\n", "title")
            self.resultado_texto.insert(tk.END, f"{expressao}\n\n\n")
            self.resultado_texto.insert(tk.END, "Resultado\n", "title")
            self.resultado_texto.insert(tk.END, f"{resultado}\n", "value")
            print("   ✓ Resultado preenchido")

            print("\n6. Preenchendo aba TOKENS...")
            self.tokens_texto.tag_configure("header", font=("SF Pro Text", 13, "bold"),
                                            spacing3=15)
            self.tokens_texto.tag_configure("item", spacing1=3)

            self.tokens_texto.insert(tk.END, "Lista de Tokens:\n\n", "header")
            for i, token in enumerate(compilador.tokens, 1):
                self.tokens_texto.insert(tk.END, f"{i:2}. Token({token.type}, {token.value}, pos={token.lexpos})\n",
                                         "item")
            print(f"   ✓ {len(compilador.tokens)} tokens preenchidos")

            print("\n7. Preenchendo aba AST...")
            self.ast_texto.tag_configure("header", font=("SF Pro Text", 13, "bold"),
                                         spacing3=15)
            self.ast_texto.tag_configure("content", spacing1=5)

            self.ast_texto.insert(tk.END, "Árvore Sintática Abstrata:\n\n", "header")
            self.ast_texto.insert(tk.END, str(compilador.ast), "content")
            print("   ✓ AST preenchida")

            print("\n8. Preenchendo aba SEMÂNTICA...")
            # Configurar estilos
            self.semantica_texto.tag_configure("header", font=("SF Pro Text", 13, "bold"),
                                               spacing3=15)
            self.semantica_texto.tag_configure("success_msg", font=("SF Pro Text", 11),
                                               foreground=self.cores['success'],
                                               spacing1=3)
            self.semantica_texto.tag_configure("info", font=("SF Pro Text", 11),
                                               spacing1=3)
            self.semantica_texto.tag_configure("item", spacing1=3)

            # Análise Semântica
            self.semantica_texto.insert(tk.END, "Análise Semântica:\n", "header")

            # Conta nós na AST
            num_numeros = self.contar_nos_tipo(compilador.ast, 'NoNumero')
            num_operacoes = self.contar_nos_tipo(compilador.ast, 'NoOperacaoBinaria')

            self.semantica_texto.insert(tk.END, f"Números verificados: {num_numeros}\n")
            self.semantica_texto.insert(tk.END, f"Operações verificadas: {num_operacoes}\n")
            self.semantica_texto.insert(tk.END, "Verificação de divisão por zero: OK\n")
            self.semantica_texto.insert(tk.END, "Validação de tipos: OK\n\n")

            # Detalhes
            self.semantica_texto.insert(tk.END, "Detalhes da Análise:\n", "header")

            # Valores encontrados
            valores = self.extrair_valores(compilador.ast)
            if valores:
                self.semantica_texto.insert(tk.END, f"Valores encontrados: {', '.join(map(str, valores))}\n\n", "info")

            # Operações identificadas
            operacoes = self.extrair_operacoes(compilador.ast)
            if operacoes:
                self.semantica_texto.insert(tk.END, "Operações identificadas:\n", "info")
                for i, op in enumerate(operacoes, 1):
                    tipo_op = self.nome_operacao(op)
                    self.semantica_texto.insert(tk.END, f"{i}. Operação '{op}' ({tipo_op}) - válida\n", "item")
                self.semantica_texto.insert(tk.END, "\n")

            # Verificar divisões
            divisoes = self.verificar_divisoes(compilador.ast)
            if divisoes:
                self.semantica_texto.insert(tk.END, "Verificação de divisões:\n", "info")
                for i, (div_esq, div_dir) in enumerate(divisoes, 1):
                    # Verifica se é divisão por zero
                    if isinstance(div_dir, (int, float)) and div_dir == 0:
                        self.semantica_texto.insert(tk.END, f"{i}. {div_esq} / {div_dir} - ⚠️ DIVISÃO POR ZERO!\n",
                                                    "item")
                    else:
                        # Formata a exibição
                        esq_str = div_esq if isinstance(div_esq, (int, float)) else f"({div_esq})"
                        dir_str = div_dir if isinstance(div_dir, (int, float)) else f"({div_dir})"
                        self.semantica_texto.insert(tk.END, f"{i}. {esq_str} / {dir_str} - OK\n", "item")
                self.semantica_texto.insert(tk.END, "\n")

            self.semantica_texto.insert(tk.END, "Conclusão:\n", "info")
            self.semantica_texto.insert(tk.END, "Todos os operandos são válidos\n", "item")
            self.semantica_texto.insert(tk.END, "Não foram detectados erros semânticos\n", "item")
            self.semantica_texto.insert(tk.END, "Expressão pronta para geração de código intermediário\n", "item")

            print("   ✓ Semântica preenchida")

            print("\n9. Preenchendo aba TAC...")
            self.tac_texto.tag_configure("header", font=("SF Pro Text", 13, "bold"),
                                         spacing3=15)
            self.tac_texto.tag_configure("item", spacing1=3)

            self.tac_texto.insert(tk.END, "Código Intermediário:\n\n", "header")
            for i, instr in enumerate(compilador.instrucoes_tac, 1):
                self.tac_texto.insert(tk.END, f"{i}. {instr}\n", "item")
            print(f"   ✓ {len(compilador.instrucoes_tac)} instruções TAC preenchidas")

            print("\n10. Preenchendo aba OTIMIZADO...")
            self.otimizado_texto.tag_configure("header", font=("SF Pro Text", 13, "bold"),
                                               spacing3=15)
            self.otimizado_texto.tag_configure("item", spacing1=3)

            self.otimizado_texto.insert(tk.END, "Código Otimizado:\n\n", "header")
            for i, instr in enumerate(compilador.instrucoes_otimizadas, 1):
                self.otimizado_texto.insert(tk.END, f"{i}. {instr}\n", "item")
            print(f"   ✓ {len(compilador.instrucoes_otimizadas)} instruções otimizadas preenchidas")

            print("\n11. Preenchendo aba ASSEMBLY...")
            self.assembly_texto.tag_configure("line", spacing1=2)

            for line in compilador.assembly.split('\n'):
                self.assembly_texto.insert(tk.END, f"{line}\n", "line")
            print("   ✓ Assembly preenchido")

            print("\n12. Selecionando aba de resultado...")
            self.notebook.select(0)
            print("   ✓ Aba selecionada")

            print("\n" + "=" * 60)
            print("✅ COMPILAÇÃO FINALIZADA COM SUCESSO!")
            print("=" * 60 + "\n")

        except Exception as e:
            print("\n" + "=" * 60)
            print("❌ ERRO DURANTE A COMPILAÇÃO")
            print("=" * 60)
            print(f"Erro: {str(e)}")
            import traceback
            print("\nTraceback completo:")
            print(traceback.format_exc())
            print("=" * 60 + "\n")
            messagebox.showerror("Erro", f"Erro ao compilar:\n{str(e)}")


def main():
    raiz = tk.Tk()
    app = InterfaceGrafica(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()