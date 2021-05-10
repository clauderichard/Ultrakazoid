from .test_uk_base import TestUkBase

class TestUkForEachChild(TestUkBase):

################
# Tests

  def test_foreachleftchild_unary(self):
    self.equkz("[[cd][ef]]:¬","c_2de_2f")

  def test_foreachleftchild_expand(self):
    self.equkz("[ceg]:*5","[ceg]*5")
    self.equkz("[cd]:x2","[ccdd]")
    self.equkz("[[cd][ef]]:x2","[cd]x2[ef]x2")

  def test_foreachleftgrandchild_repeat(self):
    self.equkz("[[cd][ef]]::x2","cx2dx2ex2fx2")
    self.equkz("[[cd][[ef]]]::x2","cx2dx2[ef]x2")

  def test_foreachleftleaf_repeat(self):
    self.equkz("[[cd][ef]]!x2","ccddeeff")
    self.equkz("[[cd]ef]!x2","ccddeeff")

################################
