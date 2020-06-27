class Semantic:

    def __init__(self, lexical):
        self.tokens = lexical.get_tokens()
        self.log = []

    def analysis(self):

        c = 0
        variables = variables_assigned_with_zero = []
        tokens = self.tokens

        for index, token in enumerate(tokens):
            lexeme, token, line, column = token.split('|')

            if index < len(tokens)-1:
                previous_lexeme, previous_token, *_ = tokens[c-1].split('|')
                next_lexeme, next_token, *_ = tokens[c+1].split('|')

            if token == 'id':
                if previous_lexeme == 'integer':

                    if lexeme in variables:
                        self.log.append(f'This variable {lexeme} was already declared once at {line}|{column}')
                    else:
                        variables.append(lexeme)

                if next_token == 'atribuicao':
                    lexeme_after_assign_operator = tokens[c+2].split('|')[0]

                    if lexeme_after_assign_operator == '0':
                        variables_assigned_with_zero.append(lexeme)

                if previous_token != 'tiponum':
                    if lexeme not in variables:
                        self.log.append(f'You must declare this variable {lexeme}')

            if token == 'divisao':
                if next_lexeme == '0':
                    self.log.append(f'A division by zero ocurred at {line}|{column}')
                elif next_token == 'id' and next_lexeme in variables_assigned_with_zero:
                    self.log.append(f'A division by zero ocurred at {line}|{column}')
            c += 1

    def show(self):
        if not self.log:
            print('Semantic analysis is finished without any errors.')
        else:
            for log in self.log:
                print(log)
