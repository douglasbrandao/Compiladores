from analysis.lexical import Lexical
from analysis.syntactic import Syntactic
from analysis.semantic import Semantic
from code_generation.intermediate import Intermediate
from code_generation.final import Final
import argparse
import os

parser = argparse.ArgumentParser(description='Etapas de um Analisador de Compiladores')
parser.add_argument('code', type=str)
parser.add_argument('-lt', '--ltokens', action='store_true', help='Retorna a listagem dos tokens')
parser.add_argument('-ls', '--lsyntactic', action='store_true', help='Retorna o log da análise sintática')
parser.add_argument('-lse', '--lsemantic', action='store_true', help='Retorna o log da análise semântica')
parser.add_argument('-lgc', '--lgencode', action='store_true', help='Retorna o log da geração de código')
parser.add_argument('-tudo', '--tudo', action='store_true', help='Retorna todas as etapas da análise')
args = parser.parse_args()

if __name__ == '__main__':

    if not (args.ltokens and args.lsyntactic and args.lsemantic and args.tudo and args.lgencode):
        print('You must provide an argument. Use -h to see the options.')

    if args.ltokens or args.tudo:
        try:
            print('*' * 20 + ' LISTAGEM DOS TOKENS ' + '*' * 20, end='\n\n')
            lexical = Lexical(args.code)
            lexical.analysis()
            lexical.show_tokens()
            lexical.save('list_tk.txt')
        except IOError:
            print(f'The {args.code} argument doesn\'t exist!')

    if args.lsyntactic or args.tudo:
        try:
            print('\n\n')
            print('*' * 20 + ' LOG SINTÁTICO ' + '*' * 20, end='\n\n')
            syntactic = Syntactic('tabela_sintatica.csv', 'list_tk.txt')
            syntactic.analysis()
            syntactic.show()
        except IOError:
            if not(os.path.isfile('./list_tk.txt')):
                print('O arquivo list_tk.txt não existe. Faça a análise léxica!')

    if args.lsemantic or args.tudo:
        try:
            print('\n\n')
            print('*' * 20 + ' LOG SEMÂNTICO ' + '*' * 20, end='\n\n')
            semantic = Semantic('list_tk.txt')
            semantic.analysis()
            semantic.show()
        except IOError:
            if not (os.path.isfile('./list_tk.txt')):
                print('O arquivo list_tk.txt não existe. Faça a análise léxica!')

    if args.lgencode or args.tudo:
        try:
            print('\n\n')
            print('*' * 20 + ' LOG GERAÇÃO DE CÓDIGO INTERMEDIÁRIO ' +
                  '*' * 20, end='\n\n')
            intermediate = Intermediate('list_tk.txt')
            intermediate.generation()
            intermediate.show()
            intermediate.save()
            print('\n\n')
            print('*' * 20 + ' LOG GERAÇÃO DE CÓDIGO FINAL ' + '*' * 20, end='\n\n')
            final = Final('intermediario.itm')
            final.generation()
            final.show()
            final.save()
        except IOError:
            if not (os.path.isfile('./list_tk.txt')):
                print('O arquivo list_tk.txt não existe. Faça a análise léxica!')
