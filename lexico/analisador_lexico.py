from .tipos_token import Token, TipoToken


class AnalisadorLexico:
    """Analisador Léxico - converte código fonte em tokens"""

    def __init__(self, texto: str):
        self.texto = texto
        self.posicao = 0
        self.caractere_atual = self.texto[0] if texto else None

    def erro(self):
        raise Exception(f"Caractere inválido na posição {self.posicao}: '{self.caractere_atual}'")

    def avancar(self):
        """Move para o próximo caractere"""
        self.posicao += 1
        if self.posicao >= len(self.texto):
            self.caractere_atual = None
        else:
            self.caractere_atual = self.texto[self.posicao]

    def pular_espacos(self):
        """Ignora espaços em branco"""
        while self.caractere_atual is not None and self.caractere_atual.isspace():
            self.avancar()

    def numero(self):
        """Reconhece números (inteiros e decimais)"""
        num_str = ''
        pos_inicial = self.posicao

        while self.caractere_atual is not None and (self.caractere_atual.isdigit() or self.caractere_atual == '.'):
            num_str += self.caractere_atual
            self.avancar()

        return Token(TipoToken.NUMERO, float(num_str) if '.' in num_str else int(num_str), pos_inicial)

    def obter_proximo_token(self):
        """Retorna o próximo token da entrada"""
        while self.caractere_atual is not None:
            if self.caractere_atual.isspace():
                self.pular_espacos()
                continue

            if self.caractere_atual.isdigit():
                return self.numero()

            if self.caractere_atual == '+':
                token = Token(TipoToken.MAIS, '+', self.posicao)
                self.avancar()
                return token

            if self.caractere_atual == '-':
                token = Token(TipoToken.MENOS, '-', self.posicao)
                self.avancar()
                return token

            if self.caractere_atual == '*':
                token = Token(TipoToken.MULTIPLICAR, '*', self.posicao)
                self.avancar()
                return token

            if self.caractere_atual == '/':
                token = Token(TipoToken.DIVIDIR, '/', self.posicao)
                self.avancar()
                return token

            if self.caractere_atual == '(':
                token = Token(TipoToken.PAREN_ESQ, '(', self.posicao)
                self.avancar()
                return token

            if self.caractere_atual == ')':
                token = Token(TipoToken.PAREN_DIR, ')', self.posicao)
                self.avancar()
                return token

            self.erro()

        return Token(TipoToken.FIM, None, self.posicao)