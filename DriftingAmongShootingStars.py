from ukz import *

################################

songName = "Drifting Among Shooting Stars"
song = Players()

actualbass = song.newPlayer( \
  Instr(44,3,{5:45}), \
  Instr(45,2,{5:50}), \
  Instr(33,2,{5:70}) )
bass = song.newPlayer( \
  Instr(4,3,{5:100}), \
  Instr(5,3,{5:80}) )
rain = song.newPlayer( \
  Instr(4,6,{5:110,6:120,7:127}), \
  Instr(2,6,{5:30,6:50,7:70}), \
  Instr(5,6,{5:90,6:105,7:120}) )
choir = song.newPlayer(\
	Instr(44,5,{5:75}), \
	Instr('choir aah',5,{5:80}) )
bell = song.newPlayer( \
  Instr(4,6,{5:100,6:110,7:120}) )

#####################################

actualBassLines = [
  "[e*2edc*2cd]+8 *4",
  "[e*2edc*2cd]+8 *4",
  "[g*2gdc*2cd]+8 *4",
  "[g*2gg]+8 *4"
]
bassLines0 = [
  """[eabD .... eabD daCD
   cf#gb .... cf#gb df#gD]""",
  """[eDF#G .... eDF#G dDF#G
   cbCE .... cbCE dbCF#]""",
  """[gDF#G .... gDF#G dDF#G
   cDF#G.... cDF#G dDF#G]""",
  """[gDF#G .... gDF#G gDF#G]"""
]
for i in range(0,len(bassLines0)):
  bassLines0[i] += " +8 <_ [[c_8c_7c_6c_5][c_4c_3x3]x2]"
bassLines = [
  """[eabDF#Dba eabD daCD
   cf#gbDbgf# cf#gb df#gD]""",
  """[eDF#GAGF#D eDF#G dDF#G
   cbCEGF#ED cbCE dbCF#]""",
  """[gDF#GAGF#D gDF#G dDF#G
   cDF#GAGF#D cDF#G dDF#G]""",
  """[gDF#GAGF#D gDF#G gDF#G]"""
]
for i in range(0,len(bassLines0)):
  bassLines[i] += " +8 <_ [[c_8c_7c_6c_5][c_4c_3x3]x3]"

def playBassLine(lineIndex,playAll=False):
  bassLine = bassLines[lineIndex] \
   if playAll \
   else bassLines0[lineIndex]
  actualBassLine = actualBassLines[lineIndex]
  actualbass.goto(bass)
  bass.play(bassLine)
  actualbass.play(actualBassLine)

#####################################
# Play the song

playBassLine(0,False)
playBassLine(0,False)
song.goto(bass)
#####################################

playBassLine(0,False)
playBassLine(0,False)
playBassLine(0,True)
playBassLine(0,True)

rain.play("""
[ E*8 b*4 C*4 g*16
  G*8 D*4 E*4 b*16
] -4 _8
[
 [[CG]/2 C2*3 .*12] .*16
 [[CG]/2 C2*3 .*12]+3 .*16
] _8
""")

song.goto(bass)
################

playBassLine(1,False)
playBassLine(1,False)
playBassLine(1,True)
playBassLine(1,True)
rain.play("""
[ E*8 b*4 C*4 g*16
  (EG)*8 (bD)*4 (CE)*4 (gb)*16
] -4 _8
[
 [[CG]/2 C2*3 .*12] .*16
 [[CG]/2 C2*3 .*12]+3 .*16
] _8
""")
song.goto(bass)

################

for _ in range(0,4):    
  playBassLine(1,True)

rain.play("""
[ EbDaCbf#gbf#aegdf#g e*16
  GDF#CEDabDaCgbf#ab g*16
] -4 << [[cC]/2] _8
[ [eb]/2 G*31
  [gD]/2 B*31
] +8 _8
""")
song.goto(bass)

################

playBassLine(2,False)
playBassLine(2,False)
playBassLine(2,True)
choir.goto(bass)
playBassLine(2,True)
rain.play("""
[ G*8 D*4 E*4 b*16
  B*8 F#*4 G*4 D*16
  A*8 E*4 F#*4 C*16
] -4 _8
[
 [[CG]/2 E2*3 .*12]+3
] _8
""")

choir.play("""
[
  C (CE) (CEG) (bDGB)
  (CEGC2) (CEGE2) (CFGF2) (CDGBG2)
] *4 +3 -12
""")
song.goto(bass)
################

choir.play("""
[
  (CEGC2)*3 (gbFB)
  (fFAC2)*3 (gbGBD2)
  (CEGCE2)*2 (CEGC2D2) (gbFBD2)
  (fCFAC2F2)*2 (fCFAC2E2) (gbGBF2)
  (CEGC2G2) (CEGC2F2) (CEGC2E2) (gbFBD2)
  (fFAC2F2) (fFAC2E2) (fFAC2F2) (gbGBG2)
  (CEGC2E2C3) (CEGC2F2B2) (CEGC2E2A2) (gbFBD2G2)
  (fFAC2F2A2) (fFAC2E2G2) (fFAC2F2A2) (gCGBD2G2B2)
  (CGBC2G2B2C2) (CGBC2G2B2) (CGBC2G2)*2
  (CGBC2) (CGB) (CG)*2
] *4 +3 -12
""")

playBassLine(2,True)
playBassLine(2,True)
playBassLine(2,True)
playBassLine(2,True)

bellline1 = "[cgbCDgECFECGFEDC cgbCDgECFEDCbDCG]"
rainmline1 = "[gCGGGDGG [CCgCCCgg]+12 gCGGGDGG [CCgggggC]+12]"
bellline2 = "[C2BAGAGFEGFEDFEDC cgbCDgECFEDCbDCG]"
rainmline2 = "[[GGCCCCCC CCgggggg]+12 gCGGGDGG [CCgggggC]+12]"

bell.play(f"""
[
{bellline1}
{bellline2}
] @x2 +3 _8 °6
""")
rain.play(f"""
 [
   ( {bellline1}
     [./3 {rainmline1}]
     [./3x2 {bellline1}+12]
   )
   ( {bellline2}
     [./3 {rainmline2}]
     [./3x2 {bellline2}+12]
   )
] @x2 -9 _8 °6
""")

song.goto(bass)
################

bell.play("""
C2+3 _16 °6
""")
rain.play("""
[[CG]/3C2]+3 _16 °6
""")
#actualbass.play("""
#D# _16
#""")

playBassLine(3,False)
playBassLine(3,False)

song.goto(bass)
################

rain.play("""
[[CG]/3 C2]+3 °7 _16
""")
bell.play("""
C2+3 °7 _16
""")
#actualbass.play("""
#D# _16
#""")

choir.choirize()

tempo = 200
    
song.write(tempo,"DASS")
