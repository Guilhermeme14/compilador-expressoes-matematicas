import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
from enum import Enum
from typing import List, Optional, Dict, Tuple


# ====================
# CÓDIGO DO COMPILADOR (Original)
# ====================

class TokenType(Enum):
    """Tipos de tokens reconhecidos pelo compilador"""
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"


class Token:
    """Representa um token (unidade léxica)"""

    def __init__(self, type: TokenType, value: any, position: int):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type.value}, {self.value}, pos={self.position})"


class Lexer:
    """Analisador Léxico - converte código fonte em tokens"""

    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.current_char = self.text[0] if text else None

    def error(self):
        raise Exception(f"Caractere inválido na posição {self.position}: '{self.current_char}'")

    def advance(self):
        """Move para o próximo caractere"""
        self.position += 1
        if self.position >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.position]

    def skip_whitespace(self):
        """Ignora espaços em branco"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """Reconhece números (inteiros e decimais)"""
        num_str = ''
        start_pos = self.position

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            num_str += self.current_char
            self.advance()

        return Token(TokenType.NUMBER, float(num_str) if '.' in num_str else int(num_str), start_pos)

    def get_next_token(self):
        """Retorna o próximo token da entrada"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '+':
                token = Token(TokenType.PLUS, '+', self.position)
                self.advance()
                return token

            if self.current_char == '-':
                token = Token(TokenType.MINUS, '-', self.position)
                self.advance()
                return token

            if self.current_char == '*':
                token = Token(TokenType.MULTIPLY, '*', self.position)
                self.advance()
                return token

            if self.current_char == '/':
                token = Token(TokenType.DIVIDE, '/', self.position)
                self.advance()
                return token

            if self.current_char == '(':
                token = Token(TokenType.LPAREN, '(', self.position)
                self.advance()
                return token

            if self.current_char == ')':
                token = Token(TokenType.RPAREN, ')', self.position)
                self.advance()
                return token

            self.error()

        return Token(TokenType.EOF, None, self.position)


class ASTNode:
    """Nó da Árvore Sintática Abstrata"""
    pass


class NumberNode(ASTNode):
    """Nó representando um número"""

    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Num({self.value})"


class BinOpNode(ASTNode):
    """Nó representando uma operação binária"""

    def __init__(self, left: ASTNode, op: Token, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left} {self.op.value} {self.right})"


