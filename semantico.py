class analiseSemantica:

    variaveis, variaveisZero, erros, log = [], [], False, []

    def __init__(self, tokens):
        self.tokens = tokens

    def analise(self):

        with open(self.tokens, 'r') as arquivo:
            tk = arquivo.readlines()

        c = 0

        for i in tk:

            linha = i.split('|')

            # Verificação se já existe uma variável declarada no programa em questão

            if linha[1] == 'id':
                if tk[c - 1].split('|')[0] == 'integer':
                    if linha[0] in self.variaveis:
                        self.log.append(f'A variável {linha[0]} na linha e coluna ({linha[2]}, {linha[3].strip()}) já foi declarada anteriormente. Declaração duplicada.')
                        self.erros = True
                        break
                    else:
                        self.variaveis.append(linha[0])

            # Verifica se é um identificador e compara os próximos tokens (atribuição e o valor)
            # se o valor for zero, é adicionado em uma lista chamada variaveisZero
            # Também faz uma verificação de uma variável que está sendo utilizada e faz uma verificação dentro da lista de variaveis, se tiver lá ela foi declarada

            if linha[1] == 'id':
                if tk[c + 1].split('|')[1] == 'atribuicao':
                    if tk[c + 2].split('|')[0] == '0':
                        self.variaveisZero.append(linha[0])
                elif tk[c - 1].split('|')[1] != 'tiponum':
                    if linha[0] not in self.variaveis:
                        self.log.append(f'A variável {linha[0]} na linha e coluna ({linha[2]}, {linha[3].strip()}) não foi declarada. Declare antes de usá-la!')
                        self.erros = True
                        break

            # Verificação para ver se ocorreu uma divisão por zero

            if linha[1] == 'divisao':
                if tk[c + 1].split('|')[0] == '0':
                    self.log.append(f'Ocorreu uma divisão por zero explícita na ({linha[2]}, {linha[3].strip()})')
                    self.erros = True
                    break
                elif tk[c + 1].split('|')[1] == 'id' and tk[c + 1].split('|')[0] in self.variaveisZero:
                    self.log.append(f'Ocorreu uma divisão por zero via atribuição de variável na linha e coluna ({linha[2]}, {linha[3].strip()})')
                    self.erros = True
                    break
            c += 1

    def mostrar(self):
        if self.erros is False:
            print('A análise semântica foi finalizada e não foi encontrado nenhum erro!')
        else:
            for i in self.log:
                print(i)


