from ukz import *

forconvert = False

# StartOfFile
#   Sections:
# Intro1
# Intro2
# PreBattle3Step
# PreBattle4Step
# QuarterNotesAttack
# SixthNotesAttack
# EighthPreAttack
# EighthAttack
# FinalAttack
# SparklingFinale
# EndOfSong
	
	# Exoplanet Obliteration? hmm.
	# Space Blast. That is a good name.
	# It's easy to talk about.
	# Cosmic Blitz describes it better.
	# Space Blast can be the album name

#[volume,vel4,vel5,vel6]
choirVols = [96,76,95,103]
drumVols = [96,80,100,107]
trumpVols = [96,80,100,107]
pianoVols = [96,96,120,122]
bassVols = [96,96,120,122]
strVols = [96,96,120,122]
#strVols = [96,0,0,0]
orchVols = [96,96,120,122]
bellVols = [96,96,120,127]
rain1Vols = [96,88,110,125]
rain2Vols = [96,72,90,105]
whisVols = [100,100,115,125]
gunVols = [100,100,115,125]
drumVelAdjs = []
drumVelAdjs = [\
   (38,5),(59,10)]
if forconvert:
  choirVols = [96,76,95,103]
  drumVols = [80,64,80,90]
  trumpVols = [96,80,100,107]
  pianoVols = [123,110,127,127]
  bassVols = [96,110,120,125]
  strVols = [96,110,115,120]
  #strVols = [96,0,0,0]
  orchVols = [96,96,120,122]
  bellVols = [105,96,120,123]
  rain1Vols = [96,80,100,120]
  rain2Vols = [96,64,80,100]
  whisVols = [85,100,100,100]
  gunVols = [96,100,115,125]
  drumVelAdjs = [\
   (36,5),(38,22),(52,-15),\
   (53,15),(55,15),(59,30)]

songname = "Cosmic Blitz"
if forconvert:
  songname = songname + " forconvert"
	
song = Song()
piani = MidiInstrument(0,3)
bassi = MidiInstrument(\
	electricBassFinger,3)
stringsi = MidiInstrument(\
	44,3)
piano = song.addTrack(\
	Instrument([piani,bassi,stringsi]))
drums = song.addDrumsTrack()
choir = song.addTrack(choirAahs,5)
trump = song.addTrack(trumpet,5)
bell = song.addTrack(tubularBells,3)
yah = song.addTrack(orchestraHit,2)
rain1i = MidiInstrument(4,6)
rain2i = MidiInstrument(5,6)
rain = song.addTrack(\
	[rain1i,rain2i])
whiss = [song.addTrack(whistle,7)]
gun = song.addTrack(gunshot,3)
drums.name = "Drums"
bell.name = "Bell"
rain.name = "Rain x2"
trump.name = "Trump"
choir.name = "Choir"
piano.name = "Piano x3"
gun.name = "gun"

#piano.enabled = False
#trump.enabled = False
#drums.enabled = False


#trump.enabled = False
#piano.enabled = False

################
# Intro1

pib1 = """
[ c*5/2 ./2 [ccc]=1 ]
"""
pib2 = """
[ c*3/2 ./2 [cc]=2 ]
"""
pib2up = """
[ c*3/2 ./2 [cd]=2 ]
"""
pib2dn = """
[ c*3/2 ./2 [cc-2]=2 ]
"""
pib = f"[{pib1} {pib2}]"
pibup = f"[{pib1} {pib2up}]"
pibdn = f"[{pib1} {pib2dn}]"
piano.play(f"""
[
[(c)] << {pib}
[(c)] << {pib}
[(cg)-4x2] << {pib}
[(cg)+1] << {pib}
[(cg)+1] << {pibup}
[(cg)+5] << {pib}
(cg)+5 *8
]&4
""")

bell.play("""
.*60
(cC) +24+5
""")

