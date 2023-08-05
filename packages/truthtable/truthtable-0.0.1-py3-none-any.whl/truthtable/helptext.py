from sys import argv
helptext = """Truth table printer.

Usage:
""" + argv[0] + """ [-hbn] [--help] [--bool|--numeric]
  -h | --help     Print this message
  -b | --bool     Use boolean values to fill the table
  -n | --numeric  Use numeric values to fill the table(defualt)
  -d | --debug    For printing intermediate representation of expression

Expression syntax:
  Variable name:
    [a-zA-Z]+
  Operations:
    &&  - conjunction
    ||  - disjunction
    ->  - implication
    <-  - converse implication
    <=> - biconditional
    ^   - exclusive disjunction
    ~   - negation
Examples:
    A && B ^ ~(~A || (A<=>C))
    A && B <=> ~(~A -> ~(~B <=> A))
    BC -> A -> C <=> ~(A || (BC && C))"""


if __name__ == "__main__":
    print("This module is not intended for execution")
