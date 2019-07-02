import csv

class analiseSintatica:

    erros = False
    log, log_erros = [], []

    def __init__(self, tabela, tokens):
        self.tabela = tabela
        self.tokens = tokens

    def getProducaoChave(self, top, token): # Passo dois argumentos (O topo da pilha e o token no qual quero saber o retorno)

        with open(f'tabela/{self.tabela}') as arquivo:
            table = csv.DictReader(arquivo)
            for x in table:
                if x['NAO-TERMINAIS'] == top:
                    return x[token]

    def getProducao(self, key): # Após pegar a chave da produção, passo como argumento e retorno a produção pra a chave requerida

        producoes = {
            '0': ('<LISTA_COMANDOS>', ['<COMANDO>', '<LISTA_COMANDOS>']),
            '1': ('<LISTA_COMANDOS>', 'î'),
            '2': ('<FORMATO_PROGRAMA', ['tk_inicio', '<LISTA_COMANDOS>', 'tk_fim']),
            '3': ('<COMANDO>', ['escrever', 'parenteses_abre', '<ARGUMENTACAO>', 'parenteses_fecha', 'fim_linha']),
            '4': ('<COMANDO>', ['ler', 'parenteses_abre', 'id', 'parenteses_fecha', 'fim_linha']),
            '5': ('<COMANDO>', ['<DECLARACAO>', 'fim_linha']),
            '6': ('<COMANDO>', ['se', '<LOGICO>', 'chaves_abre', '<LISTA_COMANDOS>', 'chaves_fecha', '<SENAO>']),
            '7': ('<COMANDO>', ['enquanto', '<LOGICO>', 'chaves_abre', '<LISTA_COMANDOS>', 'chaves_fecha']),
            '8': ('<OPERADORES_MAT>', ['adicao']),
            '9': ('<OPERADORES_MAT>', ['subtracao']),
            '10': ('<OPERADORES_MAT>', ['mult']),
            '11': ('<OPERADORES_MAT>', ['divisao']),
            '12': ('<OPERADORES_LOGICOS>', ['maiorigual']),
            '13': ('<OPERADORES_LOGICOS>', ['menorigual']),
            '14': ('<OPERADORES_LOGICOS>', ['igual']),
            '15': ('<ARGUMENTACAO>', ['<STRING>']),
            '16': ('<ARGUMENTACAO>', ['<NUMERO>']),
            '17': ('<ARGUMENTACAO>', ['<VARIAVEL>']),
            '18': ('<STRING>', ['string']),
            '19': ('<NUMERO>', ['numero']),
            '20': ('<VARIAVEL>', ['id']),
            '21': ('<TIPO>', ['tiponum']),
            '22': ('<TIPO>', 'î'),
            '23': ('<DECLARACAO>', ['<TIPO>', 'id', '<ATRIBUICAO>']),
            '24': ('<ATRIBUICAO>', ['atribuicao', '<CALCULO>']),
            '25': ('<ATRIBUICAO>', 'î'),
            '26': ('<OPERANDO>', ['<NUMERO>']),
            '27': ('<OPERANDO>', ['<VARIAVEL>']),
            '28': ('<CALCULO>', ['<OPERANDO>', '<EXPRESSAO>']),
            '29': ('<CALCULO>', ['parenteses_abre', '<CALCULO>', 'parenteses_fecha', '<EXPRESSAO>']),
            '30': ('<EXPRESSAO>', ['<OPERADORES_MAT>', '<CALCULO>']),
            '31': ('<EXPRESSAO>', 'î'),
            '32': ('<LOGICO>', ['parenteses_abre', '<EXPRESSAO_LOGICA>', 'parenteses_fecha']),
            '33': ('<EXPRESSAO_LOGICA>', ['<CALCULO>', '<OPERADORES_LOGICOS>', '<CALCULO>']),
            '34': ('<SENAO>', ['senao', 'chaves_abre', '<LISTA_COMANDOS>', 'chaves_fecha']),
            '35': ('<SENAO>', 'î')
        }

        if key in producoes:
            return producoes[key]

    def getTokens(self): # Função apenas pra abrir a lista de tokens e retornar todos os tokens da lista
        with open(self.tokens) as arquivo:

            linhas = arquivo.readlines()
            tokens = []

            for l in linhas:
                linha = l.split('|')
                tokens.append(linha)
            return tokens

    def analise(self):

        # Declaração da pilha empilhando o cifrão e o primeiro não terminal

        pilha, filaTokens = [], []

        pilha.append('$')
        pilha.append('<FORMATO_PROGRAMA>')

        fila = self.getTokens()

        for elemento in fila:
            filaTokens.append(elemento[1])
        filaTokens.append('$')

        i = 0

        while True:
            topoPilha = pilha[-1]  # Topo da pilha
            chave = self.getProducaoChave(topoPilha, filaTokens[i])  # Passa o topo da filha e o token atual pra retornar a produção a ser verificada
            if chave != '-':
                producao = self.getProducao(chave)  # Se a chave for diferente do '-', é retornado uma produção a ser verificada
                if producao:
                    self.log.append(f'Desempilhando: {pilha.pop()}')
                    listaProducao = list(reversed(producao[1]))  # Inverte a lista de produção
                    for t in listaProducao:  # Percorro a lista retornada e empilho os valores dentro da pilha
                        pilha.append(t)
                        self.log.append(f'Empilhando: {t}')
                else:
                    if topoPilha == filaTokens[i]:
                        if topoPilha == '$' and filaTokens[i] == '$':
                            self.log.append('A análise foi finalizada e não retornou nenhum erro sintático!')
                            break
                        else:
                            self.log.append(f'Desempilhando: {pilha.pop()}')
                            i += 1  # Movimenta na lista de tokens pro próximo a ser verificado
                    elif topoPilha == 'î':
                        self.log.append(f'Desempilhando: {pilha.pop()}')
                    else:
                        self.log.append(f'Erro sintático: Token {fila[i][0]} inesperado na linha: {fila[i][2]}, coluna: {fila[i][3].strip()}')
                        self.log_erros.append(f'Erro sintático: Token {fila[i][0]} inesperado na linha: {fila[i][2]}, coluna: {fila[i][3].strip()}')
                        self.erros = True
                        break
            else:
                self.log.append(f'Erro sintático: Token {fila[i][0]} inesperado na linha: {fila[i][2]}, coluna: {fila[i][3].strip()}')
                self.log_erros.append(f'Erro sintático: Token {fila[i][0]} inesperado na linha: {fila[i][2]}, coluna: {fila[i][3].strip()}')
                self.erros = True
                break

    def mostraLog(self):
        print('Empilhando: $')
        print('Empilhando: <FORMATO_PROGRAMA>')
        for i in self.log:
            print(i)

    def mostraErros(self):
        for i in self.log_erros:
            print(i)

    def retornaErros(self):
        return self.erros