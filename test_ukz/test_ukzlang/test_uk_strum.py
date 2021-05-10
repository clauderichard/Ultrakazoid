from .test_uk_base import TestUkBase

class TestUkStrum(TestUkBase):

################
# Tests

  def test_durtoend(self):
    self.equkz("[cde]¬","c_3 d_2 e")
    self.equkz("[cd*2e]¬","c_4 d_3 . e")
    self.equkz("[cd]¬[ef]¬","c_2 d e_2 f")
    # 2 ¬ in a row, 2 ops
    self.equkz("[ca]¬¬","[ca]¬")

  def test_durtoend_lag1(self):
    self.equkz("[C.*2]¬","C*3")
     
  def test_durtoend_lag2(self):
    self.equkz("[C.*2]¬v","b*3")
     
  def test_durtoend_lag3(self):
    self.equkz("[C.*2]v¬","b*3")
     
  def test_durtoend_lag4(self):
    self.equkz("[C.*2]¬v[C.*2]v¬","[b*3][b*3]")
     
  def test_durtolagequal_leavelag(self):
    self.equkz("[cd]¬=4","c_4d_3")

  def test_durtolag_setlag(self):
    self.equkz("[cd]¬==4","c_4d*3")

################################
