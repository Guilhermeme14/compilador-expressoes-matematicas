import re
from enum import Enum
from typing import List, Optional, Dict, Tuple


# ====================
# 1. ANÁLISE LÉXICA
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


# ====================
# 2. ANÁLISE SINTÁTICA
# ====================

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


# ====================
# 3. ANÁLISE SEMÂNTICA
# ====================

class SemanticAnalyzer:
    """Analisador Semântico - verifica a validade das operações"""

    def visit(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Método visit_{type(node).__name__} não definido')

    def visit_NumberNode(self, node: NumberNode):
        # Números são sempre válidos
        return True

    def visit_BinOpNode(self, node: BinOpNode):
        # Verifica os operandos
        self.visit(node.left)
        self.visit(node.right)

        # Verifica divisão por zero (análise estática básica)
        if node.op.type == TokenType.DIVIDE:
            if isinstance(node.right, NumberNode) and node.right.value == 0:
                raise Exception("Erro semântico: Divisão por zero detectada")

        return True


# ====================
# 4. CÓDIGO INTERMEDIÁRIO (TAC)
# ====================

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


# ====================
# 5. OTIMIZAÇÃO
# ====================

class Optimizer:
    """Otimizador de código - constant folding e eliminação de código morto"""

    def __init__(self, instructions: List[TACInstruction]):
        self.instructions = instructions

    def constant_folding(self):
        """Avalia operações constantes em tempo de compilação"""
        optimized = []

        for instr in self.instructions:
            # Se ambos operandos são números, calcula o resultado
            if isinstance(instr.arg1, (int, float)) and isinstance(instr.arg2, (int, float)):
                if instr.op == '+':
                    result = instr.arg1 + instr.arg2
                elif instr.op == '-':
                    result = instr.arg1 - instr.arg2
                elif instr.op == '*':
                    result = instr.arg1 * instr.arg2
                elif instr.op == '/':
                    result = instr.arg1 / instr.arg2

                # Cria nova instrução com resultado calculado
                optimized.append(TACInstruction('=', result, None, instr.result))
            else:
                optimized.append(instr)

        return optimized

    def optimize(self):
        """Aplica todas as otimizações"""
        return self.constant_folding()


# ====================
# 6. GERAÇÃO DE CÓDIGO FINAL
# ====================

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
                # Atribuição simples
                self.assembly.append(f"MOV {instr.result}, {instr.arg1}")
            else:
                # Operação binária
                op_map = {
                    '+': 'ADD',
                    '-': 'SUB',
                    '*': 'MUL',
                    '/': 'DIV'
                }

                self.assembly.append(f"MOV {instr.result}, {instr.arg1}")
                self.assembly.append(f"{op_map[instr.op]} {instr.result}, {instr.arg2}")

        return "\n".join(self.assembly)


# ====================
# 7. INTERPRETADOR
# ====================

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


# ====================
# 8. COMPILADOR COMPLETO
# ====================

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

    def compile(self, verbose=True):
        """Executa todas as etapas da compilação"""
        if verbose:
            print("=" * 60)
            print("COMPILADOR DE EXPRESSÕES MATEMÁTICAS")
            print("=" * 60)
            print(f"\nCÓDIGO FONTE: {self.source_code}\n")

        # 1. Análise Léxica
        if verbose:
            print("1. ANÁLISE LÉXICA (Tokenização)")
            print("-" * 40)
        lexer = Lexer(self.source_code)
        while True:
            token = lexer.get_next_token()
            self.tokens.append(token)
            if verbose:
                print(f"  {token}")
            if token.type == TokenType.EOF:
                break

        # 2. Análise Sintática
        if verbose:
            print("\n2. ANÁLISE SINTÁTICA (Parsing)")
            print("-" * 40)
        lexer = Lexer(self.source_code)
        parser = Parser(lexer)
        self.ast = parser.parse()
        if verbose:
            print(f"  AST: {self.ast}")

        # 3. Análise Semântica
        if verbose:
            print("\n3. ANÁLISE SEMÂNTICA")
            print("-" * 40)
        analyzer = SemanticAnalyzer()
        analyzer.visit(self.ast)
        if verbose:
            print("  ✓ Análise semântica concluída com sucesso")

        # 4. Geração de Código Intermediário
        if verbose:
            print("\n4. GERAÇÃO DE CÓDIGO INTERMEDIÁRIO (TAC)")
            print("-" * 40)
        tac_gen = TACGenerator()
        tac_gen.visit(self.ast)
        self.tac_instructions = tac_gen.instructions
        if verbose:
            for instr in self.tac_instructions:
                print(f"  {instr}")

        # 5. Otimização
        if verbose:
            print("\n5. OTIMIZAÇÃO")
            print("-" * 40)
        optimizer = Optimizer(self.tac_instructions)
        self.optimized_instructions = optimizer.optimize()
        if verbose:
            for instr in self.optimized_instructions:
                print(f"  {instr}")

        # 6. Geração de Código Final
        if verbose:
            print("\n6. GERAÇÃO DE CÓDIGO ASSEMBLY")
            print("-" * 40)
        code_gen = CodeGenerator(self.optimized_instructions)
        self.assembly = code_gen.generate()
        if verbose:
            print(self.assembly)

        # 7. Interpretação/Execução
        if verbose:
            print("\n7. EXECUÇÃO")
            print("-" * 40)
        interpreter = Interpreter()
        self.result = interpreter.visit(self.ast)
        if verbose:
            print(f"  RESULTADO: {self.result}")
            print("\n" + "=" * 60)

        return self.result


# ====================
# 9. PROGRAMA PRINCIPAL
# ====================

def main():
    """Programa principal - interface com o usuário"""
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "COMPILADOR DE EXPRESSÕES MATEMÁTICAS" + " " * 12 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # Exemplos de teste
    test_cases = [
        "3 + 5 * 2",
        "(10 + 5) * 3",
        "100 / (2 + 3) - 5",
        "2.5 * 4 + 1.5"
    ]

    print("Exemplos pré-definidos:")
    for i, expr in enumerate(test_cases, 1):
        print(f"  {i}. {expr}")

    print("\nDigite uma expressão matemática (ou pressione Enter para usar exemplo 1):")
    user_input = input(">> ").strip()

    if not user_input:
        user_input = test_cases[0]
        print(f"Usando exemplo: {user_input}")

    try:
        compiler = Compiler(user_input)
        result = compiler.compile(verbose=True)

    except Exception as e:
        print(f"\n❌ ERRO: {e}")


if __name__ == "__main__":
    main()