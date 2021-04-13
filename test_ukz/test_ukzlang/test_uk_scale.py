from .test_uk_base import TestUkBase

class TestUkScale(TestUkBase):

################
# Tests

  def test_expandtoscale(self):
    self.equkz("[cde]<$[ceg]","[cgE]")
    self.equkz("[cd^c^dg^]<$[dfga]","dafgD1")
    self.equkz("[cd^c^dg^]<$[dgfa]","dagfD1")
    self.equkz("[cd^.*2d]<$[dgfa]","da..f")

  # def test_filtertoscale(self):
  #   self.equkz("[c--C]>$[ceg]","[cegC]")
  
  def test_parallelmapintoscales_1(self):
    self.equkz("[cc^d]<€[[(ceg)(faC)(DEF)]*4]", \
     "cegcaCfaFDEF")

  def test_parallelmapintoscales_2(self):
    self.equkz("[cc^d]/4<€[[(ceg)(faC)(DEF)]]", \
     "[cegcaCfaFDEF]/4")
  
################################
