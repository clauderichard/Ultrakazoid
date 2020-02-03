from ukz import *
	
conv = False
raini = 'rain'
raini = 'pad 1'
rainv = 120
rainv4 = 100
rainv7 = 127
if conv:
  raini = 'pad 1'
  rainv = 65 # 100 still too loud
  # 75 seems sliiightly too loud
  rainv4 = 50
  rainv7 = 75
songname = "snowy"
if conv:
  songname = "snowy_conv"
# real name: "Crystalline Snowscape"

song = Song()
choir = song.newPlayer('choir',4,\
 {5:80})
atmo = song.newPlayer(
	Instr('brightness',4,{5:90}),
	Instr('pad 4',4,{5:90}))
crys = song.newPlayer(\
 raini,5,{4:rainv4,5:rainv,7:rainv7})
rain2 = song.newPlayer(\
 'elec piano 1',5,{
 	4:60,5:80,6:100,7:120})
rain3 = song.newPlayer(\
 'fx 3',5,{5:70,6:90,7:110})
rain4 = song.newPlayer(\
 raini,5,{4:rainv4,5:rainv,7:rainv7})
rain5 = song.newPlayer(\
 'elec piano 1',5,{
 	4:60,5:80,6:100,7:120})
rains2 = Players([rain2,rain3])
 #'elec piano 2',5,{5:70,6:110})])
rain = Players([crys,rain2])
bass = song.newPlayer(
	Instr('voice ooh',4,{5:90}))

################
# Melodies

choirm = """
[(aGA) (gG) (aGA) (gG)
 (fE) (gEG) (aGA) (aEA)
]1 *8
"""
choirm1 = """
[(aEA) (gG) (aGA) (gG)
 (fE) (gEG) (aGA) (aEA)
]1 *8
"""
atmom1 = """[
 [ [aDEGEDaD]¬
   [gCDFDCgD]¬ ] x2
 [fbCECbfC]¬
 [gbCGCbgD]¬
 [aDEAEDaD]¬
 [aDEBEDaE]¬
]"""
crysrainm1a = """
[A*2 EG D*3]*2
[DC]/2 E*7 [DC]/2 G*7
[bC]/2 A*9 G*4 [BC1]*2
"""

################
# Intro

atmo.play(atmom1)
choir.play(choirm)
song.sync()

################
# Crystalline 1

atmo.play(atmom1)
choir.play(choirm)
rain.play(f"""
{crysrainm1a} A*8
""")
song.sync()

################
# Mysterious 1

choir.play("""
[ (a^AA^) (a^GA^)
  (CBvC1) (CAvC1)
  (DGD1) (DGC1)
  (gGB) (gFB)
]1 *8
""")
atmo.play("""
[ [a^CDA^DCa^D]¬
  [a^DEAEDa^E]¬
  [CEFBvFECD]¬
  [avCDFDCavD]¬
  [gCDGDCgD]¬
  [gbCGCbgC]¬
  [gCDGDCgD]¬
  [gbCFCbgD]¬
]
""")
song.sync()

################
# Crystalline 2

atmo.play(atmom1)
choir.play(choirm1)
rain.play(f"""
{crysrainm1a} D1*8 C1*8
""")
bass.play("""
a*8 g*4 [fg]*2
a*6 ef g*6 dc
f*8 cv5*4 d*4
cvvv*8
""")
song.sync()

################
# Mysterious 2

choir.play("""
[ (a^AA^) (a^GA^)
  (CGC1) (CFBv)
  (agA) (aeA)
  (aA) (aAC)
]1 *8
""")
atmo.play("""
[ [a^CDA^DCa^D]¬
  [a^DEAEDa^E]¬
  [CEFC1FECE]¬
  [CDEBvEDCD]¬
  [aDEAEDaD]¬
  [aDEA^EDaD]¬
  [aCEAECaE]¬
  [aCEAC1BA[AG]/2]¬
]
""")
rain.play("""
.*8*6
.*8
[C1BAG]/2 A*6
""")
song.sync()

################
# Storm begin

choirm2 = """
[ (fCE) (gCD) (eDE) (fCE)
  (fCE) (gCD) (eDE) (fCE)
]1 *8
"""
choir.play(choirm2)
atmo.play("""
[
 [fgCECgfgCECgfgC]¬
 [F [gaDEDa]x2 gaD]¬
 [G [eabEba]x2 eab] ¬
 [F fgCECgfgCECgfgC] ¬
 [G fgCECgfgCECgfgC] ¬
 [F [gaDEDa]x2 gaD] ¬
 [G [eabEba]x2 eab] ¬
 [F fgCECgfgCECgfgCG_4] ¬
]1 /2
""")
rain.play("""[
ag
faE*10 E*2DC
D*12 bCba
gbE*8 CbCDEF
E*14 ag
faE*10 E*2DC
D*12 CDEF
GFE*8 EFGFEA
F
]1 /2 <1 _8""")
bass.play("""
[
f*6 af g*6 ag
e*6 de f*6 Ca
f*6 ef g*6 ag
e*6 de f*6 g*2
]
""")
song.sync()

################
# Snowfall 1

