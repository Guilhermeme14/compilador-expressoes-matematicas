# compiler.py - Versão Corrigida Completa
# (Conteúdo completo foi substituído aqui)

# --------------------------------------------
# TOKENS
# --------------------------------------------

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# --------------------------------------------
# LEXER
# --------------------------------------------

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def advance(self):
        self.pos += 1

    def peek(self):
        if self.pos + 1 < len(self.text):
            return self.text[self.pos+1]
        return None

    def generate_tokens(self):
        tokens = []
        while self.pos < len(self.text):
            char = self.text[self.pos]

            if char.isspace():
                self.advance()
                continue

            if char.isdigit():
                tokens.append(self.number())
                continue

            if char == '+': tokens.append(Token("PLUS", '+'))
            elif char == '-': tokens.append(Token("MINUS", '-'))
            elif char == '*': tokens.append(Token("MUL", '*'))
            elif char == '/': tokens.append(Token("DIV", '/'))
            elif char == '(': tokens.append(Token("LPAREN", '('))
            elif char == ')': tokens.append(Token("RPAREN", ')'))
            else:
                raise Exception(f"Caractere inválido: {char}")

            self.advance()

        tokens.append(Token("EOF", ''))
        return tokens

    def number(self):
        digits = ""
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            digits += self.text[self.pos]
            self.advance()
        return Token("NUMBER", float(digits) if '.' in digits else int(digits))

# --------------------------------------------
# AST
# --------------------------------------------

class Number:
    def __init__(self, value): self.value = value
    def __repr__(self): return f"Number({self.value})"

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self): return f"BinOp({self.left}, {self.op.type}, {self.right})"

# --------------------------------------------
# PARSER
# --------------------------------------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, type_):
        token = self.tokens[self.pos]
        if token.type == type_:
            self.pos += 1
            return token
        raise Exception(f"Esperado token {type_}, obtido {token.type}")

    def peek(self): return self.tokens[self.pos]

    def parse(self): return self.expr()

    def expr(self):
        node = self.term()
        while self.peek().type in ("PLUS", "MINUS"):
            op = self.consume(self.peek().type)
            node = BinOp(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.peek().type in ("MUL", "DIV"):
            op = self.consume(self.peek().type)
            node = BinOp(node, op, self.factor())
        return node

    def factor(self):
        token = self.peek()

        if token.type == "NUMBER":
            self.consume("NUMBER")
            return Number(token.value)

        if token.type == "LPAREN":
            self.consume("LPAREN")
            node = self.expr()
            self.consume("RPAREN")
            return node

        if token.type == "MINUS":
            self.consume("MINUS")
            return BinOp(Number(0), Token("MINUS", '-'), self.factor())

        raise Exception("Fator inválido")

# --------------------------------------------
# AVALIADOR DO AST
# --------------------------------------------

def eval_ast(node):
    if isinstance(node, Number):
        return node.value

    if isinstance(node, BinOp):
        left = eval_ast(node.left)
        right = eval_ast(node.right)

        if node.op.type == "PLUS":
            return left + right
        if node.op.type == "MINUS":
            return left - right
        if node.op.type == "MUL":
            return left * right
        if node.op.type == "DIV":
            if right == 0:
                return float('inf')
            return left / right

    raise Exception("AST inválido para avaliação")("AST inválido para avaliação")

# --------------------------------------------
# CONSTANT FOLDING (corrigido)
# --------------------------------------------

def constant_fold(node):
    if isinstance(node, Number): return node

    if isinstance(node, BinOp):
        left = constant_fold(node.left)
        right = constant_fold(node.right)

        if isinstance(left, Number) and isinstance(right, Number):
            try:
                if node.op.type == "PLUS": return Number(left.value + right.value)
                if node.op.type == "MINUS": return Number(left.value - right.value)
                if node.op.type == "MUL": return Number(left.value * right.value)
                if node.op.type == "DIV":
                    if right.value == 0:
                        return BinOp(left, node.op, right)
                    return Number(left.value / right.value)
            except:
                return BinOp(left, node.op, right)

        return BinOp(left, node.op, right)

    return node

# --------------------------------------------
# TAC
# --------------------------------------------

class TACGenerator:
    def __init__(self):
        self.temp_id = 1
        self.code = []

    def new_temp(self):
        t = f"t{self.temp_id}"
        self.temp_id += 1
        return t

    def generate(self, node):
        if isinstance(node, Number):
            t = self.new_temp()
            self.code.append(f"{t} = mov {node.value}")
            return t

        if isinstance(node, BinOp):
            left = self.generate(node.left)
            right = self.generate(node.right)
            t = self.new_temp()
            self.code.append(f"{t} = {left} {node.op.value} {right}")
            return t

        raise Exception("Nodo AST inválido no TAC")

# --------------------------------------------
# COMPILADOR (função principal)
# --------------------------------------------

def compile_expr(expr, do_opt=True):
    lexer = Lexer(expr)
    tokens = lexer.generate_tokens()
    parser = Parser(tokens)
    ast = parser.parse()

    optimized_ast = constant_fold(ast) if do_opt else ast

    tac = TACGenerator()
    tac.generate(optimized_ast)

    result = eval_ast(optimized_ast)

    return {
        "tokens": tokens,
        "ast": ast,
        "optimized_ast": optimized_ast,
        "tac": tac.code,
        "result": result
    }

# --------------------------------------------
# EXEMPLOS
# --------------------------------------------

if __name__ == "__main__":
    exemplos = [
        "3 + 5 * 2",
        "-(4 - 2) * (3 + 1)",
        "10 / (5 - 5)",
        "2 + 3 * (7 - 4) / 3.0"
    ]

    for expr in exemplos:
        print("------------------------------------------------")
        print(f"Expr: {expr}")
        r = compile_expr(expr)
        print("Tokens:", r["tokens"])
        print("AST:", r["ast"])
        print("AST otimizado:", r["optimized_ast"])
        print("TAC:")
        for line in r["tac"]:
            print(" ", line)
        print("Resultado:", r["result"])
