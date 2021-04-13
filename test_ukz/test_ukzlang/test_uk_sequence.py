from .test_uk_base import TestUkBase

class TestUkSequence(TestUkBase):

################
# Tests

  def test_simple_sequence_5dots(self):
    self.chkukz(".....",5,[])
  def test_simple_sequence_cdot(self):
    self.chkukz("c.",2,[(0,1,0,0)])
  def test_simple_sequence_dotc(self):
    self.chkukz(".c",2,[(1,1,0,0)])
  def test_simple_sequence_cg(self):
    self.chkukz("cg",2,[(0,1,0,0),(1,1,7,0)])

################################