choir.play("""
[ (aEA) (gEG) (ebE) (fCE)
  (aEA) (gEG) (ebE) (fCG)
  (dbC) (egC) (fCE) (gCG)
]1 *8
""")
atmo.play("""
[
 [[aDEAED]x2 aDE]¬
 [B [gCDADC]x2 gCD]¬
 [B [eCDGDC]x2 eCD] ¬
 [A [fCDADC]x2 fCD] ¬
 [B [aDEAED]x2 aDE]¬
 [B [gCDADC]x2 gCD]¬
 [B [eCDGDC]x2 eCD] ¬
 [A [fCDADC]x2 fCD]¬
 [A [dbCECb]x2 dbC] ¬
 [G [ebCGCb]x2 ebC] ¬
 [A [fCDADC]x=15 ] ¬
 [B [gDEBED]x=15 C1] ¬
]1 /2
""")
rain.play("""[
.C.baedgaedge*4
.C.DECbDCagCa*4
.C...bCD.CDE.DEF
]1 *2 _8 << (cC)
""")
bass.play("""
[ a*8 g*8 e*8 f*8
] x2
[ d*6 ef e*4 c*2e*2
  f*6 ef g*6 b*2
]°3
""")
song.sync()

################
# Glory?

rain.play("""
[ddcc]vv <<
[
  GCgGvCg .*10
]1 /2 _8 << (cC)
[
 ag
 faE*10 E*2DC
 D*10
]1^3 << (cC) /2 <1 _8
""")
atmo.play("""
[dc]vv << [
 [CDGB.*12]¬
 [CEGD1.*12]¬
]1 /2
[
  [avEvGAv.*12]¬
  [bvFBvD1.*12]¬
]1 /2
""")
bass.play("""
[dc]vv << [
  C*12 [Cg]*2
  c*16
] /2
[av bv]*8
""")
choir.play("""
[
  (cgC) (cgb)
  [ (cgC) (cgb) ]vv
]2 *8
[(avevg)(bvfBv)]2 *8
""")
song.sync()

################
# Glory? 2

crys.play("""[
[EvDEvFGG^]1 /2 _8 <3 << (cC)
[
 GCg GvDa GCg ADa GC Gvg
 GCg GvDa GCg ADa GC Gvg
 [ GCg GvDa ECg GvDa GC Ag
   GCg GvDa GCg ADa BC GD
 ]vv
]1 /2 _8 x2 << (cC)
[
 [cc cvvcvv cc] << [GCgGvDa .*10]
]2 /2 _8 << (cC)

] °4
""")
rains2.play("""[
[EvDEvFGG^]1 /2 _8 <3
[
 GCg GvDa GCg ADa GC Gvg
 GCg GvDa GCg ADa GC GvE
 FEDE.bv.a.*7
 CDCbva.f.e.*4 d.cd
 cgbC.D.E.*8
 gbDE.F^.G.*6
 F^GFGAF.E.D.*7
 CbvCDbv.a.f.*4
 edcd
]1 /2 _8
] °7
""")
rain3.play("""
c1 _8 °7
""")
rain2.play("""[
[
  [cdgb .*12] x2
  [cdgb .*12]vv
  [cgbD .*12]vv
  [cdf^a .*12] x2
]1 /2 _8
]°7
""")
atmo.play("""
[
 [CDGBGDCDGBGDCDGD1_8]¬
 [CEGD1GECEGD1GECEGE1_8]¬
 [ [CGD1G1D1GCGD1G1D1GCGD1G1v_8]¬
   [CGBE1BGCGBE1BGCGBD1_8]¬ ]vv
]1 /2 x2
[
 [CDGB.*12]¬
 [CDGB.*12]¬
 [ [CDGB.*12]¬
   [CGBD1.*12]¬ ]vv
 [CDF^A.*12]¬ x2
]1 /2
""")
bass.play("""
[
  C*8
  C*8
  [ C*8
    C*4 E*4
  ]vv
] x2
""")
choir.play("""
[
  (cgC) (cgD)
  (cvvfE) (cvvfD)
]2 *8 x2
""")
song.sync()

Players([atmo,rain]).play("""
[ CEG^B.*12
  CC^F^A^.*12
  CEvGG^.*12
  CDFBv.*12
  CEGC1.*14
]1 /2 _8 << (cC) °4
""")

song.sync()
################
# Weird

atmo.play("""
[
 [Cbge]x2
 bavge avgec
 [bavge avgec]x2
 [bbvgev]x2 [Cavfc^]x2
 [bavge avgec]x2
]1 *3/4
""")
bass.play("""
[
 c*16 c*16
 d^*8 c^*8
 c*16
]1 *3/4
""")
rain4.play("""[
.*16
[Cbge bgec]x2
[Evbbvgbbvgev] [C^CavfCavfc^]
[Cbge bgec]x2
]1 *3/4 °3
""")
rain5.play("""[
.*16
[Cbge bgec]x2
[Evbbvgbbvgev] [C^CavfCavfc^]
[Cbge bgec]x2
]1 << [[cC]/2_1] °4 *3/4
""")
song.sync()
atmo.play("""[
 [bavge avgec]x4
]1 *3/4
""")
bass.play("""[
 c*32
]1 *3/4
""")
rain4.play("""[
[Cbge bgec]x4
]1 *3/4 °3
""")
rain5.play("""[
[Cbge bgec]x4
]1 << [[cC]/2_1] °4 *3/4
""")
rain.play("""[
[C*8 g*4b*4f^*12 f^eg*2]1 °6
]*3/4
""")
song.sync()
atmo.play("""[
 [bavge avgec]x2
 [Cg^ge g^gec^]x2
 [bavge avgec]x2
]1 *3/4
""")
bass.play("""[
 [cc^c]*16
]1 *3/4
""")
rain4.play("""[
[Cbge bgec]x2
[C^Cg^e Cg^ec^]x2
[Cbge bgec]x2
]1 *3/4 °3
""")
rain5.play("""[
[Cbge bgec]x2
[C^Cg^e Cg^ec^]x2
[Cbge bgec]x2
]1 << [[cC]/2_1] °4 *3/4
""")
choir.play("""[
[(cbC)(c^CC^)(cbC)]*16
]2 *3/4
""")
song.sync()

################
choir.choirize()
song.write(155,songname)
################
