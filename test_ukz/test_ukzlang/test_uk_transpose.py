from .test_uk_base import TestUkBase
from ukz import DrumPitchUkz

class TestUkTranspose(TestUkBase):

################
# Tests

  def test_pitch_transpose_up(self):
    self.chkukzPrim("c^",1)
    self.chkukzPrim("c^^^",3)
    self.chkukzPrim("c^4",4)

  def test_pitch_transpose(self):
    self.chkukzPrim("e^",5)
    self.equkz("c^^","d")
    self.equkz("c1","d1vv")
    self.equkz("D1b","e2vva^^")

  def test_pitch_transpose_updown(self):
    self.equkz("e^v","e")
    self.equkz("f^vv","e")

  def test_pitch_octaveshift(self):
    self.chkukzPrim("C",12)
    self.chkukzPrim("c1",12)
    self.chkukzPrim("e1",16)
    self.chkukzPrim("e2",28)
    self.chkukzPrim("E1",28)

  def test_pitch_octaveshift_negative(self):
    self.equkz("b-1","cv")

  def test_pitch_doublev(self):
    self.chkukzPrim("cvv",-2)
    self.chkukzPrim("Cvv",10)
    self.chkukzPrim("Dvv",12)

  def test_pitch_combos(self):
    self.chkukzPrim("c^^",2)
    self.equkz("E1","e2")
    self.chkukzPrim("f1v",16)
    self.chkukzPrim("d1vv",12)
    self.equkz("D1b","e2vva^^")

  def test_drumpitch_transpose(self):
    self.chkukzPrim('S',DrumPitchUkz.snare+12)
    self.chkukzPrim('G',DrumPitchUkz.gong+12)
    self.chkukzPrim('G^',DrumPitchUkz.splashCymbal+12)

  def test_melody_transposeup(self):
    self.equkz("[e]^","f")

################################