drums.play("""
[
 [G..GGGG.. Lx3]=4
 [L..GGGG..G..]=4
 [G..GGGG.. Lx3]=4
 [L..GGGG..G..]=4
] x3
[
 [G.. GGG G.. Lx3]=4
 [L.....G..G#..]=4
]
C#*3 [g#x3]=1 (Gg#)*4
""")

trm1 = f"""
[
(CG)*5/2 ./2
[(CG).]x3=1
[[(CA)..]=2[(CF).]=1]=1
(aC)*5/2 ./2

(CGA#)*5/2 ./2
[(CGA#).]x3=1
[[(CFA)..]=2[(CF).]=1]=1
(CAC2)*5/2 ./2
]
"""
trm2 = f"""
[
(CG)*5/2 ./2
[(CG).]x3=1
[[(DF#)..]=2[(aD).]=1]=1
(f#a)*5/2 ./2

(CG)*5/2 ./2
[(CG).]x3=1
[[(DF#)..]=2[(aD).]=1]=1
(F#A)*5/2 ./2
]
"""
trump.play(f"""
[
{trm1}
{trm2}-4
{trm2}+1
[ (CG) <<
 [
  c*5/2 ./2 [c.]x3=1
 ]
 [
  (CF)*3/2 ./2 [(CFA)*2.]=2
 ]
 (CEG)*4
]+5
]°4
""")

#song.write(120,"a1")
song.goto(drums)
################
# Intro2

piano.play(f"""
[
[(cg)-4] << {pib} x2
[(cg)-2] << {pib}
[(cg)-2] << {pibdn}
[[(cg)-6] << {pib}]
[(cg)-4] << {pib}
[(cg)-2] << {pib}
(cg)*4-2
]°4
""")

trm3 = f"""
[
[[(CE).]=1 . [(CF#).]=1]=1 <1

(CG)*5/2 ./2
[(CG).(CA).(CG).]=1
[[(DF#)..]=2[(aD).]=1]=1
(f#a)*5/2 ./2

[(CG)...]=2/3 [(CF#).]=1/3
 (CG)=5/3 ./3
[(CG).(CA).(CG).]=1
[[(DF#)..]=2[(EG).]=1]=1
(F#A)*5/3 .*4/3
]
"""
trm3f = f"""
[
[[(CE).]=1 . [(CF#).]=1]=1 <1

(CG)*5/2 ./2
[(CG).(CA).(CG).]=1
[[(DF#)..]=2[(aD).]=1]=1
(f#a)*5/2 ./2

[(CG)...]=2/3 [(CF#).]=1/3
 (CG)=5/3 ./3
[(CA).(CG).(CF#).]=1
(CG)*2 ..
]
"""
trm5f= f"""
[
[(EB)...(DA).]=1<1
[(CG)=5 .]=3
[(CE).(CE).(CG).]=1
[(GC2)(GB)(EA)(EG)] << [c*5] =4
]
"""
trm5g= f"""
[
[(CG)=5 .]=3
[(CE).(CE).(CG).]=1
[(GC2)(GA#)(EA)(EG)]=4
]
"""
trump.play(f"""
[
{trm3}-4
{trm3f}-2
{trm5f}-6
{trm5g}-4
[
 [(CEG)=8.]=3
 [(gCE)x2(CEG)] << [c.] =1
 (CFG#)=2 (CEG) (CDF)
 (gCE)*4 .*4
]-2
]°4
""")

bell.play("""
[c d] <<
(CC2) <<
[
 .*6 Da C*8
] -4 °4
.*28 (CC2)+10*4
""")

drums.play("""
[(G)..GGG (C) .. Lx3]=4
[L..GGG G .. G..]=4
[
 [G..GGG (C) .. Lx3]=4
 [L..GGG G .. G..]=4
]x2
[
 [C.. GGG G.. G#x3]=4
 [G#.. ... G.. G..]=4
]x1
[
 [C#..LLL L.. GGG]=4
 [G..LLL G .. G..]=4
]x2
C=1 [Lx3]=1 L
[Gx3]=1 G . C# C
(CC#)=3 [Gx3]=1
C*2 ( [T4T4T3T3T2T2] ) @=2
""")

