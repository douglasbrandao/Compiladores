from csv import DictReader
from analysis.utils.production_list import production_list


class Syntactic:

    def __init__(self, table, lexical):
        self.logs = []
        self.table = table
        self.error = ''
        self.tokens = lexical.get_tokens()

    def get_production_key(self, top, token):
        with open(f'syntactic_table/{self.table}') as syntactic_table:
            table = DictReader(syntactic_table)
            for cell in table:
                if cell['NAO-TERMINAIS'] == top:
                    return cell[token]

    def get_production(self, key):
        productions = production_list
        if key in productions:
            return productions[key]

    def analysis(self):

        index = 0
        stack = ['$', '<FORMATO_PROGRAMA>']

        queue = [token.split('|') for token in self.tokens]
        tokens_queue = [token[1] for token in queue]
        tokens_queue.append('$')

        while True:
            top_of_stack = stack[-1]
            production_key = self.get_production_key(top_of_stack, tokens_queue[index])

            if production_key != '-':
                production = self.get_production(production_key)

                if production:
                    self.logs.append(f'Popping: {stack.pop()}')
                    production_list_reversed = list(reversed(production[1]))

                    for production in production_list_reversed:
                        stack.append(production)
                        self.logs.append(f'Pushing: {production}')
                else:
                    if top_of_stack == tokens_queue[index]:

                        if top_of_stack == '$' and tokens_queue[index] == '$':
                            self.logs.append('Syntactic analysis finished without any errors.')
                            break
                        else:
                            self.logs.append(f'Popping: {stack.pop()}')
                            index += 1
                    elif top_of_stack == 'î':
                        self.logs.append(f'Popping: {stack.pop()}')
                    else:
                        self.error = f'ERROR -> {queue[index-1][0]}|{queue[index-1][2]}|{queue[index-1][3].strip()}'
                        break
            else:
                if index == len(queue):
                    self.error = f'ERROR -> {queue[index-1][0]}|{queue[index-2][2]}|{queue[index-1][3].strip()}'
                else:
                    self.error = f'ERROR -> {queue[index-1][0]}|{queue[index-1][2]}|{queue[index-1][3].strip()}'
                break

    def show(self):
        if self.error:
            print(self.error)
        else:
            print('Pushing: $')
            print('Pushing: <FORMATO_PROGRAMA>')
            for log in self.logs:
                print(log)
