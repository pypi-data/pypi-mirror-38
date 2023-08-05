from truthtable.logicaloperators import symbols, unary_operators
import re 

#char to sym
def cts(s):
    s = re.sub(" +", " ", s) \
            .replace("( ", "(") \
            .replace(" (", "(") \
            .replace(") ", ")") \
            .replace(" )", ")") 
    for sym, char in symbols.items():
        if sym in unary_operators:
            s = s.replace(char+" ", sym)
        s = s.replace(char, sym)
    return s

#sym to char
def stc(s):
    for sym, char in symbols.items():
        s = s.replace(sym, " "+char+" ")
    return s

if __name__ == "__main__":
    print("This module is not intended for execution")
