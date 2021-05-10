import unittest
from ukz.uklr.transmatrix import TransMatrix

class TestTransMatrix(unittest.TestCase):

################
# Helper methods

  def eq(self,a,b):
    aa = TransMatrix(a)
    bb = TransMatrix(b)
    self.assertTrue(aa == bb)

  def neq(self,a,b):
    aa = TransMatrix(a)
    bb = TransMatrix(b)
    self.assertTrue(aa != bb)

  def eqmulii(self,a,b,c):
    aa = TransMatrix(a,True)
    bb = TransMatrix(b,True)
    cc = TransMatrix(c,True)
    r = aa*bb
    if not (cc == r):
      print('result.xs =',r.xs)
    self.assertEqual(cc,r)
    
  def eqpinf(self,a,b):
    aa = TransMatrix(a,True)
    bb = TransMatrix(b,True)
    aa.ipowInf()
    self.assertEqual(bb,aa)
    
################
# Tests

  def test_eq_empty(self):
    self.eq({2:{}},{2:{}})
  def test_eq_single(self):
    self.eq({2:{3}},{2:{3}})
  def test_eq_double(self):
    self.eq({2:{3,9}},{2:{3,9}})
  def test_eq_multiple(self):
    self.eq({2:{3,9},3:{9}},{2:{3,9},3:{9}})

  def test_neq_separate(self):
    self.neq({2:{3}},{4:{5}})

  def test_mul_separate(self):
    self.eqmulii({2:{3}},{4:{5}},{2:{3},4:{5}})
  def test_mul_sequence(self):
    self.eqmulii({2:{4}},{4:{5}},{2:{4,5},4:{5}})
    
  def test_powinf_eye(self):
    self.eqpinf({},{})
  def test_powinf_single(self):
    self.eqpinf({3:{4}},{3:{4}})
  def test_powinf_double(self):
    self.eqpinf({3:{4},5:{6}},{3:{4},5:{6}})
    self.eqpinf({3:{4,6}},{3:{4,6}})
  def test_powinf_seq(self):
    self.eqpinf({3:{4},4:{7}},{3:{4,7},4:{7}})

  def test_addArrow(self):
    t = TransMatrix()
    t.addArrow(4,6)
    self.assertTrue(6 in t[4])
    
################################

if __name__ == '__main__':
    unittest.main()