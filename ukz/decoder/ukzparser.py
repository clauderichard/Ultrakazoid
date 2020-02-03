from ukz.melody import *
from ukz.decoder.ukztokenizer import *
from ukz.decoder.pianopitchdecoder import *
from ukz.decoder.drumpitchdecoder import *


class UkzParser:
    
    stSeq = 0
    stChord = 1
    
    def __init__(self,tonicChar='a',tonicPitch=0):
        self.pitchDecoder = PianoPitchDecoder(tonicChar,tonicPitch)
        self.tokenizer = UkzTokenizer()
        self.reset()
        
    def reset(self):
        self.state = UkzParser.stSeq
        self.stack = []
        self.op = False
        self.curmels = []
        
    def parse(self,string):
        toks = self.tokenizer.parse(string)
        return self.parseTokens(toks)
    def parseFile(self,fnam):
        f = open(f"scripts3/{fnam}.ukz", 'r')
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
        p = self.pitchDecoder[string]
        m = Melody()
        if isinstance(p,int):
            m.playNote(p,1)
        else:
            for pp in p:
                m.addNote(pp,1)
            m.forward(1)
        return m
        
    def applyBinaryOp(op,mel,n):
        if op == "x":
            return mel.repeat(n)
        if op == "*":
            return mel.stretch(n)
        if op == "/":
            return mel.stretch(Fraction(1,n))
        if op == "%":
            return mel.stretchTo(n)
        if op == "^":
            raise ValueError(f"op {op} not implemented")
        raise ValueError(f"binaryOp {op} not supported")
        
    def applyUnaryOp(op,mel):
        if op == "-":
            return mel.stretchByAddition(1)
        if op == "+":
            raise ValueError(f"op {op} not implemented")
        if op == ".":
            mel.forward(1)
            return mel
        raise ValueError(f"unaryOp {op} not supported")
        
    def step(self,toktyp,tokstr):
        if self.op:
            if toktyp != UkzTokenizer.stInt:
                raise Exception("expected int after op")
            i = int(tokstr)
            self.curmels[len(self.curmels)-1] = \
             UkzParser.applyBinaryOp(\
             self.op, self.curmels[len(self.curmels)-1], i)
            self.op = None
            return
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
            self.curmels[len(self.curmels)-1] = \
             UkzParser.applyUnaryOp(\
             tokstr, self.curmels[len(self.curmels)-1])
            return
        if toktyp == UkzTokenizer.stDash:
            self.curmels[len(self.curmels)-1] = \
             UkzParser.applyUnaryOp(\
             tokstr, self.curmels[len(self.curmels)-1])
            return
        if toktyp == UkzTokenizer.stNote:
            m = self.parseNote(tokstr)
            self.curmels.append(m)

class UkzDrumParser(UkzParser):
    def __init__(self):
        UkzParser.__init__(self)
        self.pitchDecoder = DrumPitchDecoder()

