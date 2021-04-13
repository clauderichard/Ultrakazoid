from ukz import *
# Song name possibly:
#   Nostalgia for the Sun

################################
#     Sections:
# Nostalgia

song = Song("""
	bpm 150
%b slap bass 2 o2
%bb elec finger bass o2
%x alto sax o3 v110
%x bari sax o3 v110
%d power kit v96 
  pv42 110 
  pv44 110
  pv52 80
%o orch hit o4
%l elec piano 1 o6 v100
%l fx 3 o6 v90
%choir choir aahs o4 legato v70

%sfx shanai o1 v120
""")

################################
# Nostalgia

# song.play("""
# 	%sfx [cCFC1C2] << [(ce)*8~[c2c-2]]
# .*4
# """)

song.play("""
%bb
[
a..C*3/2C*3/2..
D..D*3/2D*3/2..
] x2

%l
(
  [ A[AGC1G1]/2C1*2 [DCEFED]/2 o1
    C1*3/2[D..DCEFED]/2o1C1A
  ] _8
) x2

""")

song.play("""
%bb
[
a..C*3/2C*3/2..
D..D*3/2D*3/2..
] x2

%choir
(aA)*3 (GC)*5
(F^D)*3 (GD)*3/2 (F^D)*7/2
a~[e]

%l
(
  [ A[AG1B1G1]/2A1*2 [AGBC1BG]/2o1
    A1*3/2[...DCEFED]/2o1C1A
  ] _8
) x2

""")

song.play("""
%bb
[
a..C*3/2C*3/2..
D..D*3/2D*3/2..
] x2

%d [h^*2hhh^*2hhh^*2hhhh]/4 x=8 x4
%d [b.sb[.b..]/2sb ] x4

%choir
(aA)*3 (GC)*5
(F^D)*3 (GD)*3/2 (F^D)*7/2
a~[e]

%x
[ [A*2AGEG]/2 G*2~[cc*2c2*4c2] [A G[EG]*2]/2
  F^*5/2 ~[[cv4c2]x4] ./2
  [D C EF ED [Ca]*2] /2
] o1 x2

""")



song.write("nostsun")