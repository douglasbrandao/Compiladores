from geracao.utils.infixaPosFixa import infixaPosFixa
from geracao.utils.funcoes.threeAddressCode import tac
from geracao.utils.funcoes.conditionais import condicional, loop


class Intermediario:

    def __init__(self, tokens):
        self.lista_tokens = tokens
        self.intermediario = []
        self.tokens = []
        self.pilha = []
        self.i = 0
        self.ctrl = 0
        self.L = self.C = 0

    def verificaOperador(self, op):
        operadores = {'<=': '>', '>=': '<'}
        if op in operadores:
            return operadores[op]

    def pegarTokens(self):
        with open(self.lista_tokens, "r") as arquivo:
            lista = arquivo.readlines()
        return lista

    def verificaExpressao(self, tokens, i):
        expressao = ''
        while tokens[i][1] != 'parenteses_fecha':
            expressao += ' ' + tokens[i][0]
            i += 1
        return expressao

    def verificaAtribuicao(self, variavel, i, cod, token):
        ex = ''
        while token[i][1] != 'fim_linha':
            ex += ' ' + token[i][0]
            i += 1
        return tac(variavel, infixaPosFixa(ex), cod, i)

    def verifica(self, tokens, i, L, C, pilha):
        if tokens[i][1] == 'ler':
            self.intermediario.append(f'LEIA {tokens[i+2][0]}')
            i += 4
        elif tokens[i][1] == 'escrever':
            self.intermediario.append(f'ESCREVA {tokens[i+2][0]}')
            i += 4
        elif tokens[i][1] == 'atribuicao':
            variavel = tokens[i-1][0]
            self.verificaAtribuicao(
                variavel, i+1, self.intermediario, tokens)
        elif tokens[i][1] == 'enquanto':
            expressao = self.verificaExpressao(tokens, i+2)
            op = expressao.split()[1]
            operador = self.verificaOperador(op)
            self.intermediario.append(loop(L, expressao, operador))
            i += 5
            while tokens[i][1] != 'chaves_fecha':
                i = self.verifica(tokens, i, L+i, C, pilha)
                i += 1
            self.intermediario.append(f'_L{L+1}:')
        elif tokens[i][1] == 'se':
            expressao = self.verificaExpressao(tokens, i+2)
            op = expressao.split()[1]
            operador = self.verificaOperador(op)
            self.intermediario.append(condicional(C, expressao, operador))
            i += 5
            while tokens[i][1] != 'chaves_fecha':
                i = self.verifica(tokens, i, L, C+i, pilha)
                i += 1
            self.intermediario.append(f'_C{C+1}:')
        return i

    def geracao(self):

        lista_tokens = self.pegarTokens()
        self.tokens = [token.split('|') for token in lista_tokens]

        for token in self.tokens:
            if token[1] == 'id' and self.tokens[self.ctrl-1][1] == 'tiponum':
                self.intermediario.append(f'INTEIRO {token[0]}')
            self.ctrl += 1

        while self.i < len(self.tokens):
            self.i = self.verifica(self.tokens, self.i,
                                   self.L, self.C, self.pilha)
            self.i += 1
            self.C += 1
            self.L += 1

    def mostrar(self):
        [print(codigo) for codigo in self.intermediario]

    def salvarIntermediario(self):
        with open('intermediario.itm', 'w') as arq:
            arq.writelines('\n'.join(self.intermediario))
