from sintatico.nos_ast import NoAST, NoNumero, NoOperacaoBinaria
from lexico.tipos_token import TipoToken


class Interpretador:
    """Interpretador - executa a AST e retorna o resultado"""

    def visitar(self, no: NoAST):
        nome_metodo = f'visitar_{type(no).__name__}'
        visitador = getattr(self, nome_metodo)
        return visitador(no)

    def visitar_NoNumero(self, no: NoNumero):
        return no.valor

    def visitar_NoOperacaoBinaria(self, no: NoOperacaoBinaria):
        esquerda = self.visitar(no.esquerda)
        direita = self.visitar(no.direita)

        if no.op.tipo == TipoToken.MAIS:
            return esquerda + direita
        elif no.op.tipo == TipoToken.MENOS:
            return esquerda - direita
        elif no.op.tipo == TipoToken.MULTIPLICAR:
            return esquerda * direita
        elif no.op.tipo == TipoToken.DIVIDIR:
            if direita == 0:
                raise Exception("Erro: Divisão por zero")
            return esquerda / direita