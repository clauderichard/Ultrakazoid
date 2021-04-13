import unittest
from ukz.uklr.flatparser import *
	
def f1(x):
    return x
def f2(x,y):
    return x
def f3(x,y,z):
    return x
def f4(x,y,z,a):
    return x
def f5(x,y,z,a,b):
    return x
    
def fN(n):
    if n==1:
        return f1
    if n==2:
        return f2
    if n==3:
        return f3
    if n==4:
        return f4
    if n==5:
        return f5
    raise Exception("fN of too big an N! Go add it.")

class TestParserFlatRuleset(unittest.TestCase):

################
# Helper methods

    def setUp(self):
        self.p = ParserFlatRuleset()
        self.parser = FlatParser()
        self.pInitialized = False
    
    def rul(self,restyp,stacktypes):
        f = fN(len(stacktypes))
        self.p.addRule(restyp,stacktypes,f)
        self.parser.addRule(restyp,stacktypes,f)
        
    def yes(self,st,nx):
        if not self.pInitialized:
            self.p.initialize()
            self.pInitialized = True
        stack = list(map(lambda t: \
          TkToken(t,9999), st ))
        nextInput = TkToken(nx,9999)
        m = self.p.matchStackTokens(stack,nextInput)
        self.assertIsInstance(m,ParserFlatRule)
        
    def no(self,st,nx):
        if not self.pInitialized:
            self.p.initialize()
            self.pInitialized = True
        stack = list(map(lambda t: \
          TkToken(t,9999), st ))
        nextInput = TkToken(nx,9999)
        m = self.p.matchStackTokens(stack,nextInput)
        self.assertIsNone(m)
        
    def parse(self,tokentypelist):
        tokenlist = list(map(lambda t: \
          TkToken(t,9999), tokentypelist ))
        res = self.parser.parse(tokenlist)
        return res
    def pars(self,tokentypelist):
        res = self.parse(tokentypelist)
        self.assertIsNotNone(res)
    def nopars(self,tokentypelist):
        res = self.parse(tokentypelist)
        self.assertIsNone(res)

################
# Tests

    def test_match_novalidnextinput(self):
        A = 20
        B = 30
        
        # i guess nextInput never in whitelist?
        #self.rul(B,[A])
        self.rul(B,[A,A])
        
        self.no([1,A],B)
        self.no([1,A],A)
        self.no([1,B],B)
        self.no([1,A,B],B)
        self.no([1,A,A],A)
        
    def test_match_arithmetic(self):
        plus = 20
        x = 30
        n = 88
        sums = 886
        term = 33
        self.rul(term,[n])
        self.rul(term,[term,x,term])
        self.rul(sums,[term,plus,term])
        self.rul(sums,[sums,plus,term])
        self.yes([n,x,n],plus)
        self.yes([sums,plus,n],x)
        self.yes([term,plus,term],plus)
        self.no([term,plus,term],term)
        self.no([n,plus,plus],n)
    
    # def test_reduce_simplesum(self):
    #     A = 20
    #     B = 30
    #     self.rul(B,[A,A])
    #     self.rul(B,[B,A])
    #     self.yes([1,A,A],A)
    #     self.red([1,A,A],A,[1,B])
        
    def test_parse_arithmetic(self):
        plus = 20
        x = 30
        n = 88
        sums = 886
        term = 33
        self.rul(term,[n])
        self.rul(term,[term,x,term])
        self.rul(sums,[term,plus,term])
        self.rul(sums,[sums,plus,term])
        self.nopars([n,n])
        self.nopars([n,x,x,n])
        self.pars([n,x,n])
        self.pars([n,x,n,plus,n])
        self.pars([n,x,n,x,n])
        self.pars([n,plus,n,plus,n])
        self.pars([n,plus,n,x,n])

    def test_parse_subset(self):
        P = 20
        TO = 30
        SHARP = 40
        MEL = 25
        SHRED = 50
        
        self.rul(SHRED,[P,TO,P])
        self.rul(P,[P,SHARP])
        self.rul(MEL,[P])
        self.rul(MEL,[SHRED])
        
        self.pars([P])
        self.pars([P,SHARP])
        self.pars([P,TO,P])
        self.pars([P,TO,P,SHARP])
        
################################

if __name__ == '__main__':
    unittest.main()