#song.write(120,"a2")
song.goto(drums)
################
# PreBattle3Step

yah.play(f"""
[ (Cc2)*8-3 ] x7
""")

trm5 = f"""
[
 [(CG)*5.]=1
 [(CG).(CG).(CF#).]=1
 [(CG)=5.]=4
 [(CA#)*2(CA)(CG#)(CG)(CF#)]=2
 (CG)*4 .*4
]°9/2
"""
trump.play(f"""
[
 .*16
 [{trm5}] -3 x2
]°9/2
""")

piano.play(f"""
[
 [C [C.]x3=1 D# C#]
 [C [C.]x3=1 [C#DG#bF#C2]=2]
]-15 x6
[
 [D#DC]=1 [b.]=1
 [a#ag#g f#=2 ..]/4
 [cc#f#g [cc#f#g]+1]/4
 [a#ag#gd#dc#c]/4
]-3
""")

drums.play("""
(
 [
  [G..bbbG.. C..]=4
  [G..bbbGbb[bbbbbb]=3]=4
 ] x6
 t1
 c
)
([[Gbb]=1 [L.]=1]) @x=2
([[Gbbb]=1 [G#.l.]=1]) @x=2
(b/4 [[t4t3t2t1]@x4=4]) @x=4
""")

bell.play(f"""
[ c*8	g C# C*6 ] x3 <<(cC) +9
	""")

song.goto(drums)
################
# PreBattle4Step

yah.play(f"""
(Cc2)*8-4 x8
""")

piano.play(f"""
[
 [
  [C [C.[C.]x2=2]=1 D# C#]
  [C [C.[C.]x2=2]=1 [C#DGG#bF#BC2]=2]
 ] x7
 [C [C.[C.]x2=2]=1 D# C#]
 [C [C.[C.]x2=2]=1
  [A#AG#G[DC#C]=4]=2 ]
] -16
""")

drums.play("""
[
 [G...b.bbG*4 C.l.]=4
 [C#*4b.bb]=2
 ([bx12] [h^.lg#]) @=2
] x7
 [G...b.bbG*4 C.l.]=4
 [C#*4b.bb]=2
 (
 	 ([bx12] ) @=2
 	 [t4t3t2]@x2=1
 	 [. (lt1)x3=1 ]
 )
""")

bell.play("""
[CgCgCgCf#] <<
[
.*3 (CC2) .*4
] -4
""")

choir.play("""
.*32
[
 [(cg)=4(cf#)=3(cg#)]=16
 [(cg)=6(ca#)=2]
 [(cf#a)=6]
] -4 +12
""")

song.goto(drums)
################
# QuarterNotesAttack

bell.play(f"""
(CC2C3)*8-5
""")
pianQtrNotes = """
[cc#cg# [cc#]x2 cgf# cc#cf#g]/4
"""
piano.play(f"""
{pianQtrNotes}-5 x12
{pianQtrNotes}-9 x2
{pianQtrNotes}-7 x2
{pianQtrNotes}-5 x4 x2
""")

drums.play("""
C*8
( b/8 [[l..]x4l.l.]=4 ) @x=4
( b/8 [t4t3t2]!x6=2 ) @x=2
( b/12 l/3 ) @x=2
( b/12 c*16 [.s]=1/2 l/4 ) @x=32
( b/12 c*16 g [.s]=2 l/4 ) @x=16
( b/12 c*16 g [.s]=4 l/4 ) @x=16
( b/12 c*16 [h^g] [.s]=4 l/4 ) @x=12
( b/12 
	 [.=2 [t4t3t2t1]@x6 =2 ]
	 [h^g] [.s]=4 l/4 ) @x=4
""")

