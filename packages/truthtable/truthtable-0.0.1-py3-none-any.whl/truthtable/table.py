from truthtable.symbols import cts
from truthtable.logicaloperators import *
from prettytable import PrettyTable
import itertools
import re

def repl(lst):
    new_lst = []
    for i in lst:
        new_lst.append(cts(i))
    return new_lst

class Obj(object):
    pass

class Table(object):
    def __init__(self, base=None, phrases=None, ints=True, debug=False):
        self.base = base
        self.phrases = phrases or []
        self.ints = ints
        self.debug = debug

        # generate the sets of booleans for the bases
        self.base_conditions = list(itertools.product([False, True],
                                                      repeat=len(base)))

        # regex to match whole words defined in self.bases
        # used to add object context to variables in self.phrases
        self.p = re.compile(r'(?<!\w)(' + '|'.join(self.base) + ')(?!\w)')

    def calc(self, *args):
        # store bases in an object context
        g = Obj()
        for a, b in zip(self.base, args):
            setattr(g, a, b)

        # add object context to any base variables in self.phrases
        # then evaluate each
        eval_phrases = []
        for item in self.phrases:
            item = self.p.sub(r'g.\1', item)
            eval_phrases.append(eval(item))

        # add the bases and evaluated phrases to create a single row
        row = [getattr(g, b) for b in self.base] + eval_phrases
        if self.ints:
            return [int(item) for item in row]
        else:
            return row

    def __str__(self):
        t = PrettyTable(self.base + repl(self.phrases))
        if self.debug:
            print(self.phrases[0])
        for conditions_set in self.base_conditions:
            t.add_row(self.calc(*conditions_set))
        return str(t)

if __name__ == "__main__":
    print("This module is not intended for execution")
