class Final:

    geracao_final = []

    def __init__(self, ger_intermediario):
        self.codigo = ger_intermediario

    def data(self, message, string, value, var): # função para definir os addresses e o data
        dt = []
        if value == 1: # message: .ascii some
            dt.append(f'{message}: .ascii {string}')
        elif value == 2: # message: .balign 4 .word some
            dt.append('.balign 4')
            dt.append(f'{message}: .word {var}')
        elif value == 3: # message: .balign 4 .asciz "some"
            dt.append('.balign 4')
            dt.append(f'{message}: .asciz {var}')
        elif value == 4: # message: .word some
            dt.append(f'{message}: .word {var}')
        return dt

    def start(self, cod, assembly):
        i, str = 0, 0
        dt, adr, variaveis = [], [], []
        func = False

        assembly.append('.text') # declaração de início do programa
        assembly.append('.global main')
        assembly.append('\nmain:\n')
        assembly.append('push {ip, lr}\n')

        while i < len(cod):

            if "ESCREVA" in cod[i]:
                string = cod[i].replace('ESCREVA ', '').rstrip('\n')
                if '"' in string: # escrita de string
                    assembly.append(f'ldr r0, =str{str}')
                    assembly.append('bl printf\n')
                    adr.extend(self.data(f'addr_str{str}', None, 4, f'str{str}'))
                    dt.extend(self.data(f'str{str}', None, 3, string))
                    str += 1
                else: # escrita de variável
                    assembly.append('ldr r0, =pattern')
                    assembly.append('ldr r1, [r2]')
                    assembly.append('bl printf\n')
            elif "LEIA" in cod[i]: # leitura de variável
                variavel = cod[i].replace('LEIA ', '').rstrip('\n')
                assembly.append('ldr r0, =pattern')
                assembly.append(f'ldr r1, ={variavel}')
                assembly.append('bl scanf\n')
            elif "INTEIRO" in cod[i]: # declaração de variável
                inteiro = cod[i].replace('INTEIRO ', '').rstrip('\n')
                dt.extend(self.data(f'{inteiro}', None, 4, 0))
                variaveis.append(inteiro)
            elif ":=" in cod[i]:
                if not cod[i].split()[0].strip() in variaveis: # Condição para variáveis temporárias
                    dt.extend(self.data(f'{cod[i].split()[0].strip()}', None, 4, 0))
                    variaveis.append(cod[i].split()[0].strip())

                if len(cod[i].split()) == 3: # Como toda variável é declarada no data quando coloco um inteiro antes, caso atribua um valor pra ela após ele verifica na lista e substitui
                    for n, j in enumerate(dt):
                        if cod[i].split()[0] in j:
                            dt[n] = f'{cod[i].split()[0]}: .word {cod[i].split()[2]}'

                if '+' in cod[i]: # Instruções para a soma
                    if cod[i].split()[2].isdecimal(): # Se for decimal, ele move direto para o registrador
                        assembly.append(f'mov r1, #{cod[i].split()[2]}')
                    else: # Se não, ele carrega o valor e depois insere no registrador
                        assembly.append(f'ldr r1, ={cod[i].split()[2]}')
                        assembly.append('ldr r1, [r1]')
                    if cod[i].split()[4].isdecimal(): # Se for decimal, ele move direto para o registrador
                        assembly.append(f'mov r2, #{cod[i].split()[4]}')
                    else: # Se não, ele carrega o valor e depois insere no registrador
                        assembly.append(f'ldr r2, ={cod[i].split()[4]}')
                        assembly.append('ldr r2, [r2]')
                    assembly.append('add r1, r1, r2')
                    assembly.append(f'ldr r2, ={cod[i].split()[0]}')
                    assembly.append('str r1, [r2]\n')
                elif '-' in cod[i]: # Instruções para subtração
                    if cod[i].split()[2].isdecimal():
                        assembly.append(f'mov r1, #{cod[i].split()[2]}')
                    else:
                        assembly.append(f'ldr r1, ={cod[i].split()[2]}')
                        assembly.append('ldr r1, [r1]')
                    if cod[i].split()[4].isdecimal():
                        assembly.append(f'mov r2, #{cod[i].split()[4]}')
                    else:
                        assembly.append(f'ldr r2, ={cod[i].split()[4]}')
                        assembly.append('ldr r2, [r2]')
                    assembly.append('sub r1, r1, r2')
                    assembly.append(f'ldr r2, ={cod[i].split()[0]}')
                    assembly.append('str r1, [r2]\n')
                elif '*' in cod[i]: # Instruções para multiplicação
                    if cod[i].split()[2].isdecimal():
                        assembly.append(f'mov r1, #{cod[i].split()[2]}')
                    else:
                        assembly.append(f'ldr r1, ={cod[i].split()[2]}')
                        assembly.append('ldr r1, [r1]')
                    if cod[i].split()[4].isdecimal():
                        assembly.append(f'mov r2, #{cod[i].split()[4]}')
                    else:
                        assembly.append(f'ldr r2, ={cod[i].split()[4]}')
                        assembly.append('ldr r2, [r2]')
                    assembly.append('mul r1, r1, r2')
                    assembly.append(f'ldr r2, ={cod[i].split()[0]}')
                    assembly.append('str r1, [r2]\n')
            elif "if" in cod[i]:
                linha = cod[i].split()
                if linha[2].isdecimal():
                    assembly.append(f'mov r1, #{linha[2]}')
                else:
                    assembly.append(f'ldr r1, ={linha[2]}')
                if linha[4].isdecimal():
                    assembly.append(f'mov r1, #{linha[4]}')
                else:
                    assembly.append(f'ldr r2, ={linha[4]}')
                assembly.append(f'cmp r1, r2')
                if linha[3] == '>':
                    assembly.append(f'bgt {linha[-1].strip()}')
                elif linha[3] == '<':
                    assembly.append(f'blt {linha[-1]}')
                elif linha[3] == '=':
                    assembly.append(f'beq {linha[-1]}')
            elif "_C" in cod[i]:
                assembly.append('pop {ip, pc}')
                assembly.append(cod[i].strip())
                func = True
            i += 1

        if func is False:
            assembly.append('pop {ip, pc}')

        assembly.append('\nend:')  # declaração final do programa
        assembly.append('mov r7, #1')
        assembly.append('swi 0\n')

        assembly.append('\n.extern printf')
        assembly.append('.extern scanf')
        assembly.append('\n')

        assembly.append('.data')
        assembly.extend(dt)
        assembly.extend(self.data(f'pattern', None, 3, '"%d"'))

        return assembly

    def geracao(self):

        codigo_assembly = []

        with open(self.codigo, 'r') as codigo:
            intermediario = codigo.readlines()

        self.geracao_final = self.start(intermediario, codigo_assembly)

    def salvarFinal(self):
        with open('codigo.s', 'w') as arq:
            arq.writelines('\n'.join(self.geracao_final))

    def mostrar(self):
        for codigo in self.geracao_final:
            print(codigo)



