from ukz_tests import *
from ukz.midi import DrumPitch
	
inittests()

# Empty melodies
chkukz("[]",0,0,[])
chkukz("()",0,0,[])
chkukd("[]",0,0,[])
chkukd("()",0,0,[])

# Primitive melody
def chkukPrim(f,s,p):
  ps = p if isinstance(p,list) else [p]
  ls = sorted(list(map(\
   lambda x: (0,1,x,5), ps)))
  chkuk(f,s,0,1,ls)
def chkukzPrim(s,p):
  chkukPrim(ukz,s,p)
def chkukdPrim(s,p):
  chkukPrim(ukd,s,p)
chkukzPrim("c",0)
chkukzPrim("d",2)
chkukzPrim("e",4)
chkukzPrim("f",5)
chkukzPrim("g",7)
chkukzPrim("a",9)
chkukzPrim("b",11)
chkukdPrim('b',DrumPitch.bassPedal)
chkukdPrim('s',DrumPitch.snare)
chkukdPrim('S',[\
 DrumPitch.snare,\
 DrumPitch.bassPedal])
chkukdPrim('S',[\
 DrumPitch.bassPedal,\
 DrumPitch.snare])

# Backward operator
chkukz("c<1",-1,1,[(-1,1,0,5)])
chkukz("c*2<1",-1,2,[(-1,2,0,5)])
chkukz("c.",0,2,[(0,1,0,5)])

equkz("c","c°5")
nequkz("c","c°6")

nequkz("c","d")
nequkz("c","c^")
nequkz("c1","c")

equkz("c","c")
equkz("c1","C")
equkz("e^","f")
equkz("c^^","d")
equkz("E1","e2")
equkz("D1b","e2vv a^^")

equkz("c","c_1")
equkz("c",".c<1")
equkz("c_2.","c*2")
equkz("c*2_1","c.")
equkz("c*2_1 f","c.gvv")
equkz("()","[]")
equkz("(bc)","[b c<1]")

# Volume gradient time-bounds
equkz("[de]<1o[cC]","[d<1e]o[cC]")
equkz("[de]o[cC]<1","[de]<1o[cC]")
equkz("c[de]<1o[cC]","[(cd)e]o[cC]")
equkz("c[de]<1","[(cd)e]")
nequkz("c[de]<1","[(cd)e]o[cC]")
nequkz("c[de]<1o[cC]","[(cd)e]")
nequkz("c[de]<1o[cC]","co[cC][de]<1")
equkz("c[de]<1o[cC]","c[de]o[cC]<1")

# Length of parallel = last submelody
chkukz("(cd)",0,1,[(0,1,0,5),(0,1,2,5)])
equkz("([cd][efg])a","([cd][efga])")
equkz("([cde][fg])a","([cde][fga])")

# ¬ operator
equkz("[cde]¬","c_3 d_2 e")
equkz("[cd*2e]¬","c_4 d_3 . e")

# x= operator
equkz("cx=3","ccc")
equkz("c [de]x=5","cdeded")
equkz("c*7 [de]/3 x=3","c*7 [dedededed]/3")

# << operator
equkz("c<<c","c")
equkz("c<<(cC)","(cC)")
equkz("c<<[cf]","cf")
equkz("[cd]<<[cf]","cfdg")

# @ op modifier
equkz("[[cd][ef]]@¬","c_2de_2f")
equkz("[cd]@x2","[ccdd]")
equkz("[[cd][ef]]@x2","cdcdefef")

# 2 ¬ in a row, 2 ops
equkz("[ca]¬¬","[ca]¬")

# pipe
equkz("[c|]","c<1")
equkz("[c|d]","c<1d")
equkz("[c|de]","c<1de")
equkz("[c*2d|e*3f]","[c*2de*3f]<3")

equkz("(c|)","c<1")
equkz("(c|d)","c<1d")
equkz("(c|de)","c<1(de)")
equkz("(cg|de)","(cg)<1(de)")

equkz("c<^[3]","d^")
equkz("c<^[15]","D^")
equkz("c<^[15 2]","D^d")
equkz("c<^[1-4]","c^dd^e")
equkz("c<^[15 2-5]","D^dd^ef")
equkz("c<^[2-5-3]","dd^efed^")
equkz("c<^[2-5-3 1]","dd^efed^c^")


testresults()