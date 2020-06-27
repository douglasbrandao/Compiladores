from generation.utils.infix_to_postfix import infix_to_postfix
from generation.utils.tac import tac


class Intermediate:

    def __init__(self, lexical):
        self.tokens = lexical.get_tokens()
        self.log = []

    def check_operator(self, op):

        operators = {
            '<=': 'NGT',  # Not greather than
            '>=': 'NLT',  # Not less than
            '>': 'GT',  # Greather than
            '<': 'LT',  # Less than
            '==': 'EQL',  # Equal
            '!==': 'NEQL'  # Not equal
        }

        if op in operators:
            return operators[op]

    def check_expression(self, tokens, index):

        expression = []
        while tokens[index][1] != 'parenteses_fecha':
            expression.append(tokens[index][0])
            index += 1
        expression_to_string = ' '.join(expression)

        return expression_to_string.split()

    def check_assignment(self, variable, index, intermediate, tokens):

        expression = []
        while tokens[index][1] != 'fim_linha':
            expression.append(tokens[index][0])
            index += 1
        expression_to_string = ' '.join(expression)

        return tac(variable, infix_to_postfix(expression_to_string), intermediate, index)

    def generate_intermediate(self, tokens, index, loop, cond):

        if tokens[index][1] == 'ler':
            self.log.append(f'LEIA {tokens[index+2][0]}')
            index += 4
        elif tokens[index][1] == 'escrever':
            self.log.append(f'ESCREVA {tokens[index+2][0]}')
            index += 4
        elif tokens[index][1] == 'atribuicao':
            variable = tokens[index-1][0]
            self.check_assignment(variable, index+1, self.log, tokens)
        elif tokens[index][1] == 'enquanto':
            expression = self.check_expression(tokens, index+2)
            operator = self.check_operator(expression[1])
            loop_str = f'_L{loop}: if {expression[0]} {operator} {expression[2]} goto _L{loop + 1}'
            self.log.append(loop_str)
            index += 5
            while tokens[index][1] != 'chaves_fecha':
                index = self.generate_intermediate(tokens, index, loop+index, cond)
                index += 1
            self.log.append(f'_L{loop+1}:')
        elif tokens[index][1] == 'se':
            expression = self.check_expression(tokens, index+2)
            operator = self.check_operator(expression[1])
            cond_str = f'_C{cond}: if {expression[0]} {operator} {expression[2]} goto _C{cond + 1}'
            self.log.append(cond_str)
            index += 5
            while tokens[index][1] != 'chaves_fecha':
                index = self.generate_intermediate(tokens, index, loop, cond+index)
                index += 1
            self.log.append(f'_C{cond+1}:')
        return index

    def generation(self):

        loop = cond = index = 0
        tokens = [token.split('|') for token in self.tokens]

        for c, token in enumerate(tokens):
            if token[1] == 'id' and tokens[c-1][1] == 'tiponum':
                number_assigned = token[0]
                self.log.append(f'INTEIRO {number_assigned}')

        while index < len(tokens):
            index = self.generate_intermediate(tokens, index, loop, cond)
            index += 1
            cond += 1
            loop += 1

    def show(self):
        for code in self.log:
            print(code)

    def get_code(self):
        return self.log
