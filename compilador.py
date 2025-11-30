from lexico.analisador_lexico import AnalisadorLexico
from lexico.tipos_token import TipoToken
from sintatico.analisador_sintatico import AnalisadorSintatico
from semantico.analisador_semantico import AnalisadorSemantico
from geracao_codigo.gerador_tac import GeradorTAC
from geracao_codigo.otimizador import Otimizador
from geracao_codigo.gerador_assembly import GeradorCodigo
from interpretador import Interpretador


class Compilador:
    """Compilador completo - integra todas as etapas"""

    def __init__(self, codigo_fonte: str):
        self.codigo_fonte = codigo_fonte
        self.tokens = []
        self.ast = None
        self.instrucoes_tac = []
        self.instrucoes_otimizadas = []
        self.assembly = ""
        self.resultado = None

    def compilar(self):
        """Executa todas as etapas da compilação"""
        # 1. Análise Léxica
        analisador_lexico = AnalisadorLexico(self.codigo_fonte)
        while True:
            token = analisador_lexico.obter_proximo_token()
            self.tokens.append(token)
            if token.tipo == TipoToken.FIM:
                break

        # 2. Análise Sintática
        analisador_lexico = AnalisadorLexico(self.codigo_fonte)
        analisador_sintatico = AnalisadorSintatico(analisador_lexico)
        self.ast = analisador_sintatico.analisar()

        # 3. Análise Semântica
        analisador = AnalisadorSemantico()
        analisador.visitar(self.ast)

        # 4. Geração de Código Intermediário
        gerador_tac = GeradorTAC()
        gerador_tac.visitar(self.ast)
        self.instrucoes_tac = gerador_tac.instrucoes

        # 5. Otimização
        otimizador = Otimizador(self.instrucoes_tac)
        self.instrucoes_otimizadas = otimizador.otimizar()

        # 6. Geração de Código Final
        gerador_codigo = GeradorCodigo(self.instrucoes_otimizadas)
        self.assembly = gerador_codigo.gerar()

        # 7. Interpretação/Execução
        interpretador = Interpretador()
        self.resultado = interpretador.visitar(self.ast)

        return self.resultado