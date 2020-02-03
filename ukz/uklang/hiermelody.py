

class Mel:
    def __init__(self):
        self.operators = []
    
class MelLeaf(Mel):
    def __init__(self,note):
        Mel.__init__(self)
        self.note = note
    def applyOperator(self,opSymbol,opArg):
        if opSymbol[0] == '@':
            # too many @'s in the operator, but whatever.
            # Just ignore the @'s and move along.
            self.applyOperator(opSymbol[1:],opArg)
        elif opSymbol[0] == '!':
            self.operators.append((opSymbol[1:],opArg))
        else:
            self.operators.append((opSymbol,opArg))
    def printTree(self,tabN=0):
        print(' '*tabN, '(note,', self.note, ')', sep='',end='')
        for op in self.operators:
            print(op[0],op[1],sep='',end='')
        print()
    def __str__(self):
        r = f"{self.note}"
        for op in self.operators:
            r += f"{op[0]}{op[1]}"
        return r
    def __repr__(self):
        return self.__str__()

# You shouldn't have both childMelodies and leafNote.
class MelNode(Mel):
    def __init__(self,type,childMelodies):
        self.type = type
        self.childMelodies = childMelodies
        Mel.__init__(self)
    def applyOperator(self,opSymbol,opArg):
        if opSymbol[0] == '@':
            for c in self.childMelodies:
                c.applyOperator(opSymbol[1:],opArg)
        elif opSymbol[0] == '!':
            for c in self.childMelodies:
                c.applyOperator(opSymbol,opArg)
        else:
            self.operators.append((opSymbol,opArg))
    def printTree(self,tabN=0):
        print(' '*tabN, ['[]','()'][self.type], sep='',end='')
        for op in self.operators:
            print(op[0],op[1],sep='',end='')
        print()
        for c in self.childMelodies:
            c.printTree(tabN+4)
    def __str__(self):
        s = "[]" if self.type==0 else "()"
        r = s[0]
        for c in self.childMelodies:
            r += f"{c}"
        r += s[1]
        for op in self.operators:
            r += f"{op[0]}{op[1]}"
        return r
    def __repr__(self):
        return self.__str__()

################
