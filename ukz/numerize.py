
from fractions import *

def numerize(n):
    if isinstance(n,str):
        try:
            return int(n)
        except ValueError:
            return Fraction(n)
    else:
        return n
