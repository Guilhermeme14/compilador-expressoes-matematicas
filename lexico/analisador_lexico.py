import ply.lex as lex


class AnalisadorLexico:
    """Analisador Léxico - usa PLY para tokenização"""

    # Lista de nomes de tokens
    tokens = (
        'NUMERO',
        'MAIS',
        'MENOS',
        'VEZES',
        'DIVIDIR',
        'PAREN_ESQ',
        'PAREN_DIR',
    )

    # Regras de tokens simples
    t_MAIS = r'\+'
    t_MENOS = r'-'
    t_VEZES = r'\*'
    t_DIVIDIR = r'/'
    t_PAREN_ESQ = r'\('
    t_PAREN_DIR = r'\)'

    # Regra para números (inteiros e decimais)
    def t_NUMERO(self, t):
        r'\d+(\.\d+)?'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    # Ignora espaços e tabs
    t_ignore = ' \t'

    # Ignora quebras de linha
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Tratamento de erros
    def t_error(self, t):
        raise Exception(f"Caractere inválido '{t.value[0]}' na posição {t.lexpos}")

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.tokens_list = []

    def tokenizar(self, texto):
        self.tokens_list = []
        self.lexer.input(texto)

        while True:
            tok = self.lexer.token()
            if not tok:
                break
            self.tokens_list.append(tok)

        return self.tokens_list

    def obter_lexer(self):
        return self.lexer