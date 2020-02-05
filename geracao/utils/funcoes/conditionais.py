def loop(L, e, op):
    return f'_L{L}: if {e.split()[0]} {op} {e.split()[2]} goto _L{L + 1}'


def condicional(C, e, op):
    return f'_C{C}: if {e.split()[0]} {op} {e.split()[2]} goto _C{C + 1}'
