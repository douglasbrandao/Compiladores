def msgErroSintatico(f, i):
    return f'Erro sintático: Token {f[i-1][0]} inesperado na linha: {f[i-1][2]}, coluna: {f[i-1][3].strip()}'
