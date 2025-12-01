from typing import List
from .gerador_tac import InstrucaoTAC


class Otimizador:
    """Otimizador de código - constant folding e eliminação de código morto"""

    def __init__(self, instrucoes: List[InstrucaoTAC]):
        self.instrucoes = instrucoes

    def dobramento_constantes(self):
        """Avalia operações constantes em tempo de compilação"""
        otimizado = []

        for instr in self.instrucoes:
            if isinstance(instr.arg1, (int, float)) and isinstance(instr.arg2, (int, float)):
                if instr.op == '+':
                    resultado = instr.arg1 + instr.arg2
                elif instr.op == '-':
                    resultado = instr.arg1 - instr.arg2
                elif instr.op == '*':
                    resultado = instr.arg1 * instr.arg2
                elif instr.op == '/':
                    resultado = instr.arg1 / instr.arg2

                otimizado.append(InstrucaoTAC('=', resultado, None, instr.resultado))
            else:
                otimizado.append(instr)

        return otimizado

    def otimizar(self):
        """Aplica todas as otimizações"""
        return self.dobramento_constantes()