from lexico.analisador_lexico import AnalisadorLexico
from lexico.tipos_token import TipoToken
from .nos_ast import NoNumero, NoOperacaoBinaria


class AnalisadorSintatico:
    """Analisador Sintático - constrói a AST"""

    def __init__(self, analisador_lexico: AnalisadorLexico):
        self.analisador_lexico = analisador_lexico
        self.token_atual = self.analisador_lexico.obter_proximo_token()

    def erro(self):
        raise Exception(f"Erro de sintaxe: token inesperado {self.token_atual}")

    def consumir(self, tipo_token: TipoToken):
        """Consome um token do tipo esperado"""
        if self.token_atual.tipo == tipo_token:
            self.token_atual = self.analisador_lexico.obter_proximo_token()
        else:
            self.erro()

    def fator(self):
        """fator : NUMERO | PAREN_ESQ expressao PAREN_DIR"""
        token = self.token_atual

        if token.tipo == TipoToken.NUMERO:
            self.consumir(TipoToken.NUMERO)
            return NoNumero(token)
        elif token.tipo == TipoToken.PAREN_ESQ:
            self.consumir(TipoToken.PAREN_ESQ)
            no = self.expressao()
            self.consumir(TipoToken.PAREN_DIR)
            return no

        self.erro()

    def termo(self):
        """termo : fator ((MULTIPLICAR | DIVIDIR) fator)*"""
        no = self.fator()

        while self.token_atual.tipo in (TipoToken.MULTIPLICAR, TipoToken.DIVIDIR):
            token = self.token_atual
            if token.tipo == TipoToken.MULTIPLICAR:
                self.consumir(TipoToken.MULTIPLICAR)
            elif token.tipo == TipoToken.DIVIDIR:
                self.consumir(TipoToken.DIVIDIR)

            no = NoOperacaoBinaria(esquerda=no, op=token, direita=self.fator())

        return no

    def expressao(self):
        """expressao : termo ((MAIS | MENOS) termo)*"""
        no = self.termo()

        while self.token_atual.tipo in (TipoToken.MAIS, TipoToken.MENOS):
            token = self.token_atual
            if token.tipo == TipoToken.MAIS:
                self.consumir(TipoToken.MAIS)
            elif token.tipo == TipoToken.MENOS:
                self.consumir(TipoToken.MENOS)

            no = NoOperacaoBinaria(esquerda=no, op=token, direita=self.termo())

        return no

    def analisar(self):
        """Inicia a análise sintática"""
        return self.expressao()