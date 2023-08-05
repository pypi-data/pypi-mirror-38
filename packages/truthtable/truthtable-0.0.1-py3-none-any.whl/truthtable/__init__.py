#!/usr/bin/env python3
from truthtable.table import Table
from truthtable.symbols import stc
from truthtable.helptext import helptext
from sys import argv
import re

name = "truthtable"

def main():
    ints = True
    debug = False
    if "-h" in argv or "--help" in argv:
        print(helptext)
        exit(0)
    if ("-n" in argv or "--numeric" in argv) and ("-b" in argv or "--bool" in argv):
        print('--bool and --numeric cant be used at the same time!')
        exit(-1)
    if "-b" in argv or "--bool" in argv:
        ints = False
    if "-d" in argv or "--debug" in argv:
        debug = True
    expression = input("Expression: ")
    # get all variables
    vs = re.findall("[a-zA-Z]+", expression)
    # sorted and uniq vraible names
    vs = list(sorted(set(vs)))
    # try:
    print(Table(vs, [stc(expression)], ints, debug))
    # except:
        # print("Incorrect input")
