from analises.utils.mensagens.mensagemSemantico import declarada, naoDeclarada, divisaoPorZero


class analiseSemantica:

    def __init__(self, tokens):
        self.tokens = tokens
        self.variaveis = []
        self.variaveisZero = []
        self.erros = False
        self.log = []

    def pegarTokens(self):
        with open(self.tokens, 'r') as arquivo:
            lista = arquivo.readlines()
        return lista

    def analise(self):

        c = 0
        lista_tokens = self.pegarTokens()

        for token in lista_tokens:
            linha = token.split('|')

            if linha[1] == 'id':
                if lista_tokens[c-1].split('|')[0] == 'integer':
                    if linha[0] in self.variaveis:
                        self.log.append(declarada(linha))
                        self.erros = True
                    else:
                        self.variaveis.append(linha[0])

            if linha[1] == 'id':
                if lista_tokens[c+1].split('|')[1] == 'atribuicao':
                    if lista_tokens[c+2].split('|')[0] == '0':
                        self.variaveisZero.append(linha[0])
                if lista_tokens[c-1].split('|')[1] != 'tiponum':
                    if linha[0] not in self.variaveis:
                        self.log.append(naoDeclarada(linha))
                        self.erros = True

            if linha[1] == 'divisao':
                if lista_tokens[c+1].split('|')[0] == '0':
                    self.log.append(divisaoPorZero(linha))
                    self.erros = True
                    break
                elif lista_tokens[c+1].split('|')[1] == 'id' and lista_tokens[c+1].split('|')[0] in self.variaveisZero:
                    self.log.append(divisaoPorZero(linha))
                    self.erros = True
            c += 1

    def mostrar(self):
        if self.erros is False:
            print('A análise semântica foi finalizada e não foi encontrado nenhum erro!')
        else:
            [print(i) for i in self.log]
