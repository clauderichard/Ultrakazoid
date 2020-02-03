import unittest
from .test_uk_base import TestUkBase
from ukz import ukz,ukd,Gradient,DrumPitch
from fractions import Fraction

class TestUkMiscellaneous(TestUkBase):

################
# Tests

  def test_sequence(self):
    self.chkukz("..",0,2,[])
    self.chkukz(".....",0,5,[])
    self.chkukz("c.",0,2,[(0,1,0,5)])
    self.chkukz(".c",0,2,[(1,1,0,5)])
    self.chkukz("cg",0,2,[(0,1,0,5),(1,1,7,5)])

  def test_transpose_changesmelody(self):
    self.nequkz("c","d")
    self.nequkz("c","c^")
    self.nequkz("c1","c")

  def test_pitch_transpose(self):
    self.equkz("c","c")
    self.equkz("c1","C")
    self.equkz("e^","f")
    self.equkz("c^^","d")
    self.equkz("E1","e2")
    self.equkz("e1","f1v")
    self.equkz("c1","d1vv")
    self.equkz("D1b","e2vva^^")
    self.equkz("cdefgabC","dvvevvfvgvvavvbvvCvDvv")

  def test_loudness_op(self):
    self.equkz("c","c°5")
    self.nequkz("c","c°6")

  def test_expand(self):
    self.chkukz("c*5",0,5,[(0,5,0,5)])
    self.equkz("c*3/2*4","c*6")

  def test_setduration(self):    
    self.equkz("c","c_1")
    self.equkz("c_2.","c*2")
    self.equkz("c*2_1","c.")
    self.equkz("c*2_1 f","c.gvv")
    self.equkz("()","[]")

  def test_hmelpar_length(self):
    # Length of parallel = length of last submelody
    self.chkukz("(cd)",0,1,[(0,1,0,5),(0,1,2,5)])
    self.chkukz("(c*2d*3)",0,3,[(0,2,0,5),(0,3,2,5)])
    self.chkukz("(c*2||d*3)",0,2,[(0,2,0,5),(0,3,2,5)])
    self.equkz("([cd][efg])a","([cd][efga])")
    self.equkz("([cde][fg])a","([cde][fga])")

  def test_rest_expand(self):
    self.equkz(".*5",".....")

  def test_durtoend(self):
    self.equkz("[cde]¬","c_3 d_2 e")
    self.equkz("[cd*2e]¬","c_4 d_3 . e")
    self.equkz("[cd]¬[ef]¬","c_2 d e_2 f")
    # 2 ¬ in a row, 2 ops
    self.equkz("[ca]¬¬","[ca]¬")

  def test_repeatuntil(self):
    self.equkz("[cd]x=6","[cdcdcd]")
    self.equkz("cx=3","ccc")
    self.equkz("c [de]x=5","cdeded")
    self.equkz("c*7 [de]/3 x=3","c*7 [dedededed]/3")

  def test_expandto(self):
    self.equkz("c=6","c*6")
    self.equkz("[c]=6","c*6")
    self.equkz(".=5",".*5")
    self.equkz("[cde]=1","[cde]/3")
    self.equkz("[cde]=6","[cde]*2")


  def test_melodyinject(self):
    self.equkz("c<<c","c")
    self.equkz("c<<(cC)","(cC)")
    self.equkz("c<<[cf]","cf")
    self.equkz("[cd]<<[cf]","cfdg")
    self.equkz("(cd)<<(cf)","(cfdg)")
    self.equkz("(cd)<<[cf]","(cd)(fg)")

  def test_melodyinject_durations(self):
    self.equkz("[c_2d_3]<<[cg]",\
      "([cg]*2[.*2([da]*3.*2)])")

  def test_melodyinject_rest(self):
    self.equkz("(cd)<<[c.*2e]","(cd)(.*2)(egv)")
    self.equkz("[c.*3e]<<[cf]","[cf][..]*3[ea]")

  def test_melodyinject_gradientsRHS(self):
    self.equkz("[cd]<<[cg~[Ca]]","cg~[Ca]da~[Ca]")

  def test_melodyinject_gradientsLHS(self):
    self.equkz("c~[Cc]<<(ga)","(ga)~[Cc]")
    self.equkz("[cde]~[Cc]<<(ga)","[(ga)(ab)(bC^)]~[Cc]")

  def test_melodyinject_loudnessblend(self):
    self.equkz("[cd]°7<<[[cd]°6]","[cdde]°8")

  def test_melodyinject_locksLHS(self):
    self.equkz("[c&de]<<[ceg]v2","cegcegdf^a")

  def test_pipes(self):
    self.chkukz("(c|)",0,0,[(-1,1,0,5)])
    self.chkukz("(c|d)",0,1,[(-1,1,0,5),(0,1,2,5)])
    self.chkukz("(c|de)",0,1,[(-1,1,0,5),(0,1,2,5),(0,1,4,5)])
    self.chkukz("(cg|de)",0,1,[(-1,1,0,5),(-1,1,7,5),(0,1,2,5),(0,1,4,5)])
    self.chkukz("(cg*2|d)",0,1,[(-2,2,7,5),(-1,1,0,5),(0,1,2,5)])
    self.chkukz("(c|d*2e)",0,1,[(-1,1,0,5),(0,2,2,5),(0,1,4,5)])

  def test_gradients_changesomething(self):
    self.nequkz("c~[ab]","c")
    self.nequkz("(c)~[ab]","(c)")
    self.nequkz("[c]~[ab]","[c]")
    self.equkz("(c)~[ab]","(c~[ab])")
    self.nequkz("(c)o[ab]","(c)")
    self.nequkz("[c]o[ab]","[c]")
    self.nequkz("co[ab]","c")
    self.equkz("(c)o[ab]","(co[ab])")

  def test_gradients(self):
    self.chkukzPG("[]~[cC1]",[(0,0,[(0,-2),(1,2)])])
    self.chkukzVG("[]o[cC]",[(0,0,[(0,0),(1,1)])])
    self.chkukzPG("[.*2]~[cC]",[(0,2,[(0,-2),(1,0)])])
    self.chkukzVG(".[.*3]o[cf^cC]",[(1,3,[\
     (0,0),(Fraction(1,3),Fraction(1,2)),(Fraction(2,3),0),(1,1)])])
    vs = [(0,1),(Fraction(1,2),0),(1,1)]
    self.chkukzVG("""[(aCA)*8
      (aDA)*3(a^FA^)*5]:o[CcC]""",\
     [(0,8,vs),(8,3,vs),(11,5,vs)])

  def test_transposeup(self):
    # On LHS ^n is a special transpose operator,
    # unary since "^n" is just one token in the parser.
    # On RHS ^ by itself is a unary operator.
    # Left should equal c^ transposed up by 5 octaves.
    # Right should equal c transposed up by 61 semitones.
    self.equkz("c ^ 5","c^61")

  def test_foreachchild_unary(self):
    self.equkz("[[cd][ef]]:¬","c_2de_2f")

  def test_foreachchild_binary(self):
    self.equkz("[ceg]:*5","[ceg]*5")
    self.equkz("[cd]:x2","[ccdd]")
    self.equkz("[[cd][ef]]:x2","[cd]x2[ef]x2")

  def test_foreachgrandchild_binary(self):
    self.equkz("[[cd][ef]]::x2","cx2dx2ex2fx2")
    self.equkz("[[cd][[ef]]]::x2","cx2dx2[ef]x2")

  def test_foreachleaf_binary(self):
    self.equkz("[[cd][ef]]!x2","ccddeeff")
    self.equkz("[[cd]ef]!x2","ccddeeff")

  def test_zippedop(self):
    self.equkz("[cd]:<<:[ce(gb)]","cf^(gb)de(aC^)")

  def test_expandtoscale_withlock(self):
    self.equkz("[c&d^.*2dg^]^<$[dgfa]^","dD^..a^G1^")

  def test_startpipe(self):
    self.equkz("c[d|]","(cd)")
    self.equkz("c(d|)","(cd)")
    self.equkz(".[c|de]","cde")
    self.equkz("..[cd|ef]","cdef")
    self.equkz(".*3[c*2d|e*3f]","[c*2de*3f]")
    self.equkz(".[c|d]x3","c(cd)(cd)d")

  def test_endpipe(self):
    self.equkz("c[d||]","cd")
    self.equkz("c[de||]","cde")
    self.equkz("[cd||e]f","cd(ef)")
    self.equkz("(cd*3||)","(cd*3)")
    self.equkz("(cd*3||e)","(ced*3)")

  def test_shred(self):
    self.equkz("[c-e]","cc^dd^e")
    self.equkz("[c-e-d]","cc^dd^ed^d")
    self.equkz("[c-e-C]","c-C")
    self.equkz("c-eg-e","cc^dd^egf^fe")
    self.equkz("(d-f)","(dd^ef)")
    self.equkz("[c-e]:x2","ccc^c^ddd^d^ee")

  def test_expandtoscale(self):
    self.equkz("[cde]<$[ceg]","[cgE]")
    self.equkz("[cd^c^dg^]<$[dfga]","dafgD1")
    self.equkz("[cd^c^dg^]<$[dgfa]","dagfD1")
    self.equkz("[cd^.*2d]<$[dgfa]","da..f")
    self.equkz("(cc^)<$:[[cd^]]","(cd^)")
    self.equkz("(cc^)<$:[[cd^][ce]]","(cd^)(ce)")
    self.equkz("[cd]<$:[[dgfa][cg]]","dfcC")
    self.equkz("c<<:[ce(gb)]","ce(gb)")
    self.equkz("[cd]<<:[ce(gb)]","cdef^(gb)(aC^)")


################################

if __name__ == '__main__':
    unittest.main()