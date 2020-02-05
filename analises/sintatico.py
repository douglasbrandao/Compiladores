from csv import DictReader
from analises.utils.mensagens.mensagemSintatico import msgErroSintatico
from analises.utils.estruturas.listaProducoes import lista_producoes


class analiseSintatica:

    def __init__(self, tabela, tokens):
        self.tabela = tabela
        self.tokens = tokens
        self.logs = []
        self.logs_erros = []

    # Passo dois argumentos (O topo da pilha e o token no qual quero saber o retorno)
    def pegarChaveProducao(self, topo, token):
        with open(f'tabela/{self.tabela}') as arquivo_csv:
            tabela = DictReader(arquivo_csv)
            for x in tabela:
                if x['NAO-TERMINAIS'] == topo:
                    return x[token]

    # Após pegar a chave da produção, passo como argumento e retorno a produção pra a chave requerida
    def pegarProducao(self, chave):
        producoes = lista_producoes
        if chave in producoes:
            return producoes[chave]

    # Função apenas pra abrir a lista de tokens e retornar todos os tokens da lista
    def pegarTokens(self):
        with open(self.tokens) as arquivo:
            linhas = arquivo.readlines()
            tokens = [l.split('|') for l in linhas]
            return tokens

    def analise(self):

        i = 0

        pilha = []
        pilha.append('$')
        pilha.append('<FORMATO_PROGRAMA>')

        filaDeTokens = []
        fila = self.pegarTokens()
        filaDeTokens = [elemento[1] for elemento in fila]
        filaDeTokens.append('$')

        while True:
            pilhaTopo = pilha[-1]  # Topo da pilha
            # Passa o topo da filha e o token atual pra retornar a produção a ser verificada
            chaveProducao = self.pegarChaveProducao(pilhaTopo, filaDeTokens[i])
            if chaveProducao != '-':
                # Se a chave for diferente do '-', é retornado uma produção a ser verificada
                producao = self.pegarProducao(chaveProducao)
                if producao:
                    self.logs.append(f'Desempilhando: {pilha.pop()}')
                    # Inverte a lista de produção
                    listaProducao = list(reversed(producao[1]))
                    for elem in listaProducao:  # Percorro a lista retornada e empilho
                        pilha.append(elem)
                        self.logs.append(f'Empilhando: {elem}')
                else:
                    if pilhaTopo == filaDeTokens[i]:
                        if pilhaTopo == '$' and filaDeTokens[i] == '$':
                            self.logs.append(
                                'Análise finalizada e sem erro sintático!')
                            break
                        else:
                            self.logs.append(f'Desempilhando: {pilha.pop()}')
                            i += 1  # Movimenta na lista de tokens pro próximo a ser verificado
                    elif pilhaTopo == 'î':
                        self.logs.append(f'Desempilhando: {pilha.pop()}')
                    else:
                        self.logs.append(msgErroSintatico(fila, i))
                        self.logs_erros.append(msgErroSintatico(fila, i))
                        break
            else:
                if i == len(fila):
                    self.logs.append(msgErroSintatico(fila, i-1))
                    self.logs_erros.append(msgErroSintatico(fila, i-1))
                else:
                    self.logs.append(msgErroSintatico(fila, i))
                    self.logs_erros.append(msgErroSintatico(fila, i))
                break

    def mostraLog(self):
        print('Empilhando: $')
        print('Empilhando: <FORMATO_PROGRAMA>')
        [print(log) for log in self.logs]

    def mostraErros(self):
        [print(log) for log in self.logs_erros]
