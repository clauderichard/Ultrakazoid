import unittest
from ukz.uklr.pat import *

class TestPatMethods(unittest.TestCase):

################
# Helper methods

  def patm(self,p,s,pme):
    pma = p.match(s)
    self.assertEqual(pma,pme)
        
  def revpat(self,p,r):
    p.reverse()
    self.assertEqual(p,r)

  def patheads(self,pat,e):
    r = pat.heads()
    self.assertEqual(r,e)
  def pattails(self,pat,e):
    r = pat.tails()
    self.assertEqual(r,e)
  def patpairs(self,pat,e):
    r = pat.pairs()
    self.assertEqual(r,e)
        
################
# Tests

  def test_match_maybe(self):
    self.patm(maybe(2),[],0)
    self.patm(maybe(2),[2],1)
    self.patm(seq(maybe(2),maybe(2)),[],[0,0])
    self.patm(seq(maybe(2),maybe(2)),[2],[1,0])
    self.patm(seq(maybe(2),maybe(2)),[2,2],[1,1])
    self.patm(maybe(star(2)),[2],[1])
    self.patm(star(maybe(2)),[2],[1])

  def test_match_alt(self):
    # alt
    self.patm(alt(3),[],None)
    self.patm(alt(3,4),[],None)
    self.patm(alt(3,4),[3],1)
    self.patm(alt(3,4),[3,4],1)
    self.patm(alt(3,4),[4,7],1)
    self.patm(alt(3,4),[5,3,4],None)

  def test_reverse_alt(self):
    self.revpat(alt(1),alt(1))
    self.revpat(alt(3,4),alt(3,4))

  def test_match_star(self):
    self.patm(star(2),[],[])
    self.patm(star(2),[3,2,3],[])
    self.patm(star(2),[2,2,3,2,3],[1,1])
    self.patm(star(2),[2,2,2,3],[1,1,1])

  def test_reverse_star(self):
    self.revpat(star(3),star(3))
    self.revpat(star(alt(3,4)),star(alt(3,4)))

  def test_match_starwithseq(self):
    self.patm(seq(2,star(3),4),[2,4,5],[1,[],1])
    self.patm(seq(2,star(3),4),[2,3,4,5],[1,[1],1])
    self.revpat(star(seq(3,4)),star(seq(4,3)))

  def test_match_plus(self):
    self.patm(plus(2),[],None)
    self.patm(plus(2),[3,2,3],None)
    self.patm(plus(2),[2,2,3,2,3],[1,1])
    self.patm(plus(2),[2,2,2,3],[1,1,1])

  def test_match_pluswithseq(self):
    self.patm(seq(2,plus(3),4),[2,4,5],None)
    self.patm(seq(2,plus(3),4),[2,3,4,5],[1,[1],1])

  def test_reverse_pluswithseq(self):
    self.revpat(plus(seq(3,4)),plus(seq(4,3)))
    self.revpat(seq(3,plus(seq(3,4))),seq(plus(seq(4,3)),3))
    self.revpat(seq(3,plus(seq(4,3))),seq(plus(seq(3,4)),3))
    self.revpat(seq(2,plus(seq(17,2))),seq(plus(seq(2,17)),2))

  def test_match_seqwithplus(self):
    self.patm(seq(2,17),[2,17,2,10,10,-2],[1,1])
    self.patm(plus(seq(2,17)),[2,17,2,10,10,-2],[[1,1]])
    self.patm(seq(plus(seq(2,17)),2),[2,17,2,10,10,-2],[[[1,1]],1])

  def test_reverse_plusseqalt(self):
    self.revpat(seq(3,plus(seq(alt(4,5),3))),seq(plus(seq(3,alt(4,5))),3))

  def test_match_staralt(self):  
    self.patm(star(alt(4,5)),[4,1,-1],[1])
    self.patm(star(alt(4,5)),[5,4,5,1,-1],[1,1,1])

  def test_match_seqstaralt(self):
    self.patm(seq(9,star(alt(4,5)),1),[9,4,1,-1],[1,[1],1])
    self.patm(seq(9,star(alt(4,5)),1),[9,5,1,-1],[1,[1],1])

  def test_match_star_longstring(self):
    self.patm(star(3),[3]*100,[1]*100)

  def test_heads(self):
    self.patheads(star(1),[1])
    self.patheads(alt(1,3),[1,3])
    self.patheads(star(seq(3,4)),[3])
    self.patheads(star(alt(3,4)),[3,4])

  def test_tails(self):
    self.pattails(star(1),[1])
    self.pattails(alt(1,3),[1,3])
    self.pattails(star(seq(3,4)),[4])
    self.pattails(star(alt(3,4)),[3,4])

  def test_pairs(self):
    self.patpairs(star(1),[(1,1)])
    self.patpairs(plus(1),[(1,1)])
    self.patpairs(PatSingle(6),[])
    self.patpairs(alt(1,2,3),[])
    self.patpairs(seq(alt(1,2),alt(3,4)),[(1,3),(1,4),(2,3),(2,4)])
    self.patpairs(seq(2,3),[(2,3)])
    self.patpairs(seq(2,3,3),[(2,3),(3,3)])
    self.patpairs(star(seq(2,3)),[(2,3),(3,2)])
    self.patpairs(star(alt(seq(2,3),4)),[(2,3),(3,2),(3,4),(4,2),(4,4)])

################################

if __name__ == '__main__':
    unittest.main()