from .test_uk_base import TestUkBase

class TestUkExpand(TestUkBase):

################
# Tests

  def test_expand(self):
    self.chkukz("c*5",5,[(0,5,0,0)])
    self.equkz("c*3/2*4","c*6")

  def test_rest_expand(self):
    self.equkz(".*5",".....")

  def test_expandto(self):
    self.equkz("c=6","c*6")
    self.equkz("[c]=6","c*6")
    self.equkz(".=5",".*5")
    self.equkz("[cde]=1","[cde]/3")
    self.equkz("[cde]=6","[cde]*2")

################################