choir.play("""
.*16
(C [GF#G[G#F#]=1]=1 C2) *32 -5
(f [Cb]=1 F) *8 -2
(g [DD#]=1 G) *8 -2
(C [G*2G#F#]=1 C2) *16 -5
(C [GG#A#B]=1 C2) *16 -5
""")

chgx = """
[
[C.Cx3.[C.]x2 b.]=2
C*7/2
./2
[D#*2DC#Cb]=2
C=3 .*5
] << (cg)
"""

trump.play(f"""
.*32
{chgx}-5
.*16
{chgx}-5 x2
""")

song.goto(drums)
################
# SixthNotesAttack

chg2 = """
[
[C.Cx3.[C.]x2 b.]=2
C*7/2
./2
[D#*2DC#Cb]=2
C=3 .*5
] << (cgC)
"""

bell.play("""
(CC2)-5*8
.*72
[(CC2)(gG)]x4+1 °4
[(EE2)(CC2)]x2+1 °4
[(F#F#2)(DD2)]x2+1 °4
[(CC2C3)]+5 *8
.*8
[ Cgd#g bgd#g a#gd#g agd#d
]+5 °4 << (C2C)
""")

pim = """
[ [cc#]x3 dcc#g#cc#f#
  [cc#]x2 gf#c#c ] =7/2 _*3/2
"""
pim3 = """
[ [cc#]x3 ecc#C#cc#b
  [cc#]x2 Cbc#c ] =7/2 _*3/2
"""
piano.play(f"""
c-5*8
[{pim}x=7 [d#dc#]=1 ]-4
{pim}-4 x=15
[d#dc#]=1 -4
{pim}-6 x=14
[fec#dg#D#]-8=2
{pim}-7 x=32
{pim3}-11 x=16
{pim}-7 x=30
[fec#dg#D#]-9=2
""")

drums.play("""
C*8
( b/6 l ) @x=4
( b/6 l [.r]=1 ) @x=3
( b/3 s/3 g/3 ) @x=1
( b/12 c*16 [.s]=1/2 l/6 ) @x=15
( b/12 g/3 s/3 l/6 ) @x=1
(cbg)=4
( b/12 [r]=2 ) @x=4
( b/12 [(r)(l)]=2 ) @x=4
( b/12 [(gr)(l)]=1 [t4t3t2]@x6=2 ) @x=2
[Gx5 (C#s)]=2
(
 ( b/12 c*16 [.s]=1/2 l/6 ) @x=32
 [.*30 [t4t3t2t1]@x6=2]
)
( b/12 c*8 [.s]=1/2 l/6 g# ) @x=8
( b/12 [.s]=1/2 l/6 g# ) @x=8
[g/2]<1/2
( b/12 c*16 [.s]=1/2 l/6 ) @x=16
( b/12 c*16 [.s]=1/2 l/6 ) @x=14
[Gx5 (C#s)]=2
""")

choir.play("""
(C C2 [D#*2DC#]=1 G)*8 -5
.*8
(C D# G [C2BC2[C2#B]=1]=1 )*16 -4
.*16
(C D# G [C2BA#A]=1 )*16 -7 x2
(C D# g#
	[(C2G#)(D2A#)(D#2C2)(D2F2)]=1
	) =16 -7
(C D# G
	[C2BA#A]=1
	[G2*6A2#A2]=1 ) =16 -7 x2
""")

trump.play(f"""
.*64
{chg2}-7
.*16
{chg2}-7
""")

song.goto(drums)
################
# EighthPreAttack

bell.play(f"""
(CC2#C3)-7*8
""")

p4m = """
[
cc#cc# gf# cc# f#f cc#d#dc#c
f#g cc# gg# d#d c#ag#g cc#bC
]=4 _*2
"""
pii1 = """
[
 D#DCbCGC#2C2D#2D2C2BC2*2
]/4 -7
"""
piano.play(f"""
C-7*8
{p4m}-7 x=8
.*2
""")

