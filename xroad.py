from ukz import *

s = Song("""
  bpm 120
%l elec piano 1 o6 v125
%l fx 3 o6 v115
%sb slap bass 2 o2
%ep elec piano 2 o3


""")

s.play("""
%sb
[ agaC ]*4

%ep [ccv2cd^] << (aEG^C^)*4
""")

s.play("""
%sb
[ a*3 [a..]/3x2 a*2 g*3 [g..]/3x3 a^*3 
  a*3 [a..]/3x2 a*2 [b^a^g]<<[c*2[c..]/3] ]/4

%ep [c*7 cv2*6 c^*3 c*7 [d^c^bv]<<[c*3] ]/4
      << (aEG^C^)
""")

s.play(" .*8 ")

# new smooth sax crap
s.play("""
%sb
[
 f*3 [f..]=1/4 e*3/4
 [f*3 [f..]=1x2 f*2 [gef]<<[c*2 [c..]=1] ]/4
]x2

%ep
(fCAE1)*8
[%l f*3E*2C*3.*8]¬ /2 o1
""")


s.write("xroad")