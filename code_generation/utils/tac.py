def tac(var, expression, cod, it):
    exp = expression.split()
    stack = []
    oper = ['+', '-', '*', '/']
    for i in range(len(exp)):
        if exp[i] in oper:
            v1 = stack.pop()
            v2 = stack.pop()
            t = f'{v2} {exp[i]} {v1}'
            if len(exp) == i+1:
                cod.append(f'{var} := {t}')
            else:
                cod.append(f't{it} := {t}')
                stack.append(f't{it}')
                it += 1
        else:
            stack.append(exp[i])
    if len(stack) == 1:
        cod.append(f'{var} := {stack[0]}')
