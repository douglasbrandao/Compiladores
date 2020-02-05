from analises.lexica import analiseLexica
from analises.sintatico import analiseSintatica
from analises.semantico import analiseSemantica
from geracao.intermediario import Intermediario
from geracao.final import Final
import argparse
import os

parser = argparse.ArgumentParser(
    description='Etapas de um Analisador de Compiladores')
parser.add_argument('code', type=str)
parser.add_argument('-lt', '--ltokens', action='store_true',
                    help='Retorna a listagem dos tokens')
parser.add_argument('-ls', '--lsyntactic', action='store_true',
                    help='Retorna o log da análise sintática')
parser.add_argument('-lse', '--lsemantic', action='store_true',
                    help='Retorna o log da análise semântica')
parser.add_argument('-lgc', '--lgencode', action='store_true',
                    help='Retorna o log da geração de código')
parser.add_argument('-tudo', '--tudo', action='store_true',
                    help='Retorna todas as etapas da análise')
args = parser.parse_args()

if __name__ == '__main__':

    if not args.ltokens and not args.lsyntactic and not args.lsemantic and not args.tudo and not args.lgencode:
        print(
            f'Não foi passado nenhum argumento. Adicione ao lado do seu {args.code} o -h para verificar as opções.')

    if args.ltokens or args.tudo:
        try:
            print('*' * 20 + ' LISTAGEM DOS TOKENS ' + '*' * 20, end='\n\n')
            lexica = analiseLexica(args.code)
            lexica.analise()
            lexica.mostraTokens()
            lexica.salva('list_tk.txt')
        except IOError:
            print(f'O parâmetro {args.code} informado não existe!')

    if args.lsyntactic or args.tudo:
        try:
            print('\n\n')
            print('*' * 20 + ' LOG SINTÁTICO ' + '*' * 20, end='\n\n')
            sintatico = analiseSintatica('tabela_sintatica.csv', 'list_tk.txt')
            sintatico.analise()
            sintatico.mostraLog()
        except IOError:
            if not(os.path.isfile('./list_tk.txt')):
                print('O arquivo list_tk.txt não existe. Faça a análise léxica!')

    if args.lsemantic or args.tudo:
        try:
            print('\n\n')
            print('*' * 20 + ' LOG SEMÂNTICO ' + '*' * 20, end='\n\n')
            semantico = analiseSemantica('list_tk.txt')
            semantico.analise()
            semantico.mostrar()
        except IOError:
            if not (os.path.isfile('./list_tk.txt')):
                print('O arquivo list_tk.txt não existe. Faça a análise léxica!')

    if args.lgencode or args.tudo:
        try:
            print('\n\n')
            print('*' * 20 + ' LOG GERAÇÃO DE CÓDIGO INTERMEDIÁRIO ' +
                  '*' * 20, end='\n\n')
            intermediario = Intermediario('list_tk.txt')
            intermediario.geracao()
            intermediario.mostrar()
            intermediario.salvarIntermediario()
            print('\n\n')
            print('*' * 20 + ' LOG GERAÇÃO DE CÓDIGO FINAL ' + '*' * 20, end='\n\n')
            final = Final('intermediario.itm')
            final.geracao()
            final.mostrar()
            final.salvarFinal()
        except IOError:
            if not (os.path.isfile('./list_tk.txt')):
                print('O arquivo list_tk.txt não existe. Faça a análise léxica!')
