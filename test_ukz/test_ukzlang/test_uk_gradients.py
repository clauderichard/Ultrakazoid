from .test_uk_base import TestUkBase

class TestUkGradients(TestUkBase):

################
# Tests

  def test_bend_changesomething(self):
    self.nequkz("c~[ab]","c")
    self.nequkz("(c)~[ab]","(c)")
    self.nequkz("[c]~[ab]","[c]")

  def test_bend_vertices(self):
    self.chkukzVG("[ceg]~V[cC]",[(0,3,[(0,0),(1,127)])])
    self.chkukzVG("[ceg]~V[CCc]",[(0,3,[(0,127),(1/2,127),(1,0)])])
    self.chkukzVG("[ [ceg]~V[CCc] a]",[(0,3,[(0,127),(1/2,127),(1,0)])])
    self.chkukzVG("[ [ceg]*2~V[CCc] a]o1^6",[(0,6,[(0,127),(1/2,127),(1,0)])])

  def test_fade_changesomething(self):
    self.nequkz("c~V[ab]","c")
    self.nequkz("(c)~V[ab]","(c)")
    self.nequkz("[c]~V[ab]","[c]")

  # def test_bend_notedur(self):
  #   self.chkukzVGt("c_3~V[cC]",[(0,3)])
  #   self.chkukzVGt("c*3~V[cC]",[(0,3)])

  def test_brackets_inorout(self):
    self.equkz("(c)~[ab]","(c~[ab])")
    self.equkz("(c)~V[ab]","(c~V[ab])")
    self.equkz("[c]~[ab]","[c~[ab]]")
    self.equkz("[c]~V[ab]","[c~V[ab]]")

  def test_emptymel_gradient(self):
    self.chkukzPG("[]~[cC1]",[(0,0,[(0,127//2),(1,127)])])
    self.chkukzVG("[]~V[cC]",[(0,0,[(0,0),(1,127)])])

  def test_silence_gradient(self):
    self.chkukzPG("[.*2]~[cC]",[(0,2,[(0,127//2),(1,(127*3)//4)])])
    self.chkukzVG(".[.*3]~V[cf^cC]",[(1,3,[\
     (0,0),(1/3,127//2),(2/3,0),(1,127)])])

  def test_fades_foreachchild(self):
    vs = [(0,127),(1/2,0),(1,127)]
    self.chkukzVG("c~V[CcC]",[(0,1,vs)])
    self.chkukzVG("""
      [(aCA)*8 (aDA)*3 (a^FA^)*5]:~V[CcC]
     """,[(0,8,vs),(8,3,vs),(11,5,vs)])

  def test_cyclicbend_1(self):
    self.equkz("[cdefg]~~[ab]","[cdefg]~[ababab]")

  def test_cyclicbend_breakmiddle(self):
    self.equkz("[cdefg]~~[ab*2]","[cdefg]~[ab*2aba^]")

  def test_cyclicbend_withleadup(self):
    self.equkz("[cdefg]~~[d*2|ab]","[cdefg]~[d*2abab]")

  def test_equalbend_shorterthanleft(self):
    self.equkz("[cdefg]~=[ab*2c]","[cde]~[ab*2c]fg")

  def test_equalbend_samelengthasleft(self):
    self.equkz("[cdefg]~=[ab*2c*2d]","[cdefg]~[ab*2c*2d]")

  def test_equalbend_longerthanleft(self):
    self.equkz("[cdefg]~=[ab*2c*4d]","(.*5||[cdefg..]~[ab*2c*4d])")

################################
