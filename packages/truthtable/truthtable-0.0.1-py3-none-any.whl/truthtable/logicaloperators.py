from truthtable.operators import Prefix,Infix

symbols = {}
unary_operators = []

def add_operator(sym, char):
    obj = eval(char)
    priority = obj.priority()
    if priority == 1:
        unary_operators.append(sym)
    char = {
            priority == 1: char+"**",
            priority == 2: "*"+char+"*",
            priority == 3: "+"+char+"+",
            priority == 4: "&"+char+"&",
            priority == 5: "|"+char+"|"
    }[True]
    symbols[sym] = char


negation      = Prefix(lambda x: not x)
conjunction   = Infix(lambda x,y: x and y, 2)
disjunction   = Infix(lambda x,y: x or y, 3)
implication   = Infix(lambda x,y: not x or y, 4)
rimplication  = Infix(lambda x,y: not y or x, 4)
biconditional = Infix(lambda x,y: x == y, 5)


add_operator("~", "negation")
add_operator("&&", "conjunction")
add_operator("||", "disjunction")
add_operator("->", "implication")
add_operator("<-", "rimplication")
add_operator("<=>", "biconditional")


if __name__ == "__main__":
    print("This module is not intended for execution")
