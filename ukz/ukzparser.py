from ukz.melody import *
from ukz.ukztokenizer import *
from ukz.pianopitchdecoder import *
from ukz.drumpitchdecoder import *


def ukzApplyBinaryOp(op,mel,n):
    if op == "x":
        return mel.repeat(n)
    if op == "*":
        return mel.stretch(n)
    if op == "=":
        return mel.repeat(n).stretchTo(1)
    if op == "/":
        return mel.stretch(Fraction(1,n))
    if op == "+":
        return mel.translate(n)
    if op == "-":
        return mel.translate(-n)
    if op == "%":
        return mel.stretchTo(n)
    if op == "^":
        return mel.louded(n)
    raise ValueError(f"binaryOp {op} not supported")


class UkzParser:
    
    stSeq = 0
    stChord = 1
    
    folder = ""
    
    instance = None
    
    def __init__(self):
        self.pitchDecoder = PianoPitchDecoder.getSingleton()
        self.tokenizer = UkzTokenizer.getSingleton()
        self.reset()
        
    def getSingleton():
        if UkzParser.instance is None:
            UkzParser.instance = UkzParser()
        return UkzParser.instance
        
    def reset(self):
        self.state = UkzParser.stSeq
        self.stack = []
        self.op = False
        self.curmels = []
        self.var = False
        
    def parse(self,string):
        toks = self.tokenizer.parse(string)
        return self.parseTokens(toks)
    def parseFile(self,fnam):
        fff = UkzParser.folder + fnam
        f = open(f"scripts3/{fff}.ukz", 'r')
        s = f.read()
        r = self.parse(s)
        f.close()
        return r
        
    def parseTokens(self,toks):
        self.reset()
        self.step(UkzTokenizer.stSymbol,"[")
        for (string,typ) in toks:
            self.step(typ,string)
        self.step(UkzTokenizer.stSymbol,"]")
        return self.curmels[0]
        
    def parseNote(self,string):
        if string==".":
            m = Melody()
            m.forward(1)
            return m
        p = self.pitchDecoder[string]
        m = Melody()
        if isinstance(p,int):
            m.playNote(p,1)
        else:
            for pp in p:
                m.addNote(pp,1)
            m.forward(1)
        return m
        
    
    def applyUnaryOp(op,mel):
        #if op == "-":
        #    return mel.stretchByAddition(1)
        #if op == "+":
        #    raise ValueError(f"op {op} not implemented")
        #if op == ".":
        #    mel.forward(1)
        #    return mel
        raise ValueError(f"unaryOp {op} not supported")
        
    def step(self,toktyp,tokstr):
        if self.op:
            if toktyp != UkzTokenizer.stInt:
                raise Exception("expected int after op")
            i = int(tokstr)
            self.curmels[len(self.curmels)-1] = \
             ukzApplyBinaryOp(\
             self.op, self.curmels[len(self.curmels)-1], i)
            self.op = None
            return
        if self.var:
            raise Exception("not implemented (var)")
        if tokstr == "(" or tokstr == "[":
            self.stack.append((self.state,self.curmels))
            if tokstr == "(":
                self.state = UkzParser.stChord
            elif tokstr == "[":
                self.state = UkzParser.stSeq
            self.curmels = []
            return
        if tokstr == ")" or tokstr == "]":
            mel = Melody()
            if tokstr == ")":
                if self.state != UkzParser.stChord:
                    raise Exception("unmatched )")
                for m in self.curmels:
                    mel.addMelody(m)
                mel.forward(self.curmels[0].curTime)
            elif tokstr == "]":
                if self.state != UkzParser.stSeq:
                    raise Exception("unmatched ]")
                for m in self.curmels:
                    mel.playMelody(m)
            (self.state,self.curmels) = self.stack.pop()
            self.curmels.append(mel)
            return
        if toktyp == UkzTokenizer.stOp:
            if self.op:
                raise Exception("you have two op symbols in a row")
            self.op = tokstr
            return
        if toktyp == UkzTokenizer.stSymbol:
            if len(self.curmels) == 0:
                self.curmels.append(Melody())
            self.curmels[len(self.curmels)-1] = \
             UkzParser.applyUnaryOp(\
             tokstr, self.curmels[len(self.curmels)-1])
            return
        #if toktyp == UkzTokenizer.stDash:
        #    self.curmels[len(self.curmels)-1] = \
        #     UkzParser.applyUnaryOp(\
        #     tokstr, self.curmels[len(self.curmels)-1])
        #    return
        if toktyp == UkzTokenizer.stNote:
            m = self.parseNote(tokstr)
            self.curmels.append(m)
        if toktyp == UkzTokenizer.stDot:
            m = self.parseNote(tokstr)
            self.curmels.append(m)

class UkzDrumParser(UkzParser):
    
    instance = None
    
    def __init__(self):
        UkzParser.__init__(self)
        self.pitchDecoder = DrumPitchDecoder.getSingleton()

    def getSingleton():
        if UkzDrumParser.instance is None:
            UkzDrumParser.instance = UkzDrumParser()
        return UkzDrumParser.instance
        
def parseUkz(s):
    p = UkzParser.getSingleton()
    return p.parse(s)
def parseUkzFile(filename):
    p = UkzParser()
    return p.parseFile(filename)
def parseUkzDrums(s):
    p = UkzDrumParser()
    return p.parse(s)
def parseUkzDrumsFile(filename):
    p = UkzDrumParser()
    return p.parseFile(filename)
