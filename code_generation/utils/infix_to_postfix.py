def infix_to_postfix(exp):
    prec = {"*": 3, "/": 3, "<=": 2,  # Precedências
            ">=": 2, "+": 2, "-": 2,
            "(": 1
            }
    opStack = []
    postfixList = []
    tokenList = exp.split()

    for token in tokenList:
        if token.isalnum():
            postfixList.append(token)
        elif token == '(':
            opStack.append(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while not len(opStack) == 0 and (prec[opStack[-1]] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.append(token)

    while not len(opStack) == 0:
        postfixList.append(opStack.pop())
    return " ".join(postfixList)
