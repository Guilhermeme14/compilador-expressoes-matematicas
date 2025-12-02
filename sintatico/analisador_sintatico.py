import ply.yacc as yacc
from lexico.analisador_lexico import AnalisadorLexico
from .nos_ast import NoNumero, NoOperacaoBinaria


class AnalisadorSintatico:
    tokens = AnalisadorLexico.tokens
    precedence = (
        ('left', 'MAIS', 'MENOS'),
        ('left', 'VEZES', 'DIVIDIR'),
    )

    def __init__(self):
        self.analisador_lexico = AnalisadorLexico()
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False)
        self.ast = None

    # Regras gramaticais
    def p_expressao(self, p):
        """expressao : termo"""
        p[0] = p[1]

    def p_expressao_binaria(self, p):
        """expressao : expressao MAIS expressao
                     | expressao MENOS expressao"""
        p[0] = NoOperacaoBinaria(p[2], p[1], p[3])

    def p_termo_binario(self, p):
        """termo : termo VEZES termo
                 | termo DIVIDIR termo"""
        p[0] = NoOperacaoBinaria(p[2], p[1], p[3])

    def p_termo_fator(self, p):
        """termo : fator"""
        p[0] = p[1]

    def p_fator_numero(self, p):
        """fator : NUMERO"""
        p[0] = NoNumero(p[1])

    def p_fator_parenteses(self, p):
        """fator : PAREN_ESQ expressao PAREN_DIR"""
        p[0] = p[2]

    def p_error(self, p):
        if p:
            raise Exception(f"Erro de sintaxe no token '{p.value}' na posição {p.lexpos}")
        else:
            raise Exception("Erro de sintaxe: fim inesperado da expressão")

    def analisar(self, texto):
        lexer = self.analisador_lexico.obter_lexer()
        self.ast = self.parser.parse(texto, lexer=lexer)
        return self.ast

    def obter_tokens(self):
        return self.analisador_lexico.tokens_list