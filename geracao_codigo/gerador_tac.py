from typing import List
from sintatico.nos_ast import NoAST, NoNumero, NoOperacaoBinaria
from lexico.tipos_token import TipoToken


class InstrucaoTAC:
    """Instrução de Código de Três Endereços"""

    def __init__(self, op: str, arg1, arg2, resultado):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.resultado = resultado

    def __repr__(self):
        if self.arg2 is not None:
            return f"{self.resultado} = {self.arg1} {self.op} {self.arg2}"
        else:
            return f"{self.resultado} = {self.arg1}"


class GeradorTAC:
    """Gerador de Código Intermediário"""

    def __init__(self):
        self.instrucoes = []
        self.contador_temp = 0

    def novo_temp(self):
        """Cria uma nova variável temporária"""
        temp = f"t{self.contador_temp}"
        self.contador_temp += 1
        return temp

    def visitar(self, no: NoAST):
        nome_metodo = f'visitar_{type(no).__name__}'
        visitador = getattr(self, nome_metodo)
        return visitador(no)

    def visitar_NoNumero(self, no: NoNumero):
        return no.valor

    def visitar_NoOperacaoBinaria(self, no: NoOperacaoBinaria):
        esquerda = self.visitar(no.esquerda)
        direita = self.visitar(no.direita)

        temp = self.novo_temp()
        mapa_op = {
            TipoToken.MAIS: '+',
            TipoToken.MENOS: '-',
            TipoToken.MULTIPLICAR: '*',
            TipoToken.DIVIDIR: '/'
        }

        instrucao = InstrucaoTAC(mapa_op[no.op.tipo], esquerda, direita, temp)
        self.instrucoes.append(instrucao)

        return temp