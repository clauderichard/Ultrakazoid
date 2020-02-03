from fractions import *

################################

def numerize(n):
    if isinstance(n,str):
        try:
            return int(n)
        except ValueError:
            return Fraction(n)
    else:
        return n
        
def divide(a,b):
    aa = numerize(a)
    bb = numerize(b)
    if isinstance(a,int) \
     and isinstance(b,int):
        return Fraction(aa,bb)
    else:
        return aa / bb

################################

def intsFromTo(a,b):
    if a<=b:
        return range(a,b+1)
    else:
        return range(a,b-1,-1)

################################