dri = """
([bb]=1gs[ll]=1) /4
"""
drums.play(f"""
C*4
(
	b/16 x=12
	[
 	( l=2 ) @x=4
 	( l=2 [.g]=2 ) @x=4
 	( l=2 g ) @x=2
 	( l=2 [ggg[gc#]=1]/2 ) @x=2
 ]
)
""")

choir.play("""
(C D# F# G C2 C2# G2 )*8 -7
""")

song.goto(drums)
################
# EighthAttack

pii = f"""
[
 {p4m}-7 x=7/2
 F#-7 /2
 {p4m}-7 x=2
 [D#DCbCGC2#.]/4 -7
]
"""
piifinal = f"""
[
 {p4m}-7 x=7/2
 F#-7 /2
 {p4m}-7 x=2
 [D#DCbCGC2#C2D#2D2C2BC2*2.*2]/4 -7
]
"""
piano.play(f"""
{p4m}-7 x=16
{pii}x2
{p4m}-7 x=16
{pii} {piifinal}
""")

dr8fac = 8 if forconvert else 6
dr1 = f"""
( b/16 c*16 [.s]=1/2 l/{dr8fac} )
"""
dr2 = """
( b/16 g/2 c*16 [.s]=2 )
"""
dr3 = f"""
( b/16 c*16 [.s]=1/2 l/{dr8fac} )
"""
dri2 = """
( [bb]=1 g s [ll]=1 ) /4
"""
dri = f"""
[
 {dr2} @x=7/2
 (C#)/2
 {dr2} @x=2
 {dri2}x7 (C#)/4
]
"""
dri4 = f"""
[
 {dr2} @x=7/2
 (C)/2
 {dr2} @x=2
 {dri2}x12 [(sC)(C#)]/2
]
"""
drums.play(f"""
(
{dr1} @x=16
[ .*31/2 g#/2 ]
)
{dri}x2
(
 {dr3} @x=16
 [.*8 [t4t3t2t1]@x16=8 ]
 [ .*31/2 g#/2 ]
)
(
 [ {dri} {dri4} ]
 [ .*12 [t4t3t2t1]@x8=2 ]
)
""")

choir.play(f"""
[
(C D# F# [GG#AA#]=1
	[GG#AA#]=1+12°4 C2 )=16
(C D# F# G C2 G2°4 B2°4 )=7/2 ./2
(C D# F# G C2 G2°4 B2°4 )=2 .*2
.*8
(C D# F# G C2 G2°4 C3 )=16
[
 (C D# F# G C2 G2°4 C3 )=7/2 ./2
 (C D# F# G C2 G2°4 C3 )=2 .*2
] x2
]-7
""")

belli = """
.*7/2
[
(F#F#2)-7 *17/4
(CC2C3)-7 *15/4
]x2
"""
belli2 = """
.*7/2
[
(F#F#2C#3F#3)-7 *17/4
(CC2G2C3C4)-7 *15/4
]
[
(F#F#2C#3F#3)-7 *24/4
(CC2G2C3C4)-7 *15/4
]
"""
bell.play(f"""
.*16
{belli}
.*9/2
[C2GBGA#GAG]-7°4 <<(CC2)°6
{belli2}°6
""")

song.goto(drums)
################
# FinalAttack
#song.reset()

bell.play(f"""
[ [ce]<<[cfg] $$ [cdefgab]
]-6 /2 x=8
[ [ce]<<[cfg] $$ [cdefgab]
]-6 /3 x=8
[ [cde]<<[cfgC] $$ [cdefgab]
]-4 /4 x=8
[ [cde]<<[cefgCE] $$ [cdefgab]
]-2 /6 x=8
""")

