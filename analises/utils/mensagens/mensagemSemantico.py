def declarada(l):
    return f'A variável {l[0]} na linha e coluna ({l[2]}, {l[3].strip()}) já foi declarada anteriormente. Declaração duplicada.'


def naoDeclarada(l):
    return f'A variável {l[0]} na linha e coluna ({l[2]}, {l[3].strip()}) não foi declarada. Declare antes de usá-la!'


def divisaoPorZero(l):
    return f'Ocorreu uma divisão por zero via atribuição de variável na linha e coluna ({l[2]}, {l[3].strip()})'
