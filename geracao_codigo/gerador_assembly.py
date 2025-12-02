from typing import List
from .gerador_tac import InstrucaoTAC


class GeradorCodigo:
    def __init__(self, instrucoes: List[InstrucaoTAC]):
        self.instrucoes = instrucoes
        self.assembly = []

    def gerar(self):
        self.assembly.append("Código Assembly Gerado")
        self.assembly.append(" ")

        for instr in self.instrucoes:
            if instr.arg2 is None:
                self.assembly.append(f"MOV {instr.resultado}, {instr.arg1}")
            else:
                mapa_op = {
                    '+': 'ADD',
                    '-': 'SUB',
                    '*': 'MUL',
                    '/': 'DIV'
                }

                self.assembly.append(f"MOV {instr.resultado}, {instr.arg1}")
                self.assembly.append(f"{mapa_op[instr.op]} {instr.resultado}, {instr.arg2}")

        return "\n".join(self.assembly)