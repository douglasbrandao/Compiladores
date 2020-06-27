import os
import argparse
from analysis.lexical import Lexical
from analysis.syntactic import Syntactic
from analysis.semantic import Semantic
from generation.intermediate import Intermediate
from generation.final import Final

parser = argparse.ArgumentParser(description='Etapas de um Analisador de Compiladores')
parser.add_argument('code', type=str)
parser.add_argument('-lt', '--ltokens', action='store_true', help='show token list')
parser.add_argument('-ls', '--lsyntactic', action='store_true', help='show syntactic analysis')
parser.add_argument('-lse', '--lsemantic', action='store_true', help='show semantic analysis')
parser.add_argument('-lgc', '--lgencode', action='store_true', help='generate the intermediate and final code')
parser.add_argument('-tudo', '--tudo', action='store_true', help='do all the steps')
args = parser.parse_args()

if __name__ == '__main__':

    if not (args.ltokens or args.lsyntactic or args.lsemantic or args.tudo or args.lgencode):
        print('You must provide an argument. Use -h to see the options.')

    lexical = Lexical(args.code)
    lexical.analysis()

    if args.ltokens or args.tudo:
        print('\n')
        print('*' * 20 + ' LEXICAL ANALYSIS ' + '*' * 20)
        print('\n')
        lexical.show()
        print('\n')

    if args.lsyntactic or args.tudo:
        print('\n')
        print('*' * 20 + ' SYNTACTIC ANALYSIS ' + '*' * 20)
        print('\n')
        syntactic = Syntactic('tabela_sintatica.csv', lexical)
        syntactic.analysis()
        syntactic.show()
        print('\n')

    if args.lsemantic or args.tudo:
        print('\n')
        print('*' * 20 + ' SEMANTIC ANALYSIS ' + '*' * 20)
        print('\n')
        semantic = Semantic(lexical)
        semantic.analysis()
        semantic.show()
        print('\n')

    if args.lgencode or args.tudo:
        print('\n')
        print('*' * 20 + ' INTERMEDIATE CODE GENERATION ' + '*' * 20)
        print('\n')
        intermediate = Intermediate(lexical)
        intermediate.generation()
        intermediate.show()
        print('\n')
        print('*' * 20 + ' FINAL CODE GENERATION ' + '*' * 20)
        print('\n')
        final = Final(intermediate)
        final.generation()
        final.show()
        file_name = input('What name do you want to save your output file? ')
        final.save(file_name)
        print('Saved in output folder!')
