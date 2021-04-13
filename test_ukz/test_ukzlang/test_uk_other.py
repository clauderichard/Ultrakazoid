from .test_uk_base import TestUkBase

class TestUkOther(TestUkBase):

################
# Tests

  def test_loudness_op(self):
    self.equkz("c","c@0")
    self.nequkz("c","c@1")
    self.nequkz("c","c@-1")

  def test_setduration(self):    
    self.equkz("c","c_1")
    self.equkz("c_2.","c*2")
    self.equkz("c*2_1","c.")
    self.equkz("c*2_1 f","c.gvv")
    self.equkz("()","[]")

  def test_hmelpar_length(self):
    # Length of parallel = length of last submelody
    self.chkukz("(cd)",1,[(0,1,0,0),(0,1,2,0)])
    self.chkukz("(c*2d*3)",3,[(0,2,0,0),(0,3,2,0)])
    self.equkz("([cd][efg])a","([cd][efga])")
    self.equkz("([cde][fg])a","([cde][fga])")

  def test_durtoend(self):
    self.equkz("[cde]¬","c_3 d_2 e")
    self.equkz("[cd*2e]¬","c_4 d_3 . e")
    self.equkz("[cd]¬[ef]¬","c_2 d e_2 f")
    # 2 ¬ in a row, 2 ops
    self.equkz("[ca]¬¬","[ca]¬")

  def test_shred_1(self):
    self.equkz("[c--e]","cc^dd^e")

  def test_shred_2(self):
    self.equkz("[c--e--d]","cc^dd^ed^d")
    self.equkz("[c--e--C]","c--C")
    
  def test_shred_nobrackets(self):
    self.equkz("c--eg--e","cc^dd^egf^fe")
    
  def test_shred_withforloop(self):
    self.equkz("[c--e]:x2","ccc^c^ddd^d^ee")
    
  def test_shred_rsharp(self):
    self.equkz("[c--d^]","cc^dd^")
    
  def test_shred_parallel(self):
    self.equkz("(d--f)","(dd^ef)")
    
  def test_backwardbyend(self):
    self.chkukz("c<¬",0,[(-1,1,0,0)])
    self.chkukz("[ce]<¬",0,[(-2,1,0,0),(-1,1,4,0)])

  def test_guill_nested_withreturn(self):
    self.equkz("%t 《c % d》","%t (cd)")

  def test_names_nested_stuff(self):
    self.equkz("%a [c %b [c]d]","%a c %b .cd")

################################
