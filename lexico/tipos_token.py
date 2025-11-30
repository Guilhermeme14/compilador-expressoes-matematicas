from enum import Enum


class TipoToken(Enum):
    """Tipos de tokens reconhecidos pelo compilador"""
    NUMERO = "NUMERO"
    MAIS = "MAIS"
    MENOS = "MENOS"
    MULTIPLICAR = "MULTIPLICAR"
    DIVIDIR = "DIVIDIR"
    PAREN_ESQ = "PAREN_ESQ"
    PAREN_DIR = "PAREN_DIR"
    FIM = "FIM"


class Token:
    """Representa um token (unidade léxica)"""

    def __init__(self, tipo: TipoToken, valor: any, posicao: int):
        self.tipo = tipo
        self.valor = valor
        self.posicao = posicao

    def __repr__(self):
        return f"Token({self.tipo.value}, {self.valor}, pos={self.posicao})"