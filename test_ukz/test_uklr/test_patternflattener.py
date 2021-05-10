import unittest
from ukz.uklr.flatparser import *
from ukz.uklr.pattern import *
from ukz.uklr.patternflattener import *
	
class TestPatternFlattener(unittest.TestCase):

################
# Helper methods

    def pars(self,lhs,rhs,tks,res):
        fun = lambda *ls: ls
        rules = flattenedRules(lhs,rhs,fun)
        parser = FlatParser()
        for rule in rules:
            l,r,f = rule
            parser.addRule(l,r,f)
        toks = []
        for tk in tks.split(' '):
            toks.append(TkToken(tk,tk))
        actualRes = parser.parse(toks)
        self.assertEqual(res, actualRes)
    
    def nopars(self,lhs,rhs,tks):
        fun = lambda *ls: ls
        rules = flattenedRules(lhs,rhs,fun)
        parser = FlatParser()
        for rule in rules:
            l,r,f = rule
            parser.addRule(l,r,f)
        toks = []
        for tk in tks.split(' '):
            toks.append(TkToken(tk,tk))
        actualRes = parser.parse(toks)
        self.assertIsNone(actualRes)
    
################
# Tests

    def test_flat_single(self):
        self.pars("a",["b"], "b", ('b',))
    
    def test_plus_simple(self):
        self.pars("a",[plus("b")], "b", (['b'],))
        self.pars("a",[plus("b")], "b b", (['b','b'],))
    
    def test_plus_inbrackets(self):
        self.pars("a",["b",plus("c"),"d"], "b c d", ('b',['c'],'d'))
        self.pars("a",["b",plus("c"),"d"], "b c c d", ('b',['c','c'],'d'))
    
    def test_star_inbrackets(self):
        self.pars("a",["b",star("c"),"d"], "b d", ('b',[],'d'))
        self.pars("a",["b",star("c"),"d"], "b c d", ('b',['c'],'d'))
        self.pars("a",["b",star("c"),"d"], "b c c d", ('b',['c','c'],'d'))
    
    def test_starofalt_inbrackets(self):
        pat = ["b",star(alt("c","d")),"e"]
        self.pars("a",pat, "b e", ('b',[],'e'))
        self.pars("a",pat, "b c e", ('b',['c'],'e'))
        self.pars("a",pat, "b d e", ('b',['d'],'e'))
        self.pars("a",pat, "b d c e", ('b',['d','c'],'e'))
        self.pars("a",pat, "b d c c e", ('b',['d','c','c'],'e'))
    
    def test_alt_plusorflat(self):
        pat = ["b",alt(plus("c"),"d")]
        self.pars("a",pat, "b d", ('b','d'))
        self.pars("a",pat, "b c", ('b',['c']))
        self.pars("a",pat, "b c c", ('b',['c','c']))
        self.nopars("a",pat, "b c d")
    
    def test_alt_plusaltorflat(self):
        pat = ["b",alt(plus(alt("c","d")),"e")]
        self.pars("a",pat, "b e", ('b','e'))
        self.nopars("a",pat, "b c e")
        self.nopars("a",pat, "b d e")
        self.pars("a",pat, "b c", ('b',['c']))
        self.pars("a",pat, "b c c", ('b',['c','c']))
        self.pars("a",pat, "b c d", ('b',['c','d']))
        self.pars("a",pat, "b c d c", ('b',['c','d','c']))
    
    
################################

if __name__ == '__main__':
    unittest.main()