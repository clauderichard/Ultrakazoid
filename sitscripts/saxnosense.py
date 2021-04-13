from ukz import *

s = Song(""" bpm 120
	%x alto sax o5 V120 v110
	%d power kit
""")

s.play("""
%d [b.b.s.bsbsb.s.b.]/4 x=64
%d .=32 c

%x [d ev f] << [
[aavggvfeevddvc]<<[d^c] <$ [cdef^avbv] /16
 x=5
[aavggvfeevddvc]<<[d^c] <$ [cdef^avbv] /16 v
 x=8
[aavggvfeevddvc]<<[d^c] <$ [cdef^avbv] /16 v2
 x=3
]
""")

s.write("saxnosense")
