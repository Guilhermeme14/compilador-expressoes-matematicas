from sintatico.nos_ast import NoAST, NoNumero, NoOperacaoBinaria


class Interpretador:

    def visitar(self, no: NoAST):
        nome_metodo = f'visitar_{type(no).__name__}'
        visitador = getattr(self, nome_metodo)
        return visitador(no)

    def visitar_NoNumero(self, no: NoNumero):
        return no.valor

    def visitar_NoOperacaoBinaria(self, no: NoOperacaoBinaria):
        esquerda = self.visitar(no.esquerda)
        direita = self.visitar(no.direita)

        if no.op == '+':
            return esquerda + direita
        elif no.op == '-':
            return esquerda - direita
        elif no.op == '*':
            return esquerda * direita
        elif no.op == '/':
            if direita == 0:
                raise Exception("Erro: Divisão por zero")
            return esquerda / direita