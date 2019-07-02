from infixaPosFixa import infixaPosFixa

class Intermediario:

    # variáveis de controle
    i, ctrl = 0, 0

    # declaração das listas de apoio
    cod_intermediario, tokens, pilha = [], [], []

    def __init__(self, tokens):
        self.lista_tokens = tokens

    def verificaOperador(self, op):
        options = {'<=': '>', '>=': '<', '==': '='}
        if op in options:
            return options[op]

    def verificaExpressao(self, tokens, i):
        expressao = ''
        while tokens[i][1] != 'parenteses_fecha':  # enquanto não encontrar um fechamento de parenteses, acumula os tokens no buffer
            expressao += ' ' + tokens[i][0]
            i += 1
        return expressao

    def tac(self, var, expression, cod, it):
        exp = expression.split()
        stack = []
        oper = ['+', '-', '*', '/']
        for i in range(len(exp)):
            if exp[i] in oper:
                v1 = stack.pop()
                v2 = stack.pop()
                t = f'{v2} {exp[i]} {v1}'
                if len(exp) == i+1:
                    cod.append(f'{var} := {t}')
                else:
                    cod.append(f't{it} := {t}')
                    stack.append(f't{it}')
                    it += 1
            else:
                stack.append(exp[i])
        if len(stack) == 1:
            cod.append(f'{var} := {stack[0]}')

    def verificaAtribuicao(self, variavel, i, cod, tok):
        ex = ''
        while tok[i][1] != 'fim_linha':  # Enquanto não encontrar um token de fim linha
            ex += ' ' + tok[i][0]  # o buffer acumula os tokens encontrados
            i += 1
        return self.tac(variavel, infixaPosFixa(ex), cod, i)  # Chama a função tac (three address code) passando a variavel, expressao pos fixada, a lista e a iteração

    def verifica(self, tokens, i, L, C, pilha):
        if tokens[i][1] == 'ler':  # Verifica se o token é de leitura, mostra o token e pula 4 iterações
            self.cod_intermediario.append(f'LEIA {tokens[i + 2][0]}')
            i += 4
        elif tokens[i][1] == 'escrever':  # Verifica se o token é de escrita, mostra o token e pula 4 iterações
            self.cod_intermediario.append(f'ESCREVA {tokens[i + 2][0]}')
            i += 4
        elif tokens[i][1] == 'atribuicao':  # Verifica se o token é de atribuição e avança 1 iteração
            variavel = tokens[i - 1][0]
            self.verificaAtribuicao(variavel, i + 1, self.cod_intermediario, tokens)
        elif tokens[i][1] == 'enquanto':  # Verifica se o token encontrado é um enquanto
            expressao = self.verificaExpressao(tokens, i + 2)
            op = expressao.split()[1]
            operador = self.verificaOperador(op)
            self.cod_intermediario.append(
                f'_L{L}: if {expressao.split()[0]} {operador} {expressao.split()[2]} goto _L{L + 1}')
            i += 5
            while tokens[i][1] != 'chaves_fecha':
                i = self.verifica(tokens, i, L + i, C, pilha)
                i += 1
            self.cod_intermediario.append(f'_L{L + 1}:')
        elif tokens[i][1] == 'se':  # Verifica se o token encontrado é um enquanto
            expressao = self.verificaExpressao(tokens, i + 2)
            op = expressao.split()[1]
            operador = self.verificaOperador(op)
            self.cod_intermediario.append(
                f'_C{C}: if {expressao.split()[0]} {operador} {expressao.split()[2]} goto _C{C + 1}')
            i += 5
            while tokens[i][1] != 'chaves_fecha':
                i = self.verifica(tokens, i, L, C + i, pilha)
                i += 1
            self.cod_intermediario.append(f'_C{C + 1}:')
        return i

    def geracao(self):

        # Abertura da lista de tokens retornada na análise léxica

        with open(self.lista_tokens, "r") as arquivo:
            tk = arquivo.readlines()

        for j in tk:
            self.tokens.append(j.split('|'))

        # Faz a verificação da declaração das variáveis

        for tk in self.tokens:
            if tk[1] == 'id' and self.tokens[self.ctrl - 1][1] == 'tiponum':
                self.cod_intermediario.append(f'INTEIRO {tk[0]}')
            self.ctrl += 1

        self.L = self.C = 0

        while self.i < len(self.tokens):
            self.i = self.verifica(self.tokens, self.i, self.L, self.C, self.pilha)
            self.i += 1
            self.C += 1
            self.L += 1

    def mostrar(self):
        for codigo in self.cod_intermediario:
            print(codigo)

    def salvarIntermediario(self):
        with open('intermediario.itm', 'w') as arq:
            arq.writelines('\n'.join(self.cod_intermediario))