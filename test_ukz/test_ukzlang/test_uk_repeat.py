from .test_uk_base import TestUkBase

class TestUkRepeat(TestUkBase):

################
# Tests

  def test_repeat_rest(self):
    self.equkz(".x1",".")
    self.equkz(".x3","...")
    
  def test_repeatuntil_wholemultiple(self):
    self.equkz("[cd]x=6","[cdcdcd]")
    self.equkz("cx=3","ccc")
    
  def test_repeatuntil_partialmultiple(self):
    self.equkz("[de]x=5","deded")
    self.equkz("c[de]x=5","cdeded")
    self.equkz("[de]/3 x=3","[dedededed]/3")

  def test_repeatuntil_partialandwholemultiples(self):
    self.equkz("[cd]x=5x=10","cdcdccdcdc")
    self.equkz("[cd]x2x=5","cdcdc")

  def test_repeatuntil_dur(self):
    self.equkz("[cd]_2x=5","[cdcd]_2c_2")

################################
