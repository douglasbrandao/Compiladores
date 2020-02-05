class Final:

    def __init__(self, ger_intermediario):
        self.codigo = ger_intermediario
        self.geracao_final = []

    def start(self, cod):
        i = 0
        string_valor = 0
        variaveis = []

        main = ['.text', '.global main', '\nmain:\n', '\tpush {ip, lr}\n']
        data = ['.data\n']

        while i < len(cod):

            if "ESCREVA" in cod[i]:
                string = cod[i].replace('ESCREVA ', '').rstrip('\n')
                if '"' in string:  # escrita de string
                    data.append('.balign 4')
                    data.append(f'\tstr{string}: .asciz {string_valor}')
                    main.append(f'\tldr r0, =str{string_valor}')
                    main.append('\tbl printf\n')
                    string_valor += 1
                else:  # escrita de variável
                    main.append('\tldr r0, =pattern')
                    main.append('\tldr r1, [r2]')
                    main.append('\tbl printf\n')
            elif "LEIA" in cod[i]:  # leitura de variável
                variavel = cod[i].replace('LEIA ', '').rstrip('\n')
                main.append('\tldr r0, =pattern')
                main.append(f'\tldr r1, ={variavel}')
                main.append('\tbl scanf\n')
            elif "INTEIRO" in cod[i]:  # declaração de variável
                inteiro = cod[i].replace('INTEIRO ', '').rstrip('\n')
                data.append(f'\t.balign 4')
                data.append(f'\t{inteiro}: .word 0\n')
                variaveis.append(inteiro)
            elif ":=" in cod[i]:
                # Condição para variáveis temporárias
                if not cod[i].split()[0].strip() in variaveis:
                    data.append(f'{cod[i].split()[0].strip()}: .word 0')
                    variaveis.append(cod[i].split()[0].strip())

                # Como toda variável é declarada no data quando coloco um inteiro antes, caso atribua um valor pra ela após ele verifica na lista e substitui
                if len(cod[i].split()) == 3:
                    for n, j in enumerate(data):
                        if cod[i].split()[0] in j:
                            data[n] = f'{cod[i].split()[0]}: .word {cod[i].split()[2]}'

                if '+' in cod[i]:  # Instruções para a soma
                    # Se for decimal, ele move direto para o registrador
                    if cod[i].split()[2].isdecimal():
                        main.append(f'\tmov r1, #{cod[i].split()[2]}')
                    else:  # Se não, ele carrega o valor e depois insere no registrador
                        main.append(f'\tldr r1, ={cod[i].split()[2]}')
                        main.append('\tldr r1, [r1]')
                    # Se for decimal, ele move direto para o registrador
                    if cod[i].split()[4].isdecimal():
                        main.append(f'\tmov r2, #{cod[i].split()[4]}')
                    else:  # Se não, ele carrega o valor e depois insere no registrador
                        main.append(f'\tldr r2, ={cod[i].split()[4]}')
                        main.append('\tldr r2, [r2]')
                    main.append('\tadd r1, r1, r2')
                    main.append(f'\tldr r2, ={cod[i].split()[0]}')
                    main.append('\tstr r1, [r2]\n')
                elif '-' in cod[i]:  # Instruções para subtração
                    if cod[i].split()[2].isdecimal():
                        main.append(f'\tmov r1, #{cod[i].split()[2]}')
                    else:
                        main.append(f'\tldr r1, ={cod[i].split()[2]}')
                        main.append('\tldr r1, [r1]')
                    if cod[i].split()[4].isdecimal():
                        main.append(f'\tmov r2, #{cod[i].split()[4]}')
                    else:
                        main.append(f'\tldr r2, ={cod[i].split()[4]}')
                        main.append('\tldr r2, [r2]')
                    main.append('\tsub r1, r1, r2')
                    main.append(f'\tldr r2, ={cod[i].split()[0]}')
                    main.append('\tstr r1, [r2]\n')
                elif '*' in cod[i]:  # Instruções para multiplicação
                    if cod[i].split()[2].isdecimal():
                        main.append(f'\tmov r1, #{cod[i].split()[2]}')
                    else:
                        main.append(f'\tldr r1, ={cod[i].split()[2]}')
                        main.append('\tldr r1, [r1]')
                    if cod[i].split()[4].isdecimal():
                        main.append(f'\tmov r2, #{cod[i].split()[4]}')
                    else:
                        main.append(f'\tldr r2, ={cod[i].split()[4]}')
                        main.append('\tldr r2, [r2]')
                    main.append('\tmul r1, r1, r2')
                    main.append(f'\tldr r2, ={cod[i].split()[0]}')
                    main.append('\tstr r1, [r2]\n')
            i += 1

        main.append('\tpop {ip, pc}\n')

        # syscall
        end = ['\nend:', '\tmov r7, #1', '\tswi 0\n']

        # bibliotecas C externas
        end.append('\n.extern printf')
        end.append('.extern scanf\n')

        # pattern para leitura de inteiros
        data.append('\t.balign 4')
        data.append('\tpattern: .asciz "%d"\n')

        return data + main + end

    def geracao(self):
        with open(self.codigo, 'r') as codigo:
            intermediario = codigo.readlines()
        self.geracao_final = self.start(intermediario)

    def salvarFinal(self):
        with open('codigo.s', 'w') as arq:
            arq.writelines('\n'.join(self.geracao_final))

    def mostrar(self):
        [print(codigo) for codigo in self.geracao_final]
