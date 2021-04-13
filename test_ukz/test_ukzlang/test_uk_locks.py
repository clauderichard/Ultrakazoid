from .test_uk_base import TestUkBase

class TestUkLocks(TestUkBase):

################
# Tests

  def test_lock_transpose_inner(self):
    self.equkz("c;^","c")

  def test_lock_transpose(self):
    self.equkz("[c;]^","c")
    self.equkz("[a;]v2","a")

  def test_lock_transpose_outer(self):
    self.equkz("[[c;]]^","c^")
    self.equkz("[a;]v2","a")

################################
