from sintatico.nos_ast import NoAST, NoNumero, NoOperacaoBinaria
from lexico.tipos_token import TipoToken


class AnalisadorSemantico:
    """Analisador Semântico - verifica a validade das operações"""

    def visitar(self, no: NoAST):
        nome_metodo = f'visitar_{type(no).__name__}'
        visitador = getattr(self, nome_metodo, self.visita_generica)
        return visitador(no)

    def visita_generica(self, no):
        raise Exception(f'Método visitar_{type(no).__name__} não definido')

    def visitar_NoNumero(self, no: NoNumero):
        return True

    def visitar_NoOperacaoBinaria(self, no: NoOperacaoBinaria):
        self.visitar(no.esquerda)
        self.visitar(no.direita)

        if no.op.tipo == TipoToken.DIVIDIR:
            if isinstance(no.direita, NoNumero) and no.direita.valor == 0:
                raise Exception("Erro semântico: Divisão por zero detectada")

        return True