class Final:

    def __init__(self, intermediate):
        self.intermediate = intermediate
        self.final = []

    def generate_final(self, intermediate):
        i = 0
        string_value = 0
        variables = []

        main = ['.text', '.global main', '\nmain:\n', '\tpush {ip, lr}\n']
        data = ['.data\n']

        while i < len(intermediate):

            if "ESCREVA" in intermediate[i]:
                string = intermediate[i].replace('ESCREVA ', '').rstrip('\n')
                if '"' in string:  # escrita de string
                    data.append('.balign 4')
                    data.append(f'\tstr{string}: .asciz {string_value}')
                    main.append(f'\tldr r0, =str{string_value}')
                    main.append('\tbl printf\n')
                    string_value += 1
                else:  # escrita de variável
                    main.append('\tldr r0, =pattern')
                    main.append('\tldr r1, [r2]')
                    main.append('\tbl printf\n')
            elif "LEIA" in intermediate[i]:  # leitura de variável
                variavel = intermediate[i].replace('LEIA ', '').rstrip('\n')
                main.append('\tldr r0, =pattern')
                main.append(f'\tldr r1, ={variavel}')
                main.append('\tbl scanf\n')
            elif "INTEIRO" in intermediate[i]:  # declaração de variável
                inteiro = intermediate[i].replace('INTEIRO ', '').rstrip('\n')
                data.append(f'\t.balign 4')
                data.append(f'\t{inteiro}: .word 0\n')
                variables.append(inteiro)
            elif ":=" in intermediate[i]:
                # Condição para variáveis temporárias
                if not intermediate[i].split()[0].strip() in variables:
                    data.append(f'{intermediate[i].split()[0].strip()}: .word 0')
                    variables.append(intermediate[i].split()[0].strip())

                # Como toda variável é declarada no data quando coloco um inteiro antes, caso atribua um valor pra ela após ele verifica na lista e substitui
                if len(intermediate[i].split()) == 3:
                    for n, j in enumerate(data):
                        if intermediate[i].split()[0] in j:
                            data[n] = f'{intermediate[i].split()[0]}: .word {intermediate[i].split()[2]}'

                if '+' in intermediate[i]:  # Instruções para a soma
                    # Se for decimal, ele move direto para o registrador
                    if intermediate[i].split()[2].isdecimal():
                        main.append(f'\tmov r1, #{intermediate[i].split()[2]}')
                    else:  # Se não, ele carrega o valor e depois insere no registrador
                        main.append(f'\tldr r1, ={intermediate[i].split()[2]}')
                        main.append('\tldr r1, [r1]')
                    # Se for decimal, ele move direto para o registrador
                    if intermediate[i].split()[4].isdecimal():
                        main.append(f'\tmov r2, #{intermediate[i].split()[4]}')
                    else:  # Se não, ele carrega o valor e depois insere no registrador
                        main.append(f'\tldr r2, ={intermediate[i].split()[4]}')
                        main.append('\tldr r2, [r2]')
                    main.append('\tadd r1, r1, r2')
                    main.append(f'\tldr r2, ={intermediate[i].split()[0]}')
                    main.append('\tstr r1, [r2]\n')
                elif '-' in intermediate[i]:  # Instruções para subtração
                    if intermediate[i].split()[2].isdecimal():
                        main.append(f'\tmov r1, #{intermediate[i].split()[2]}')
                    else:
                        main.append(f'\tldr r1, ={intermediate[i].split()[2]}')
                        main.append('\tldr r1, [r1]')
                    if intermediate[i].split()[4].isdecimal():
                        main.append(f'\tmov r2, #{intermediate[i].split()[4]}')
                    else:
                        main.append(f'\tldr r2, ={intermediate[i].split()[4]}')
                        main.append('\tldr r2, [r2]')
                    main.append('\tsub r1, r1, r2')
                    main.append(f'\tldr r2, ={intermediate[i].split()[0]}')
                    main.append('\tstr r1, [r2]\n')
                elif '*' in intermediate[i]:  # Instruções para multiplicação
                    if intermediate[i].split()[2].isdecimal():
                        main.append(f'\tmov r1, #{intermediate[i].split()[2]}')
                    else:
                        main.append(f'\tldr r1, ={intermediate[i].split()[2]}')
                        main.append('\tldr r1, [r1]')
                    if intermediate[i].split()[4].isdecimal():
                        main.append(f'\tmov r2, #{intermediate[i].split()[4]}')
                    else:
                        main.append(f'\tldr r2, ={intermediate[i].split()[4]}')
                        main.append('\tldr r2, [r2]')
                    main.append('\tmul r1, r1, r2')
                    main.append(f'\tldr r2, ={intermediate[i].split()[0]}')
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

    def generation(self):
        with open(self.intermediate, 'r') as intermediate_list:
            intermediate = intermediate_list.readlines()
            self.final = self.generate_final(intermediate)

    def save(self):
        with open('codigo.s', 'w') as file:
            file.write('\n'.join(self.final))

    def show(self):
        for code in self.final:
            print(code)
