from fractions import Fraction

class Ratio:

    def __init__(self,n,d):
        self.n = n
        self.d = d
    
    # mul and rmul should take integer o
    def __mul__(self,o):
        return (self.n*o) // self.d
    def __rmul__(self,o):
        return (o*self.n) // self.d

def mkFraction(a):
    if isinstance(a,str):
        x = Fraction(a)
        if x.numerator % x.denominator == 0:
            return x.numerator // x.denominator
        return Ratio(x.numerator, x.denominator)
    raise Exception('mkFraction expects a string argument')
