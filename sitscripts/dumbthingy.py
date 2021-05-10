from ukz import *

song = Song("""
	bpm 120
  tpb 32
%b slap bass 2 o2 v120 105 95
%bb elec finger bass o2 v110 100 90 0
%s square o4 v110 100
%s sawtooth o4 v100 90
%t brass section o5 v120 105 90
%t brass section o4 v120 90 75
%d power kit v110 95
  pv42 125
  pv44 125
  pv52 95
  pv36 105
%o orch hit o4 v110
%bell tubular bell o5 v110
%l elec piano 1 o6 v125
%l fx 3 o6 v115
%choir choir aahs o4 legato v80 60
%w whistle o5 v75 85
%w choir aahs o5 v65 75
""")

################################

song.play("""
%d
  [p36 p37p38p39p50p50p48p48p45p45p43p43p41p41 p28p28p28p28p29p29p29p29]/4
  [ [b.b.s.bsbsb. p29 /2x=4 ]/4
    [b.b.s.bsbsb. p52 /16x=4 ]/4 ] x2
  [ [b.b.s.bsbsb. p83 /2x=4 ]/4
    [b.b.s.bsbsb. p76 /16x=4 ]/4
    [b.b.s.bsbsb. p82 /16x=4 ]/4
    [b.b.s.bsbsb. p75 /16x=4 ]/4 ]
    .*4
""")


song.write("dumbthingy")