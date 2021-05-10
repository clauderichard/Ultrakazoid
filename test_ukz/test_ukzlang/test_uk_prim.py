from .test_uk_base import TestUkBase
from ukz import DrumPitchUkz

class TestUkPrimitives(TestUkBase):

################
# Tests

  def test_check_consistency(self):
    self.equkz("c","c")
    self.equkz(".",".")
    self.equkz("[]","[]")
    self.equkz("()","()")
    self.equkz("[]","()")
    
  def test_emptymels(self):
    self.chkukz("[]",0,[])
    self.chkukz("()",0,[])
    
  def test_invalidchar(self):
    self.failukz("(#)")

  def test_ukz_prim_pitches(self):
    self.chkukzPrim("c",0)
    self.chkukzPrim("d",2)
    self.chkukzPrim("e",4)
    self.chkukzPrim("f",5)
    self.chkukzPrim("g",7)
    self.chkukzPrim("a",9)
    self.chkukzPrim("b",11)

  def test_ukz_prim_drumpitches(self):
    self.chkukzPrim('b',DrumPitchUkz.bassPedal)
    self.chkukzPrim('s',DrumPitchUkz.snare)
    self.chkukzPrim('g^',DrumPitchUkz.splashCymbal)

  def test_rest(self):
    self.chkukz(".",1,[])

################################
