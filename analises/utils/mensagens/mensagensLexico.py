def msgErroLexico(lex, lin, col):
    return f'Lexema: [ {lex} ] | Linha: {lin} | Coluna: {col + 1} -> Erro léxico!'


def msgLog(lex, final, atual, lin, col):
    return f'Lexema: {lex} | Token: {final[atual]} | Linha: {lin} | Coluna: {col + 1}'


def token(lex, final, atual, lin, col):
    return f'{lex}|{final[atual]}|{lin}|{col+1}\n'
