from analysis.utils.final_states import final_states_dict


class Lexical:

    def __init__(self, code, transition_file="list.txt"):
        self.log = []
        self.code = code
        self.errors = 0
        self.transitions = transition_file

    def code_lines_to_list(self):
        with open(f'examples/{self.code}', 'r') as code:
            return code.readlines()

    def transition_function(self, current_state, current_token):
        with open(f'transitions/{self.transitions}', 'r') as transitions:
            transition_list = [line for line in transitions.readlines() if line.strip()]

        for transition in transition_list:
            state, tokens, next_state = transition.split(',')

            if state == current_state:
                for token in tokens:
                    if token == current_token:
                        return next_state.strip()

    def analysis(self):

        code_lines = self.code_lines_to_list()
        lexeme = ''
        number_lines = 1
        current_state = 'q0'
        final_states = final_states_dict  # imported from final_states module

        for line in code_lines:
            for column in range(len(line)):

                if line[column] != '\n':
                    current_state = self.transition_function(current_state, line[column])
                    lexeme += line[column]

                    if lexeme == 'run':
                        if len(line) == 3 or not self.transition_function(current_state, line[column+1]):
                            current_state = 'q3'
                    elif lexeme == 'exit':
                        if len(line) == 4 or not self.transition_function(current_state, line[column+1]):
                            current_state = 'q7'
                    elif lexeme == 'else':
                        if len(line) == 4 or not self.transition_function(current_state, line[column+1]):
                            current_state = 'q28'
                    elif lexeme == 'if':
                        if len(line) == 2 or not self.transition_function(current_state, line[column+1]):
                            current_state = 'q9'
                    elif lexeme == 'integer':
                        if len(line) == 7 or not self.transition_function(current_state, line[column+1]):
                            current_state = 'q15'
                    elif lexeme == 'input':
                        if len(line) == 5 or not self.transition_function(current_state, line[column+1]):
                            current_state = 'q18'
                    elif lexeme == 'display':
                        if len(line) == 7 or not self.transition_function(current_state, line[column+1]):
                            current_state = 'q25'
                    elif lexeme == 'while':
                        if len(line) == 5 or not self.transition_function(current_state, line[column+1]):
                            current_state = 'q33'

                    '''
                    Se o estado atual é uma chave no dicionário então
                    ele é um estado final, agora é só verificar para
                    qual ele corresponde
                    '''

                    if current_state in final_states.keys():

                        token_information = f'{lexeme}|{final_states[current_state]}|{number_lines}|{column+1}'

                        # Numeral
                        if current_state == 'q51' and column+1 < len(line):
                            if self.transition_function(current_state, line[column+1]):
                                current_state = 'q51'
                            else:
                                self.log.append(token_information)
                                current_state = 'q0'
                                lexeme = ''
                        # Atribuição e igualdade
                        elif current_state == 'q42' and column+1 < len(line):
                            if self.transition_function(current_state, line[column+1]):
                                current_state = 'q42'
                            else:
                                self.log.append(token_information)
                                current_state = 'q0'
                                lexeme = ''
                        # Identificador
                        elif current_state == 'q52' and column + 1 < len(line):
                            if self.transition_function(current_state, line[column+1]):
                                current_state = 'q52'
                            else:
                                self.log.append(token_information)
                                current_state = 'q0'
                                lexeme = ''
                        elif current_state == 'q54':  # Espaços e tabulações. Só ignora e segue o programa
                            current_state = 'q0'
                            lexeme = ''
                        # Verifica se após < ou > tem algum retorno, caso não tenha ele segue adiante
                        elif current_state == 'q40' and column+1 < len(line):
                            if self.transition_function(current_state, line[column+1]):
                                current_state = 'q40'
                            else:
                                self.log.append(token_information)
                                current_state = 'q0'
                                lexeme = ''
                        elif current_state == 'q38' and column+1 < len(line):
                            if self.transition_function(current_state, line[column+1]):
                                current_state = 'q38'
                            else:
                                self.log.append(token_information)
                                current_state = 'q0'
                                lexeme = ''
                        else:
                            self.log.append(token_information)
                            current_state = 'q0'
                            lexeme = ''
                    # Caso não exista nos estados finais, então não é um token válido
                    elif not current_state:
                        print(f'LEXICAL ERROR -> This symbol {lexeme} at {number_lines}|{column+1} doesn\'t exist')
                        current_state = 'q0'
                        self.errors += 1
                        lexeme = ''
            number_lines += 1

    def show_tokens(self):
        if not self.errors:
            for token in self.log:
                print(token)

    def get_errors(self):
        return self.errors

    def save(self, name):
        with open(f'{name}', "w") as tokens:
            tokens.write('\n'.join(self.log))
