
def isdigit(c):
    return c >= ord("0") \
     and c <= ord("9")
     
def isbinop(c):
    if c==ord("*"):
        return True
    if c==ord("/"):
        return True
    if c==ord("%"):
        return True
    if c==ord("x"):
        return True
    if c==ord("^"):
        return True
     
def iswhitekey(c):
    if c==ord("é"):
        return True
    if c == ord("x") or c == ord("X"):
        return False
    if c >= ord("a") \
     and c <= ord("z"):
        return True
    return c >= ord("A") \
     and c <= ord("Z")

def iswhitespace(c):
    if c == ord(" "):
        return True
    if c == ord("\n"):
        return True
    if c == ord("\t"):
        return True
    if c == ord("\r"):
        return True
    return False

class UkzTokenizer:
    
    stEmpty = 0
    stNote = 1
    stInt = 2
    stSymbol = 3
    stDash = 4
    stOp = 5
    
    def __init__(self):
        self.state = UkzTokenizer.stEmpty
        self.tokens = []
        self.acc = ""
        
    def nextState(state,c):
        if iswhitespace(c):
            return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stEmpty:
            if isdigit(c):
                return UkzTokenizer.stInt
            if iswhitekey(c):
                return UkzTokenizer.stNote
            if isbinop(c):
                return UkzTokenizer.stOp
            #if c == ord("x"):
            #    return UkzTokenizer.stSymbol
            if c==ord("-"):
                return UkzTokenizer.stDash
            return UkzTokenizer.stSymbol
        if state == UkzTokenizer.stNote:
            if isdigit(c) or c==ord("#"):
                return state
            return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stInt:
            if isdigit(c):
                return state
            return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stSymbol:
            return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stDash:
            if isdigit(c):
                return UkzTokenizer.stInt
            return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stOp:
            return UkzTokenizer.stEmpty
        return UkzTokenizer.stEmpty
        
    
    def step(self,s):
        c = ord(s)
        ns = UkzTokenizer.nextState(\
        	self.state,c)
        if ns == UkzTokenizer.stEmpty:
            if len(self.acc) > 0:
                tk = (self.acc,self.state)
                self.tokens.append(tk)
            self.acc = ""
            self.state = \
             UkzTokenizer.nextState(\
            	ns,c)
        else:
            self.state = ns
        if not iswhitespace(c):
            self.acc += s
    
    def parse(self,string):
        self.__init__()
        for s in string:
            self.step(s)
        self.step("\n")
        return self.tokens
        