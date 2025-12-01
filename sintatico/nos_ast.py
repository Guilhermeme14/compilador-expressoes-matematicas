class NoAST:
    """Nó base da Árvore Sintática Abstrata"""
    pass


class NoNumero(NoAST):
    """Nó representando um número"""

    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"Num({self.valor})"


class NoOperacaoBinaria(NoAST):
    """Nó representando uma operação binária"""

    def __init__(self, op, esquerda, direita):
        self.op = op
        self.esquerda = esquerda
        self.direita = direita

    def __repr__(self):
        return f"BinOp({self.esquerda} {self.op} {self.direita})"