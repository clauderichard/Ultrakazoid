import unittest
from ukz.util.iterutil import *

class TestIterutil(unittest.TestCase):

################################################
# Helper functions
    
  def ift(self,a,b,expected):
    self.assertEqual(expected, list(intsFromTo(a,b)))
  
  def cart(self,expected,*lists):
    self.assertEqual(expected, list(cartProd(*lists)))

################################################
# Tests for cartProd

  def test_cartProd_empty(self):
    self.cart([],[])

  def test_cartProd_two_empties(self):
    self.cart([],[],[])

  def test_cartProd_single(self):
    self.cart([(3,)],[3])

  def test_cartProd_double(self):
    self.cart([(3,),(5,)],[3,5])

  def test_cartProd_two_singles(self):
    self.cart([(3,5)],[3],[5])

  def test_cartProd_two_doubles(self):
    self.cart([(3,1),(3,4),(6,1),(6,4)],[3,6],[1,4])

  def test_cartProd_three_lists(self):
    self.cart([ \
     (3,1,'x'),(3,1,'y'),(3,4,'x'),(3,4,'y'),(3,5,'x'),(3,5,'y'),
     (6,1,'x'),(6,1,'y'),(6,4,'x'),(6,4,'y'),(6,5,'x'),(6,5,'y')], \
     [3,6],[1,4,5],['x','y'])
    
################################################
# Tests for intsFromTo

  def test_intsFromTo_sameNumber(self):
    self.ift(4,4,[4])
    
  def test_intsFromTo_upward(self):
    self.ift(3,5,[3,4,5])
    
  def test_intsFromTo_downward(self):
    self.ift(6,3,[6,5,4,3])
    
################################################

if __name__ == '__main__':
    unittest.main()