dr1 = """
( b/24 (gc)*16 l/8 [.s]=1/4 )
"""
dr2 = """
( b/24 (gc)*16 l/8 s/6 )
"""
dr3 = """
( b/24 (gc)*16 l/8 s/8 )
"""
dr4 = """
( b/24 (gc)*16 l/8 s/12 )
"""
if not forconvert:
  dr1 = """
  ( b/24 (gc)*16 l/4 [.s]=1/4 )
  """
  dr2 = """
  ( b/24 (gc)*16 l/4 s/6 )
  """
  dr3 = """
  ( b/24 (gc)*16 l/4 s/8 )
  """
  dr4 = """
  ( b/24 (gc)*16 l/4 s/12 )
  """
drums.play(f"""
{dr1} @x=16
{dr2} @x=8
(
[ {dr3}@x=4 {dr4}@x=4 ]
[t4t3t2t3t2t1] @x16 =8
[.*4 gx4]
)
""")

choir.play(f"""
(C E F# G C2
	[C3B2C3[C3#B2]=1] =1
)-6 =16
(C E F# G C2
	[C3B2A2G2] =1
)-4 =8
(C E F# G C2
	[C3B2A2G2] =1
)-2 =8
""")

piandurop = "_*3" if forconvert else ""
pm1 = f"""
[ cegf#g#g Cbgcbg f#egf#ec ]/12 {piandurop}
"""
pm2 = f"""
[ f#egf#ec cegf#g#g Cbgcbg ]/12 {piandurop}
"""
pm3 = f"""
[ cc#dc#cc# f#gecc#d
  cc#dc#cc# bCgcc#d ]/12 {piandurop}
"""
piano.play(f"""
{pm3}-6 x=16
{pm3}-4 x=8
{pm3}-2 x=8
""")

song.goto(drums)
################
# SparklingFinale
#if not forconvert:
  #song.reset()
  #bell.enabled = False
  #rain.enabled = False
  #whistle.enabled = False
#song.write(120,"fa")
fwStartT = drums.time

finalbellL1 = "243/4"
finalbellL1Over6 = "243/24"
finalbellL2 = 108
finallag = 20
ffac = "27/20"
fadelengthC = 64
fadelength = 48

gun.play(f"[cf#CF#]<<[cg#df#e]/8")

whiss[0].play(f"""
[
[
[
 ./2 b~1  D~2
 ./2 g~2  E~1
 ./2 a~2  F#~1
] =1
[
 a#~2 ./3 D~1
 G~1  ./3 C~2
 D~1  ./3 g#~2
 C~2  ./3 E~1
] =1
[
 a#~2 D~1  C~2  .
 E~1  A~1  D~1  .
 D#~2 A~1  C~1  .
 D~2  F~1  a#~2 .
]=1
] ={finalbellL1} _3

 [
  (b~1 G~2) C~2 .
  (DA)~2 F~2 .
  a~2 (G~2 b~1)
  E~1 b~1 (F#A)~1
  D~2 (G~2 C~2)
  D~2 (FA)~2
  E~1 G~2 (bE)~1
  .
 ]_3
 [
  (F#A)~1 (CE)~2
  (DA#)~2 .
 ]_4
] !g=1
 [
  (F)~2 (CGEB)~1!g=5
 ] _5
""")
lastTrumpGap = 18
lastFwGap = lastTrumpGap + 13
lastTrumpT = whiss[0].time \
 + lastTrumpGap
whiss[0].play(f"""
 [
  .*{lastFwGap}
  (CBF#E)_7~1 !g=7!h=10
 ]
""")
whvs = whiss[0].splitVoices()
numWhiss = len(whvs)
print(numWhiss)

for i in range(1,numWhiss):
  whiss.append(\
   song.addTrack(whistle,7))
for (instr,vols) in zip(\
	[piani,bassi,stringsi,\
	drums,choir,trump,\
	bell,yah,rain1i,rain2i,gun]\
	+ whiss, \
	[pianoVols,bassVols,strVols,\
	drumVols,choirVols,trumpVols,\
	bellVols,orchVols,\
	rain1Vols,rain2Vols,gunVols]\
	+ [whisVols]*numWhiss):
  instr.setVolume(vols[0])
  for i in range(1,4):
    instr.setVelAllPitch(i+3,vols[i])
