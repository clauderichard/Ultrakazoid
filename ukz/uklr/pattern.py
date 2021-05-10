
class PatOr:
    def __init__(self,options):
        self.options = options
    def __repr__(self):
        s = "("
        for o in self.options:
            s += f"{o}|"
        return s[0:len(s)-1] + ")"

class PatStar:
    def __init__(self,elmt):
        self.elmt = elmt
    def __repr__(self):
        return f"{self.elmt}*"
        
class PatPlus:
    def __init__(self,elmt):
        self.elmt = elmt
    def __repr__(self):
        return f"{self.elmt}+"
        
def star(x):
    return PatStar(x)
def plus(x):
    return PatPlus(x)
def alt(*ls):
    return PatOr(ls)
