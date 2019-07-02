class analiseLexica:

    codigo, listatokens, lt_file, atual, transicao, erros = [], [], [], None, None, 0

    final = {
        'q3': 'tk_inicio',
        'q7': 'tk_fim',
        'q28': 'senao',
        'q9': 'se',
        'q15': 'tiponum',
        'q18': 'ler',
        'q25': 'escrever',
        'q33': 'enquanto',
        'q34': 'subtracao',
        'q35': 'adicao',
        'q36': 'mult',
        'q37': 'divisao',
        'q39': 'menorigual',
        'q41': 'maiorigual',
        'q42': 'atribuicao',
        'q43': 'igual',
        'q44': 'parenteses_abre',
        'q45': 'parenteses_fecha',
        'q46': 'chaves_abre',
        'q47': 'chaves_fecha',
        'q50': 'string',
        'q51': 'numero',
        'q52': 'id',
        'q53': 'fim_linha',
        'q54': 'espaco ou tabulacao'
    }

    def __init__(self, texto, atual = "q0", transicao = "transicao.txt"):
        self.codigo = texto
        self.atual = atual
        self.transicao = transicao

    def textoParaLista(self):
        with open(f'codigos/{self.codigo}', 'r') as programa:  # Abertura do arquivo que contém o código
            arquivo = programa.readlines()
        return arquivo

    def ftransicao(self, s, l):
        with open(f'tokens/{self.transicao}', 'r') as transicao:  # Abertura do arquivo que contém a tabela de transição da gramática
            linhas = transicao.readlines()

        for v in linhas:  # Navega pelas linhas do arquivo de transição
            linha = v.split(',')  # Divide a string em 3 partes (estado atual, letra, próximo estado)
            if linha[0] == s:  # Se o primeiro valor da string dividida for igual o estado atual
                for z in linha[1]:  # É navegado apenas pelos valores das letras da função transição
                    if z == l:  # Se a letra lida no arquivo for igual a letra lida da palavra então é retornado o próximo estado
                        return linha[2].strip()
        return None

    def analise(self):

        arquivo, linha, lexema = self.textoParaLista(), 1, ''

        for lines in arquivo:
            line = lines

            for i in range(len(line)):
                if line[i] != '\n':

                    self.atual = self.ftransicao(self.atual, line[i])
                    lexema += line[i]
                    if lexema == 'run':
                        if len(line) == 3 or self.ftransicao(self.atual, line[i + 1]) is None:
                            self.atual = 'q3'
                    elif lexema == 'exit':
                        if len(line) == 4 or self.ftransicao(self.atual, line[i + 1]) is None:
                            self.atual = 'q7'
                    elif lexema == 'else':
                        if len(line) == 4 or self.ftransicao(self.atual, line[i + 1]) is None:
                            self.atual = 'q28'
                    elif lexema == 'if':
                        if len(line) == 2 or self.ftransicao(self.atual, line[i + 1]) is None:
                            self.atual = 'q9'
                    elif lexema == 'integer':
                        if len(line) == 7 or self.ftransicao(self.atual, line[i + 1]) is None:
                            self.atual = 'q15'
                    elif lexema == 'input':
                        if len(line) == 5 or self.ftransicao(self.atual, line[i + 1]) is None:
                            self.atual = 'q18'
                    elif lexema == 'display':
                        if len(line) == 7 or self.ftransicao(self.atual, line[i + 1]) is None:
                            self.atual = 'q25'
                    elif lexema == 'while':
                        if len(line) == 5 or self.ftransicao(self.atual, line[i + 1]) is None:
                            self.atual = 'q33'
                    elif self.atual == 'q40' or self.atual == 'q38':  # Verifica se após < ou > tem algum retorno, caso não tenha ele segue adiante
                        if self.ftransicao(self.atual, line[i + 1]) is None:
                            print(f'Lexema: [ {lexema} ] | Linha: {linha} | Coluna: {i + 1} -> Erro léxico!')
                            self.atual = 'q0'
                            lexema = ''
                            self.erros += 1

                    # Se o estado atual é uma chave no dicionário, logo chegou no estado final

                    if self.atual in self.final.keys():
                        if self.atual == 'q51' and i + 1 < len(line):  # Numeral
                            if self.ftransicao(self.atual, line[i + 1]) is not None:
                                self.atual = 'q51'
                                continue
                            else:
                                self.listatokens.append(f'Lexema: {lexema} | Token: {self.final[self.atual]} | Linha: {linha} | Coluna: {i + 1}')
                                self.lt_file.append(f'{lexema}|{self.final[self.atual]}|{linha}|{i + 1}\n')
                                self.atual = 'q0'
                                lexema = ''
                                continue
                        elif self.atual == 'q42' and i + 1 < len(line):  # Atribuição e igualdade
                            if self.ftransicao(self.atual, line[i + 1]) is not None:
                                self.atual = 'q42'
                                continue
                            else:
                                self.listatokens.append(f'Lexema: {lexema} | Token: {self.final[self.atual]} | Linha: {linha} | Coluna: {i + 1}')
                                self.lt_file.append(f'{lexema}|{self.final[self.atual]}|{linha}|{i + 1}\n')
                                self.atual = 'q0'
                                lexema = ''
                                continue
                        elif self.atual == 'q52' and i + 1 < len(line):  # Identificador
                            if self.ftransicao(self.atual, line[i + 1]) is not None:
                                self.atual = 'q52'
                                continue
                            else:
                                self.listatokens.append(f'Lexema: {lexema} | Token: {self.final[self.atual]} | Linha: {linha} | Coluna: {i + 1}')
                                self.lt_file.append(f'{lexema}|{self.final[self.atual]}|{linha}|{i + 1}\n')
                                self.atual = 'q0'
                                lexema = ''
                                continue
                        elif self.atual == 'q54':  # Espaços e tabulações. Só ignora e segue o programa
                            self.atual = 'q0'
                            lexema = ''
                            continue
                        else:  # Caso não seja nenhum dos casos acima, mas esteja no estado final, ele retorna o token correspondido
                            self.listatokens.append(f'Lexema: {lexema} | Token: {self.final[self.atual]} | Linha: {linha} | Coluna: {i + 1}')
                            self.lt_file.append(f'{lexema}|{self.final[self.atual]}|{linha}|{i + 1}\n')
                            self.atual = 'q0'
                            lexema = ''
                            continue
                    elif self.atual is None:  # Caso não esteja no estado final e retornar None, é retornado um erro Léxico
                        print(f'Lexema: [ {lexema} ] | Linha: {linha} | Coluna: {i + 1} -> Erro léxico!')
                        self.atual = 'q0'
                        lexema = ''
                        self.erros += 1
                        continue
            linha += 1

    def mostraTokens(self):
        for i in self.listatokens:
            print(i)

    def retornaErros(self):
        return self.erros

    def salva(self, nome):
        with open(f'{nome}', "w") as lt:  # Armazena os tokens reconhecidos dentro de um .txt
            lt.writelines(self.lt_file)


