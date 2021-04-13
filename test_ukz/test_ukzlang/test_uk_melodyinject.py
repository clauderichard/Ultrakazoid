from .test_uk_base import TestUkBase

class TestUkMelodyInject(TestUkBase):

################
# Tests

  def test_melodyinject(self):
    self.equkz("c<<c","c")
    self.equkz("c<<(cC)","(cC)")
    self.equkz("c<<[cf]","cf")
    self.equkz("[cd]<<[cf]","cfdg")
    self.equkz("(cd)<<(cf)","(cfdg)")
    self.equkz("(cd)<<[cf]","(cd)(fg)")

  def test_melodyinject_transposeup(self):
    self.equkz("[cd]<<[cf]^","c^f^d^g^")

  def test_melodyinject_scale1(self):
    self.equkz("[cd]<<[cc^]<$[cg]","cgCG")

  def test_melodyinject_scale2(self):
    self.equkz("[cd]<<[cc^]<$[cg]^3","[cgCG]^3")

  def test_melodyinject_scale3(self):
    self.equkz("[cd]<$[cg]^","[cd]<$[c^g^]")

  def test_melodyinject_durations(self):
    self.equkz("[c_2d_3]<<[cg]",\
      "([cg]*2[.*2([da]*3.*2)])")

  def test_melodyinject_rest(self):
    self.equkz("(cd)<<[c.*2d]","(cd)(.*2)(de)")
    self.equkz("[c.*3e]<<[cf]","[cf][..]*3[ea]")

  def test_melodyinject_gradientsRHS(self):
    self.equkz("[cd]<<[cg~[Ca]]","cg~[Ca]da~[Ca]")

  def test_melodyinject_gradientsLHS(self):
    self.equkz("c~[Cc]<<(ga)","(ga)~[Cc]")
    self.equkz("[cde]~[Cc]<<(ga)","[(ga)(ab)(bC^)]~[Cc]")

  def test_melodyinject_loudnessblend(self):
    self.equkz("[cd]@2<<[[cd]@1]","[cdde]@3")
    
  def test_melodyinject_instrs_right(self):
    self.equkz("[cd]<<[c %g d]","[c %g d % d %g e]")
  
  def test_melodyinject_instrs_left(self):
    self.equkz("[c %a d]<<[cd]","[cd %a de]")
    
  def test_melodyinject_instrs_leftandright(self):
    self.equkz("[c %a d]<<[c %g d]","[c %g d %a d %g e]")

################################
