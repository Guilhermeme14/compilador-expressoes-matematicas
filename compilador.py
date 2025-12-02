from sintatico.analisador_sintatico import AnalisadorSintatico
from semantico.analisador_semantico import AnalisadorSemantico
from geracao_codigo.gerador_tac import GeradorTAC
from geracao_codigo.otimizador import Otimizador
from geracao_codigo.gerador_assembly import GeradorCodigo
from interpretador import Interpretador


class Compilador:
    def __init__(self, codigo_fonte: str):
        self.codigo_fonte = codigo_fonte
        self.tokens = []
        self.ast = None
        self.instrucoes_tac = []
        self.instrucoes_otimizadas = []
        self.assembly = ""
        self.resultado = None

    def compilar(self):
        analisador = AnalisadorSintatico()
        self.ast = analisador.analisar(self.codigo_fonte)

        analisador.analisador_lexico.tokenizar(self.codigo_fonte)
        self.tokens = analisador.analisador_lexico.tokens_list

        analisador_semantico = AnalisadorSemantico()
        analisador_semantico.visitar(self.ast)

        gerador_tac = GeradorTAC()
        gerador_tac.visitar(self.ast)
        self.instrucoes_tac = gerador_tac.instrucoes

        otimizador = Otimizador(self.instrucoes_tac)
        self.instrucoes_otimizadas = otimizador.otimizar()

        gerador_codigo = GeradorCodigo(self.instrucoes_otimizadas)
        self.assembly = gerador_codigo.gerar()

        interpretador = Interpretador()
        self.resultado = interpretador.visitar(self.ast)

        return self.resultado