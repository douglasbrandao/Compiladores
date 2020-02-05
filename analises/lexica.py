from analises.utils.mensagens.mensagensLexico import msgErroLexico, msgLog, token
from analises.utils.estruturas.estadosFinais import estados_finais


class analiseLexica:

    def __init__(self, texto, atual="q0", transicao="transicao.txt"):
        self.codigo = texto
        self.atual = atual
        self.transicao = transicao
        self.log = []
        self.erros = 0
        self.tokens = []
        self.final = estados_finais

    def linhasCodigoParaLista(self):
        with open(f'codigos/{self.codigo}', 'r') as codigo:
            lista = codigo.readlines()
        return lista

    def ftransicao(self, estado_atual, letra_palavra):
        with open(f'transicoes/{self.transicao}', 'r') as transicao:
            linhas = transicao.readlines()

        for linha in linhas:
            linha_split = linha.split(',')
            if linha_split[0] == estado_atual:
                for token in linha_split[1]:
                    if token == letra_palavra:
                        return linha_split[2].strip()

        return None

    def analise(self):

        arquivo = self.linhasCodigoParaLista()
        linha_cont = 1
        lexema = ''

        for linhas in arquivo:
            linha = linhas

            for coluna in range(len(linha)):
                if linha[coluna] != '\n':

                    self.atual = self.ftransicao(self.atual, linha[coluna])
                    lexema += linha[coluna]

                    if lexema == 'run':
                        if len(linha) == 3 or self.ftransicao(self.atual, linha[coluna+1]) is None:
                            self.atual = 'q3'
                    elif lexema == 'exit':
                        if len(linha) == 4 or self.ftransicao(self.atual, linha[coluna+1]) is None:
                            self.atual = 'q7'
                    elif lexema == 'else':
                        if len(linha) == 4 or self.ftransicao(self.atual, linha[coluna+1]) is None:
                            self.atual = 'q28'
                    elif lexema == 'if':
                        if len(linha) == 2 or self.ftransicao(self.atual, linha[coluna+1]) is None:
                            self.atual = 'q9'
                    elif lexema == 'integer':
                        if len(linha) == 7 or self.ftransicao(self.atual, linha[coluna+1]) is None:
                            self.atual = 'q15'
                    elif lexema == 'input':
                        if len(linha) == 5 or self.ftransicao(self.atual, linha[coluna+1]) is None:
                            self.atual = 'q18'
                    elif lexema == 'display':
                        if len(linha) == 7 or self.ftransicao(self.atual, linha[coluna+1]) is None:
                            self.atual = 'q25'
                    elif lexema == 'while':
                        if len(linha) == 5 or self.ftransicao(self.atual, linha[coluna+1]) is None:
                            self.atual = 'q33'
                    # Verifica se após < ou > tem algum retorno, caso não tenha ele segue adiante
                    elif self.atual == 'q40' or self.atual == 'q38':
                        if self.ftransicao(self.atual, linha[coluna+1]) is None:
                            print(msgErroLexico(lexema, linha_cont, coluna))
                            self.atual = 'q0'
                            lexema = ''
                            self.erros += 1

                    # Se o estado atual é uma chave no dicionário, logo chegou no estado final
                    if self.atual in self.final.keys():
                        # Numeral
                        if self.atual == 'q51' and coluna+1 < len(linha):
                            if self.ftransicao(self.atual, linha[coluna+1]) is not None:
                                self.atual = 'q51'
                            else:
                                self.log.append(
                                    msgLog(lexema, self.final, self.atual, linha_cont, coluna))
                                self.tokens.append(
                                    token(lexema, self.final, self.atual, linha_cont, coluna))
                                self.atual = 'q0'
                                lexema = ''
                        # Atribuição e igualdade
                        elif self.atual == 'q42' and coluna+1 < len(linha):
                            if self.ftransicao(self.atual, linha[coluna+1]) is not None:
                                self.atual = 'q42'
                            else:
                                self.log.append(
                                    msgLog(lexema, self.final, self.atual, linha_cont, coluna))
                                self.tokens.append(
                                    token(lexema, self.final, self.atual, linha_cont, coluna))
                                self.atual = 'q0'
                                lexema = ''
                        # Identificador
                        elif self.atual == 'q52' and coluna + 1 < len(linha):
                            if self.ftransicao(self.atual, linha[coluna+1]) is not None:
                                self.atual = 'q52'
                            else:
                                self.log.append(
                                    msgLog(lexema, self.final, self.atual, linha_cont, coluna))
                                self.tokens.append(
                                    token(lexema, self.final, self.atual, linha_cont, coluna))
                                self.atual = 'q0'
                                lexema = ''
                        elif self.atual == 'q54':  # Espaços e tabulações. Só ignora e segue o programa
                            self.atual = 'q0'
                            lexema = ''
                        # Caso não seja nenhum dos casos acima, mas esteja no estado final
                        else:
                            self.log.append(
                                msgLog(lexema, self.final, self.atual, linha_cont, coluna))
                            self.tokens.append(
                                token(lexema, self.final, self.atual, linha_cont, coluna))
                            self.atual = 'q0'
                            lexema = ''
                    elif self.atual is None:  # Caso não esteja no estado final e retornar None
                        print(msgErroLexico(lexema, linha_cont, coluna))
                        self.atual = 'q0'
                        lexema = ''
                        self.erros += 1
            linha_cont += 1

    def mostraTokens(self):
        [print(token) for token in self.log]

    def retornaErros(self):
        return self.erros

    def salva(self, nome):
        with open(f'{nome}', "w") as lista:
            lista.writelines(self.tokens)
