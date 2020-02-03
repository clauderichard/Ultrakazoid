from ukz.tokenizerautomaton import *

def getops():
    for s in getopsSimple():
        yield s
        #yield "!"+s
        #yield "@"+s

def getopsSimple():
    yield "+"
    yield "-"
    yield "*"
    yield "**"
    yield "¬"
    yield "%"
    yield "/"
    yield "//"
    yield "^"
    yield "\\"
    yield "="

def isdigit(c):
    return c >= ord("0") \
     and c <= ord("9")
def isdigitS(s):
    if len(s) != 1:
        raise ValueError("s must be a single character")
    c = ord(s)
    return c >= ord("0") \
     and c <= ord("9")
    
def isAlphaNumeric(c):
    if c >= ord("0") \
     and c <= ord("9"):
        return True
    if c >= ord("a") \
     and c <= ord("z"):
        return True
    if c >= ord("A") \
     and c <= ord("Z"):
        return True
    return False
    
def isAlphaNumericS(s):
    if len(s) != 1:
        raise ValueError("s must be a single character")
    c = ord(s)
    if c >= ord("0") \
     and c <= ord("9"):
        return True
    if c >= ord("a") \
     and c <= ord("z"):
        return True
    if c >= ord("A") \
     and c <= ord("Z"):
        return True
    return False
     
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
    if c==ord("="):
        return True
    if c==ord("+"):
        return True
    if c==ord("-"):
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

def issymbol(c):
    if iswhitespace(c):
        return False
    if isdigit(c):
        return False
    if iswhitekey(c):
        return False
    return True

class UkzTokenizer:
    
    stEmpty = 0
    stNote = 1
    stInt = 2
    stSymbol = 3
    stDot = 4
    #stDash = 4
    stOp = 5
    stVar = 6
    
    instance = None
    
    def __init__(self):
        self.state = UkzTokenizer.stEmpty
        self.tokens = []
        self.acc = ""
        self.tauto = TokenizerAutomaton()
        for o in getops():
            self.tauto.addWord(o)
            
    def getSingleton():
        if UkzTokenizer.instance is None:
            UkzTokenizer.instance = UkzTokenizer()
        return UkzTokenizer.instance
        
    def nextState(self,state,s,c):
        if s == "$":
            if state == UkzTokenizer.stEmpty:
                return UkzTokenizer.stVar
            return UkzTokenizer.stEmpty
        if iswhitespace(c):
            return UkzTokenizer.stEmpty
        if state != UkzTokenizer.stEmpty \
         and s==".":
            return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stEmpty:
            if self.tauto.symbolMayExist(s):
                return UkzTokenizer.stOp
            if s==".":
                return UkzTokenizer.stDot
            if isdigit(c):
                return UkzTokenizer.stInt
            if iswhitekey(c):
                return UkzTokenizer.stNote
            #if isbinop(c):
            #    return UkzTokenizer.stOp
            #if c == ord("x"):
            #    return UkzTokenizer.stSymbol
            #if c==ord("-"):
            #    return UkzTokenizer.stDash
            return UkzTokenizer.stSymbol
        if state == UkzTokenizer.stNote:
            if isdigit(c) or c==ord("#") or c==ord("°"):
                return state
            return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stInt:
            if isdigit(c):
                return state
            return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stSymbol:
            if issymbol(c):
                o = self.acc + s
                if self.tauto.symbolMayExist(o):
                    return UkzTokenizer.stSymbol
            return UkzTokenizer.stEmpty
        #if state == UkzTokenizer.stDash:
        #    if isdigit(c):
        #        return UkzTokenizer.stInt
        #    return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stOp:
            if issymbol(c):
                o = self.acc + s
                if self.tauto.symbolMayExist(o):
                    return UkzTokenizer.stOp
            return UkzTokenizer.stEmpty
        if state == UkzTokenizer.stVar:
            if isAlphaNumericS(s):
                return UkzTokenizer.stVar
        return UkzTokenizer.stEmpty
        
    
    def step(self,s):
        ret = None
        c = ord(s)
        ns = self.nextState(\
        	self.state,s,c)
        if ns == UkzTokenizer.stEmpty:
            if len(self.acc) > 0:
                tk = (self.acc,self.state)
                self.tokens.append(tk)
                ret = tk
            self.acc = ""
            self.state = \
             self.nextState(\
            	ns,s,c)
        else:
            self.state = ns
        if not iswhitespace(c):
            self.acc += s
        return ret
    
    def parse(self,string):
        self.__init__()
        for s in string+"\n":
            r = self.step(s)
            if r is not None:
                yield r
        