class NoAST:
    pass


class NoNumero(NoAST):

    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"Num({self.valor})"


class NoOperacaoBinaria(NoAST):
    def __init__(self, op, esquerda, direita):
        self.op = op
        self.esquerda = esquerda
        self.direita = direita

    def __repr__(self):
        return f"BinOp({self.esquerda} {self.op} {self.direita})"