class Parser:
    """Analisador Sintático - constrói a AST"""

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception(f"Erro de sintaxe: token inesperado {self.current_token}")

    def eat(self, token_type: TokenType):
        """Consome um token do tipo esperado"""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : NUMBER | LPAREN expr RPAREN"""
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        self.error()

    def term(self):
        """term : factor ((MULTIPLY | DIVIDE) factor)*"""
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)

            node = BinOpNode(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOpNode(left=node, op=token, right=self.term())

        return node

    def parse(self):
        """Inicia o parsing"""
        return self.expr()


class SemanticAnalyzer:
    """Analisador Semântico - verifica a validade das operações"""

    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Método visit_{type(node).__name__} não definido')

    def visit_NumberNode(self, node: NumberNode):
        return True

    def visit_BinOpNode(self, node: BinOpNode):
        self.visit(node.left)
        self.visit(node.right)

        if node.op.type == TokenType.DIVIDE:
            if isinstance(node.right, NumberNode) and node.right.value == 0:
                raise Exception("Erro semântico: Divisão por zero detectada")

        return True


class TACInstruction:
    """Instrução de Código de Três Endereços"""

    def __init__(self, op: str, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        if self.arg2 is not None:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        else:
            return f"{self.result} = {self.arg1}"


class TACGenerator:
    """Gerador de Código Intermediário (Three-Address Code)"""

    def __init__(self):
        self.instructions = []
        self.temp_count = 0

    def new_temp(self):
        """Cria uma nova variável temporária"""
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name)
        return visitor(node)

    def visit_NumberNode(self, node: NumberNode):
        return node.value

    def visit_BinOpNode(self, node: BinOpNode):
        left = self.visit(node.left)
        right = self.visit(node.right)

        temp = self.new_temp()
        op_map = {
            TokenType.PLUS: '+',
            TokenType.MINUS: '-',
            TokenType.MULTIPLY: '*',
            TokenType.DIVIDE: '/'
        }

        instruction = TACInstruction(op_map[node.op.type], left, right, temp)
        self.instructions.append(instruction)

        return temp


class Optimizer:
    """Otimizador de código - constant folding e eliminação de código morto"""

    def __init__(self, instructions: List[TACInstruction]):
        self.instructions = instructions

    def constant_folding(self):
        """Avalia operações constantes em tempo de compilação"""
        optimized = []

        for instr in self.instructions:
            if isinstance(instr.arg1, (int, float)) and isinstance(instr.arg2, (int, float)):
                if instr.op == '+':
                    result = instr.arg1 + instr.arg2
                elif instr.op == '-':
                    result = instr.arg1 - instr.arg2
                elif instr.op == '*':
                    result = instr.arg1 * instr.arg2
                elif instr.op == '/':
                    result = instr.arg1 / instr.arg2

                optimized.append(TACInstruction('=', result, None, instr.result))
            else:
                optimized.append(instr)

        return optimized

    def optimize(self):
        """Aplica todas as otimizações"""
        return self.constant_folding()


class CodeGenerator:
    """Gerador de Código de Máquina Simplificado (Assembly-like)"""

    def __init__(self, instructions: List[TACInstruction]):
        self.instructions = instructions
        self.assembly = []

    def generate(self):
        """Gera código assembly simplificado"""
        self.assembly.append("; Código Assembly Gerado")
        self.assembly.append("; " + "=" * 40)

        for instr in self.instructions:
            if instr.arg2 is None:
                self.assembly.append(f"MOV {instr.result}, {instr.arg1}")
            else:
                op_map = {
                    '+': 'ADD',
                    '-': 'SUB',
                    '*': 'MUL',
                    '/': 'DIV'
                }

                self.assembly.append(f"MOV {instr.result}, {instr.arg1}")
                self.assembly.append(f"{op_map[instr.op]} {instr.result}, {instr.arg2}")

        return "\n".join(self.assembly)


class Interpreter:
    """Interpretador - executa a AST e retorna o resultado"""

    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name)
        return visitor(node)

    def visit_NumberNode(self, node: NumberNode):
        return node.value

    def visit_BinOpNode(self, node: BinOpNode):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == TokenType.PLUS:
            return left + right
        elif node.op.type == TokenType.MINUS:
            return left - right
        elif node.op.type == TokenType.MULTIPLY:
            return left * right
        elif node.op.type == TokenType.DIVIDE:
            if right == 0:
                raise Exception("Erro: Divisão por zero")
            return left / right


class Compiler:
    """Compilador completo - integra todas as etapas"""

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens = []
        self.ast = None
        self.tac_instructions = []
        self.optimized_instructions = []
        self.assembly = ""
        self.result = None

    def compile(self):
        """Executa todas as etapas da compilação"""
        # 1. Análise Léxica
        lexer = Lexer(self.source_code)
        while True:
            token = lexer.get_next_token()
            self.tokens.append(token)
            if token.type == TokenType.EOF:
                break

        # 2. Análise Sintática
        lexer = Lexer(self.source_code)
        parser = Parser(lexer)
        self.ast = parser.parse()

        # 3. Análise Semântica
        analyzer = SemanticAnalyzer()
        analyzer.visit(self.ast)

        # 4. Geração de Código Intermediário
        tac_gen = TACGenerator()
        tac_gen.visit(self.ast)
        self.tac_instructions = tac_gen.instructions

        # 5. Otimização
        optimizer = Optimizer(self.tac_instructions)
        self.optimized_instructions = optimizer.optimize()

        # 6. Geração de Código Final
        code_gen = CodeGenerator(self.optimized_instructions)
        self.assembly = code_gen.generate()

        # 7. Interpretação/Execução
        interpreter = Interpreter()
        self.result = interpreter.visit(self.ast)

        return self.result


# ====================
# INTERFACE GRÁFICA
# ====================

class CompilerGUI:
    """Interface Gráfica para o Compilador"""

    def __init__(self, root):
        self.root = root
        self.root.title("🔧 Compilador de Expressões Matemáticas")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2e")

        # Configurar estilo
        self.setup_styles()

        # Criar interface
        self.create_widgets()

    def setup_styles(self):
        """Configura os estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')

        # Cores
        bg_color = "#1e1e2e"
        fg_color = "#cdd6f4"
        accent_color = "#89b4fa"

        style.configure('Title.TLabel',
                        background=bg_color,
                        foreground=accent_color,
                        font=('Helvetica', 16, 'bold'))

        style.configure('Section.TLabel',
                        background=bg_color,
                        foreground=fg_color,
                        font=('Helvetica', 10, 'bold'))

        style.configure('TButton',
                        background=accent_color,
                        foreground='#1e1e2e',
                        font=('Helvetica', 10, 'bold'),
                        borderwidth=0,
                        focuscolor='none')

    def create_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        title_label = ttk.Label(main_frame,
                                text="🔧 COMPILADOR DE EXPRESSÕES MATEMÁTICAS",
                                style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        # Frame de entrada
        input_frame = tk.Frame(main_frame, bg="#313244", relief=tk.RIDGE, bd=2)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Label de entrada
        input_label = ttk.Label(input_frame,
                                text="📝 Digite a expressão:",
                                style='Section.TLabel')
        input_label.pack(anchor=tk.W, padx=10, pady=(10, 5))

        # Campo de entrada
        self.expression_entry = tk.Entry(input_frame,
                                         font=('Courier', 14),
                                         bg="#45475a",
                                         fg="#cdd6f4",
                                         insertbackground="#cdd6f4",
                                         relief=tk.FLAT,
                                         bd=5)
        self.expression_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.expression_entry.insert(0, "3 + 5 * 2")
        self.expression_entry.bind('<Return>', lambda e: self.compile_expression())

        # Frame de botões
        button_frame = tk.Frame(input_frame, bg="#313244")
        button_frame.pack(pady=(0, 10))

        # Botão compilar
        compile_btn = tk.Button(button_frame,
                                text="▶ COMPILAR",
                                command=self.compile_expression,
                                bg="#89b4fa",
                                fg="#1e1e2e",
                                font=('Helvetica', 12, 'bold'),
                                relief=tk.FLAT,
                                padx=30,
                                pady=10,
                                cursor='hand2')
        compile_btn.pack(side=tk.LEFT, padx=5)

        # Botão limpar
        clear_btn = tk.Button(button_frame,
                              text="🗑 LIMPAR",
                              command=self.clear_output,
                              bg="#f38ba8",
                              fg="#1e1e2e",
                              font=('Helvetica', 12, 'bold'),
                              relief=tk.FLAT,
                              padx=30,
                              pady=10,
                              cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Frame de exemplos
        examples_frame = tk.Frame(input_frame, bg="#313244")
        examples_frame.pack(pady=(0, 10))

        ttk.Label(examples_frame,
                  text="📚 Exemplos:",
                  style='Section.TLabel').pack(side=tk.LEFT, padx=5)

        examples = [
            "3 + 5 * 2",
            "(10 + 5) * 3",
            "100 / (2 + 3) - 5",
            "2.5 * 4 + 1.5"
        ]

        for example in examples:
            btn = tk.Button(examples_frame,
                            text=example,
                            command=lambda e=example: self.set_example(e),
                            bg="#45475a",
                            fg="#cdd6f4",
                            font=('Courier', 9),
                            relief=tk.FLAT,
                            padx=10,
                            pady=5,
                            cursor='hand2')
            btn.pack(side=tk.LEFT, padx=2)

        # Notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Criar abas
        self.create_tab("📊 Resultado", "result")
        self.create_tab("🔤 Tokens", "tokens")
        self.create_tab("🌳 AST", "ast")
        self.create_tab("⚙️ TAC", "tac")
        self.create_tab("⚡ Otimizado", "optimized")
        self.create_tab("💾 Assembly", "assembly")

    def create_tab(self, title, name):
        """Cria uma aba com área de texto"""
        frame = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(frame, text=title)

        text_widget = scrolledtext.ScrolledText(frame,
                                                font=('Courier', 11),
                                                bg="#1e1e2e",
                                                fg="#cdd6f4",
                                                insertbackground="#cdd6f4",
                                                relief=tk.FLAT,
                                                padx=10,
                                                pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)

        setattr(self, f"{name}_text", text_widget)

    def set_example(self, example):
        """Define um exemplo no campo de entrada"""
        self.expression_entry.delete(0, tk.END)
        self.expression_entry.insert(0, example)

    def clear_output(self):
        """Limpa todas as áreas de saída"""
        for name in ['result', 'tokens', 'ast', 'tac', 'optimized', 'assembly']:
            text_widget = getattr(self, f"{name}_text")
            text_widget.delete(1.0, tk.END)

    def compile_expression(self):
        """Compila a expressão e exibe os resultados"""
        expression = self.expression_entry.get().strip()

        if not expression:
            messagebox.showwarning("Aviso", "Por favor, digite uma expressão!")
            return

        try:
            # Limpar saídas anteriores
            self.clear_output()

            # Compilar
            compiler = Compiler(expression)
            result = compiler.compile()

            # Mostrar Resultado
            self.result_text.insert(tk.END, "=" * 50 + "\n")
            self.result_text.insert(tk.END, f"EXPRESSÃO: {expression}\n")
            self.result_text.insert(tk.END, "=" * 50 + "\n\n")
            self.result_text.insert(tk.END, f"✅ RESULTADO: {result}\n\n")
            self.result_text.insert(tk.END, "=" * 50 + "\n")

            # Mostrar Tokens
            self.tokens_text.insert(tk.END, "ANÁLISE LÉXICA - TOKENS\n")
            self.tokens_text.insert(tk.END, "=" * 50 + "\n\n")
            for token in compiler.tokens:
                self.tokens_text.insert(tk.END, f"{token}\n")

            # Mostrar AST
            self.ast_text.insert(tk.END, "ANÁLISE SINTÁTICA - ÁRVORE SINTÁTICA ABSTRATA\n")
            self.ast_text.insert(tk.END, "=" * 50 + "\n\n")
            self.ast_text.insert(tk.END, f"{compiler.ast}\n")

            # Mostrar TAC
            self.tac_text.insert(tk.END, "CÓDIGO INTERMEDIÁRIO (TAC)\n")
            self.tac_text.insert(tk.END, "=" * 50 + "\n\n")
            for instr in compiler.tac_instructions:
                self.tac_text.insert(tk.END, f"{instr}\n")

            # Mostrar Otimizado
            self.optimized_text.insert(tk.END, "CÓDIGO OTIMIZADO\n")
            self.optimized_text.insert(tk.END, "=" * 50 + "\n\n")
            for instr in compiler.optimized_instructions:
                self.optimized_text.insert(tk.END, f"{instr}\n")

            # Mostrar Assembly
            self.assembly_text.insert(tk.END, compiler.assembly)

            # Mudar para aba de resultado
            self.notebook.select(0)

        except Exception as e:
            messagebox.showerror("Erro de Compilação", str(e))


# ====================
# PROGRAMA PRINCIPAL
# ====================

def main():
    """Função principal"""
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()