for (p,dv) in drumVelAdjs:
  for l in range(4,7):
    drums.setVel(p,l,min(127,drumVols[l-3]+dv))

i = 0
for whv in whvs:
  whiss[i].notes = whv
  i += 1

rain.play(f"""
[ [C2 GAFGDEC]
  [C2 GAFGDEC]-4
  [C2 GAFGDEC]-2
]@x5 ={finalbellL1}
<< [[cgC]=1 @_*4]
-12 °6
""")

choir.play(f"""
[
 ( C E  G G2 C2 E2     C3 )
 ( C  F G G2 C2  F    B2 )
 ( g# D# G# C2   G#2   C3 )
 ( g# D# G# C2 G G#2   C3 )
 ( a# F A# C2 F2  G2   A#2  )
 ( a# F A# C2 F2 [A2 A#2]=1  )
] ={finalbellL1}

( cegbCEGC2 )+12 ={finalbellL2}
""")

bell.play(f"""
[
 [Cg#a#] <<
 [cd] << [cfg]
 << [cfg]
 << [cfC] << [cgC]
] /8 -12 °5
""")
bellfinm = f"""
[
 [cgf]
 << [cfd] << [cgCe]
]+12 °6 /8 x={finalbellL2}
"""
bell.play(bellfinm)
rain.play(f"""
{bellfinm} _*4 -12
""")

bell.addFadeOut(-fadelength)
rain.addFadeOut(-fadelength)
choir.addFadeOut(-fadelengthC)

# lastdrums
drums.play(f"""
( b c c# g g# ) ={finalbellL1}
( c c# g g#
)
""")
drums.goto(lastTrumpT)
drums.play(f"""
[
[
  [G..GGGG.. Lx3]=4
  [L..GGGG..C#..]=4
]

( b c c# g )*5
] *{ffac}
""")

trump.goto(lastTrumpT)
trump.play(f"""
[
 [ c*5/2 ./2 [c.]x3=1 ] << (CG)
 [ (CF)*3 . (CA)*3 . ]/2
 (CGC2)*7
] °6 * {ffac}
""")

piano.goto(lastTrumpT)
piano.play(f"""
[
 [(cC2)] << {pib}
 (cC2) *7
] °6 *{ffac}
""")

fwEndT = bell.time

def extractPitchBends():
  for wh in whiss:
    v = wh.maxVolume
    for n in wh.notes:
      if n.b != 0:
        wh.pitchBends.append(\
        (n.t,n.t+n.d,n.b,0))
        wh.volumeGradients.append(\
         (n.t,n.t+n.d,v//2,v))
#extractPitchBends()

minGun = 0
maxGun = 60

class X:
  prevGunT = -1
  prevGunTc = 0

def addGun(n,g,h,i):
  if g is None:
    return
  if n.t+n.d == X.prevGunT:
    X.prevGunTc += 1
  else:
    X.prevGunTc = 1
    X.prevGunT = n.t+n.d
  if X.prevGunTc > 1:
    return
  hh = 8 if h is None else h
  ii = floor(minGun + \
   (maxGun-minGun)*(n.t-fwStartT)\
   /(fwEndT-fwStartT)) + n.p-6 \
   if i is None else i
  gun.goto(n.t+n.d)
  if g < 6:
    gun.play(f"""
     [cCC2C3]<<
     [cdef#g#a#CDEF#] << [cg#df#ecg#]
     	/{hh} x={g} +{ii}
     """)
  else:
    gun.play(f"""
    		 [cCC2C3]<<
       [cdef#g#a#CDEF#] << 
       [cg#df#ecg#]
       << (c+{ii} c-12)
     	 /{hh} x={g}
   """)
for wh in whiss:
  wh.processPropsAll(addGun,\
  	'g','h','i')

################
# EndOfSong

choir.choirize()

song.write(120,songname)
