class Operator:
    def __init__(self, function):
        self.function = function
class Prefix(Operator):
    def __pow__(self, other):
        return self.function(other)
    def priority(self):
        return 1
class Infix_2(Operator):
    def __rmul__(self, other):
       return Infix_2(lambda x, self=self, other=other: self.function(other, x))
    def __mul__(self, other):
        return self.function(other)
    def priority(self):
        return 2
class Infix_3(Operator):
    def __radd__(self, other):
       return Infix_3(lambda x, self=self, other=other: self.function(other, x))
    def __add__(self, other):
        return self.function(other)
    def priority(self):
        return 3
class Infix_4(Operator):
    def __rand__(self, other):
       return Infix_4(lambda x, self=self, other=other: self.function(other, x))
    def __and__(self, other):
        return self.function(other)
    def priority(self):
        return 4
class Infix_5(Operator):
    def __ror__(self, other):
       return Infix_5(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def priority(self):
        return 5
Infixes = {2:Infix_2, 3:Infix_3, 4:Infix_4, 5:Infix_5}
def Infix(operator, precedence):
    return Infixes[precedence](operator)

if __name__ == "__main__":
    print("This module is not intended for execution")
