from lexico.tipos_token import Token


class NoAST:
    """Nó base da Árvore Sintática Abstrata"""
    pass


class NoNumero(NoAST):
    """Nó representando um número"""

    def __init__(self, token: Token):
        self.token = token
        self.valor = token.valor

    def __repr__(self):
        return f"Num({self.valor})"


class NoOperacaoBinaria(NoAST):
    """Nó representando uma operação binária"""

    def __init__(self, esquerda: NoAST, op: Token, direita: NoAST):
        self.esquerda = esquerda
        self.op = op
        self.direita = direita

    def __repr__(self):
        return f"BinOp({self.esquerda} {self.op.valor} {self.direita})"