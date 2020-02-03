import unittest
from .test_uk_base import TestUkBase
from ukz import ukz,ukd,Gradient,DrumPitch
from fractions import Fraction

class TestUkPrimitives(TestUkBase):

################
# Tests

  def test_emptymels(self):
    self.chkukz("[]",0,0,[])
    self.chkukz("()",0,0,[])
    self.chkukd("[]",0,0,[])
    self.chkukd("()",0,0,[])
    
  def test_invalidchar(self):
    self.failukz("(#)")
    self.failukd("(#)")

  def test_ukz_primitives(self):
    self.chkukzPrim("c",0)
    self.chkukzPrim("d",2)
    self.chkukzPrim("e",4)
    self.chkukzPrim("f",5)
    self.chkukzPrim("g",7)
    self.chkukzPrim("a",9)
    self.chkukzPrim("b",11)

  def test_ukd_primitives(self):
    self.chkukdPrim('b',DrumPitch.bassPedal)
    self.chkukdPrim('s',DrumPitch.snare)
    self.chkukdPrim('S',DrumPitch.snare+12)
    self.chkukdPrim('G',DrumPitch.gong+12)
    self.chkukdPrim('G^',DrumPitch.splashCymbal+12)

  def test_drum_capitalized(self):
    self.chkukd("S",0,1,[\
     (0,1,DrumPitch.snare+12,5)])

  def test_rest(self):
    self.chkukz(".",0,1,[])
    self.chkukd(".",0,1,[])

################################

if __name__ == '__main__':
    unittest.main()