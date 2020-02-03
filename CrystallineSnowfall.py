from ukz import *
	
conv = True
raini = 'rain'
songname = "CrysSnow"
if conv:
  songname = "Crystalline Snowfall"

song = Song()
choirs = []
cryss = []
for _ in range(0,2):
  choirs.append(song.newPlayer(
  	'choir',4,\
   {4:70,5:80,6:105}))
  cryss.append(song.newPlayer(\
   'pad 1' if conv else 'pad 1',
   5, {
   2: 17 if conv else 50,
   3: 30 if conv else 80,
   4: 45 if conv else 100,
   5: 65 if conv else 120,
   7: 75 if conv else 127 }))
choir = choirs[0]
choir2 = Players([choirs[1],
	song.newPlayer('whistle',4,
	{4:50,5:60,6:65})])
[crys,crys2] = cryss

atmo = song.newPlayer(
	Instr('brightness',4,{
		3:60,4:75,5:90}),
	Instr('pad 4',4,{
		3:60,4:75,5:90}))
  
rain2 = song.newPlayer(\
 'elec piano 1',5,{
 	4:60,5:80,6:100,7:120})
rain3 = song.newPlayer(\
 'fx 3',5,{5:70,6:90,7:110})
rain5 = song.newPlayer(\
 'elec piano 1',5,{
 	4:60,5:80,6:100,7:120})
rain6 = song.newPlayer(\
 'elec piano 1',5,{5:120,6:90,7:110})
rains2 = Players([rain2,rain3])
 #'elec piano 2',5,{5:70,6:110})])
rain = Players([crys,rain2])
bass = song.newPlayer(
	Instr('voice ooh',4,{5:90}))
#bass = song.newPlayer(
#	Instr('voice ooh',4,{5:0}))

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
rainmys1 = """[
[a^E^A^.]/2 .*6
[D*4E*2F*2]
[ECA^.]/2 .*6
[G^.GG^]*2
[GFD.]/2 .*6
[D.FG^]*2
G*8
] _8 """
rain2.play(f"""
{rainmys1} °6
""")
rain3.play(f"""
{rainmys1} o[cC]
""")
song.sync()

################
# Crystalline 2

atmo.play(atmom1)
choir.play(choirm1)
rain.play(f"""
{crysrainm1a} D1*8 C1*8
""")
bass.play("""[
a*8 g*4 [fg]*2
a*6 ef g*6 dc
f*8 g*4 D*2C*2
a*16
]
""")
song.sync()

################
# Mysterious 2

choir.play("""
[ (a^AA^) (a^GA^)
  (CGC1) (CFBv)
  (EgA) (aeA)
  (acA) (aAC)
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
rainmys2 = """[
[a^FA^*2]/2 .*6
[D*4E*2F*2]
[ECC1*2]/2 .*6
[G.AA^]*2
[AGE.]/2 .*6
[F...E.G.]
[A*6[EFGA]/2]
[C1BAG]/2 A*6
] _8"""
crys.play(f"""
{rainmys2} o[eC]
""")
rain2.play(f"""
{rainmys2}
""")
rain3.play(f"""
{rainmys2} o[C.gc]
""")
bass.play("""
[ bv*16
  C*16
  a*32
] °4
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
[ag
faE*10 E*2D]_16 C
[D*12 bCba
gbE*8 CbCDE]_16 F°4
[E*14°6 ag
faE*10 E*2D]_16 C
[D*12 CDEF
G]_16 F [E*8 EFGF]_16 E_2 A°4
[F°6]_16
]1 /2 <1""")
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
.C.DEDCbCagCa*4
.C...bCD.CDE.DEF
]1 *2 _8 << (cC)
""")
bass.play("""[
[ a*8 g*8 e*8 f*8
] x2
[ d*6 ef e*6 fg
  f*6 ga g*6 ab
] °5
]
""")
song.sync()

################
# Glory 1

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
bass.play("""[
[dc]vv << [
  C*12 [Cg]*2
  c*16
] /2
[av bv]*8
]
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

atmom1g2 = """
"""
rainmg2 = """[
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
]1 /2
]
"""

crys.play(f"""[
[EvDEvFGG^]1 /2 _8 <3
[
 GCg GvDa GCg ADa GC Gvg
 GCg GvDa GCg ADa GC Gvg
 [ GCg GvDa ECg GvDa GC Ag
   GCg GvDa GCg ADa BC GD
 ]vv
]1 /2 _8 x2
[
 [cc cvvcvv c] << [GCgGvDa .*10]
]2 /2 _8

] °3 <<(cC)
""")
rain2.play(f"""
[{rainmg2}] _8 °7
""")
rain3.play(f"""
[{rainmg2} c1 ] _8 °7 oC
""")
rain2.play("""[
[
  [cdgb .*12] x2
  [cdgb .*12]vv
  [cgbD .*12]vv
  [cdf^a .*12]
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
 [CDGB.*12]¬ x2
 [ [CDGB.*12]¬
   [CGBD1.*12]¬ ]vv
 [CDF^A.*12]¬
]1 /2
""")
bass.play("""
[ c*16 [c*12 e*4]vv ]1
[c*16 [c*12 e*4]vv o[CC]]1
""")
choir.play("""
[
  (cgC) (cgD)
  (cvvfE) (cvvfD)
]2 *8 x2
""")
song.sync()

################
# Postglory Transition

atmo.play(f"""
[ [CDF^A.*12]¬
  [CEG^B.*12]¬
  [CC^F^A^.*12]¬
  [bCFA.*12]¬
  [aC^EA*12 .*16]¬
]1 /2 o[C*4 a^ x2 c]
""")
crys.play("""
[
 [GCgGvDa .*10]
 [G^^EbG^Eb .*10]
 [A^F^CA^F^C^ .*10]
 [AFbAFC .*10]
 [BEaAEa .*10]
] 2 /2 _8 °3 <<(cC)
[Cgeg^gc .*10]1v3 2 /2 _8 °3
""")

song.sync()

################
# Something
effit = False
midtempo0 = 155 if effit else 135
midtempo = 155 if effit else 150
serenityTempo = 155 if effit else 153
tempoInterval0 = 8*6
tempoInterval1 = 24
serenityTempoOffset = 8*7
serenityTempoOffset2 = 8*5

song.gradualTempo(\
	155,-tempoInterval0,
	midtempo0,-2)
song.setTempo(midtempo,-2)
#song.setTempo(\
#	serenityTempo,40)

choirmidvol = "bv"
crysmidvol = "C"
crysmidvol2 = "f^"
atmomidvol = "f^"

choir.play(f"""[
(gCE)*6 (g^CE)*2
(gCE)*6 (aCF)*2
(avCEv)*6 (gCEv)*2
(avCEv)*4 (bvDF)*4
(gCE)*14 (bvDF)*2
(bvEvG)*8
(CEvAv)*6 (DEvBv)*2
(EvGC1)*6 (DFBv)*2
(CEvAv)*4 (DFBv)*4
(CEGC1)*8
(CEvAvC1)*4 (DEvBvD1)*4
(EGBvC1)*6 (DFBv)*2
(CEvAv)*4 (DFBv)*4
(CEvGC1)*12 (DBvD1)*4
]1v3 o [{choirmidvol}{choirmidvol}]""")
somethingm = f"""[
 [Cg^ge....Cg^geg^gec]1
 [Cg^ge....]1 G^GECFECa
 avCEvG....avCEvGCEvGG^
	avCEvG....bvEFBvD1BvAF
	[Cg^ge.*12]1
	[Cg^ge.*12]1
	EvDbvg....[EvDbvg]x2
	EvDbvav....EvDbvavFDCbv
	GEvDbv....GEvDbvBvGEvD
	AvGEvC....GFDCFDCbv
	EDbvg....[EDbvg]x2
	FEvbvav....GFDbvAvFED
	BvGED....BvGEDC1GED
	BvAvFEv....AvGEvDGEvDC
	GEvDC....AvGEvCBvGEvC
	C1GEvC .*12
]1v3 /2 """
crys2.play(f"""
	{somethingm}
	 _4 °3 o[{crysmidvol}]""")
rain5.play(f"""
	{somethingm}
	 _4 °3 o[aa]""")

song.sync()

################
# Serenity

song.gradualTempo(\
	midtempo,-serenityTempoOffset,
	serenityTempo,-serenityTempoOffset2)

choir.play(f"""
[ (cgC)*8 [(cveb)(cveg)]*4
  [(cfa)(cfC)]*4 (cea)*8
  (cfC)*8 (cveb)*4 (cveg)*4
  (cea)*12 (ceC)*2 (cveb)*2
  (cea)*8 (cveg)*4 (cveb)*4
  (cfa)*4 (cfg)*4 (cvvvvvce)*6 (cvvvvvcvd)*2
  (cvvvce)*4 (cvvvcg)*2 (cvvvca)*2
  (cveb)*4 (cveC)*2 (cveb)*2
  ((cf)*8 [aaCa]*2)
  ((cvd)*8 [bbag]*2)
  (cea)*16
]2 o[{choirmidvol}{choirmidvol}]
""")
rainm = """[
  [GF^EC]x4 [GF^Eb]x4
  [AFEC]x4 [AECbFECbabCEABC1E1]
  [CfbfCfDgEaDgCfbe]1
  [begbEDEFEbDaCgbe]1
  [aceaCbCDEDCbCbag]1
  [a*8 (ce)*4 (gb)*4]1
  [(ae)ceaCbagaeaCEDCD]1
  [begbEDEF]1[EbDgCfbe]1
  [FCagCagfagfegfed]
   [cdegCDEGC1GEDBGED]
  [(CE).CDEaCF(Ea).CEAGAB]
  [(BE)F^GABGBE1(E1B)...E1D1C1B]
  [(AC1)*6  AGFCagf.(aC).]
  [(bg)*6 gbDbDEG.(GB).]
  [(AE).(CE)(aC)]*4
  [(ae).*15]
]/2 """
rain2.play(f"""
{rainm}1 _3 °6
""")
song.sync()

################
# Pre melancholy
song.setTempo(155,-1)
song.sync()
atmo.play(f"""
[ [[fbCFCb]x=15 G] ¬
  [[gbCGCb]x=15 A] ¬
  [[abEGEb]x=15 A]x2 ¬
  [[fbCFCb]x=15 G] ¬
  [[gbCGCb]x=15 A] ¬
  [[ebCECb]x=15 F] ¬
  [[fbCFCb]x=15 G] ¬
  [[abEGEb]x=15 A]x4 ¬
]1 /2 o[{atmomidvol}C]
""")
choir.play(f"""[
(fEA) (gDG) (aGA) (aEA)
(fCEA) (gDG) (eEG) (fFG)
(aEA) (aEB) (aEA) (aGA)
]1 *8 o[{choirmidvol}C]""")
rainm = """[
.aCba*12
bCDCb*8 bCDCbE
C*16 .*14
] /2 _8 """
rainm2 = """[
CbCba*12 bCDCb*10
bCbageb*8 bCDCbEC*16
.*15 [C*16 b*16 a*16 .]<<(cC)
] /2 _8 """
crys.play(f"""
{rainm}1 oc <1 {rainm2}1
 o[{crysmidvol2}C]
""")
rain2.play(f"{rainm}1 <1 {rainm2}1")
rain3.play(f"""
{rainm}1 oC <1 {rainm2}1 o[Cad]
""")
crys2.play(f"""[
 [ [fgaefgef]°4
   [aaaa]°5
 ]*8 _8
]1 o[{crysmidvol}C]""")
song.sync()

################
# last melancholy
choirm2 = """
[
	 (fCE) (gCD) (eDE) (fCE)
  (fCE) (gCD)
  (eDE) (fCE)
]1 *8
"""
choir.play(choirm2)
choir2.play("""
[
  agbCCbC[DC]/2
]2 *8 °6
""")
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
rainmhigh = """[
[g
faE*10 E*2D]_16 C
[D*12 bCba
gbE*8 CbCDE]_16 F°4
[E*14°6 ag
faE*10 E*2D]_16 C
[D*12 CDEF
G]_16 F [E*8 EFGF]_16 E_2 A°4
[F°6]_16
]1 /2 <1/2 <<(cC°3) """
rainmlow2 = """[
[d
cfC*10 C*2b]_16 a
[b*12 gagf
egC*8 agabC]_16 D°4
[C*14°6 fd
cfC*10 C*2b]_16 a
[b*12 abCD
E]_16 D [C*8 CDED]_16 C_2 F°4
[C°6]_16
]2 /2 <1/2 """
rainmlow = """[
[b
aCG*10 G*2F]_16 E
[F*12 DEDC
bEG*8 EDEFG]_16 A°4
[G*14°6 ag
faE*10 E*2D]_16 C
[D*12 CDEF
G]_16 F [E*8 EFGF]_16 E_2 A°4
[F°6]_16
]2 /2 <1/2 """
rain.play(f"""(
{rainmhigh}
)""")
rain5.play(f"""
{rainmlow2} oC °6
""")
bass.play("""
[
f*6 af g*6 ag
e*6 de f*6 Ca
f*6 ef g*6 ag
e*6 de f*6 g*2
] oC
""")
song.sync()

################
# Snowfall reprise

choir.play("""
[
	 (aE) (gE) (ebE) (fCE)
	 (aEA) (gEG) (ebE) (fCG)
  (dbC) (egC) (fCE) (gCG)
]1 *8
""")
choir2.play("""
[ a[CbagaaCDEEDD]/4
  C[EDCbCCEFGGFF]/4
  [D*6CDE*6DEF*6EFG*8]/8
]2 °13/2 *8
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
.C.DEDCbCagCa*4
.C...bCD.CDE.DEF
]1 *2 _8 << (cC)
""")
rain5.play("""[
.a.geccvdeccvdc*4
.a.bCbagafegf*4
.a...gab.abC.bCD
]2 *2 _8 °6""")
bass.play("""[
[ a*8 g*8 e*8 f*8
] x2
[ d*6 ef e*6 fg
  f*6 ga g*6 ab
]
]
""")
song.sync()

################
# To last glory
song.sync()

song.setTempo(155)

rain.play("""
[
  [GCgFECgf .*8]
  [GCgFECge .*8]
  [GCgF^ECgf^ .*8]vv
  [GCgF^ECge .*8]vv
]1 /2 _8 << (cC)
""")
atmo.play("""
[dc]vv << [
 [CEBD.*12]¬
 [CGCE1.*12]¬
]1 /2 oC
""")
bass.play("""
[dc]vv << [
  C*12 [Cg]*2
  c*16
] /2
""")
choir.play("""
[
  [ccvv] << [(cgD) (cgC)]
]2 *8
""")
song.sync()

################
# Pre-End

song.setTempo(148,-4)
song.gradualTempo(148,6,90,14)
rainm = """[
 ag faE*10 E*2DC
 D*20
]1 ^3 /2 <1
"""
rainm2 = """[
 Cb aCA*10 A*2GF
 G*20
]1 ^3 /2 <1
"""
crys.play(f"""[
( {rainm} °4 {rainm2} °3) << (cC) _8
]
""")
rains2.play(f"""[
( {rainm} °7 {rainm2} °6 ) _8
]
""")
atmo.play("""
[
  [avEvGAv.*12]¬ oC
  [bvFBvD1E1vD1BvFEvD.*10]¬
    °4 o[CC.f]
]1 /2
""")
bass.play("""
[av*8 bv*10 o[CCc]]
""")
choir.play("""
[(avevg)*8
 (bvfBv)*10 o[CC.f]
]2
.*5
""")
song.sync()
song.setTempo(140,-4)

################
# The End

crys.play("""[
[FEFGAB]1 /2 _8 <3 << (cC)
[
 C1GC BGD C1GC D1GD C1G BC
 C1GC BGD C1GC D1GD C1G BC
 [ C1GC BGD C1GC D1GD C1G BC
   C1GC BGD C1GC D1GD E1G C1C
 ]vv 
]1 /2 _8 x2 << (cC)
[
[
 [C1GCBGD .*10]
 [C1GCBGE .*10]
 [C1GCBGD .*10]vv
 [C1GCBGE .*10]vv
 [C1GCBGE .*10]
 [C1GCBGD .*10]
]2 /2 _8 << (cC)
[C1GCBGC .*34]2¬ /2 << (cC)
] o[Ca]
] °3
""")
rains2.play("""[
[FEFGAB] /2 _8 <3
[
 C1GC BGD C1GC D1GD C1G BD
 C1GC BGD C1GC D1GD C1G BE
 [ C1GE BGF^ C1GE D1GF^ C1G BE
   C1GE BGF^ C1GE D1GF^ E1G C1F^
 ]vv
] /2 _8 x2
] °7 << (C)
""")
rains2.play("""[
[
  [Cbgd .*12]
  [Cbge .*12]
  [Cbgd .*12]vv
  [Cbge .*12]vv
  [Cbge .*12]
  [Cbgd .*12]
]1 << (C) /2 _8
[Cbgc .*36]1¬ << (C) /2
] °7 o[Ce]
""")
atmo.play("""
[
 [CDGBGDCDGBGDCDGD1_8]¬
 [CEGD1GECEGD1GECEGE1_8]¬
 [ [CGD1G1D1GCGD1G1D1GCGD1G1v_8]¬
   [CGBE1BGCGBE1BGCGBD1_8]¬
 ]vv
]1 /2 x2 °3 oC
[
 [CDGB.*12]¬
 [CDGB.*12]¬
 [ [CDGB.*12]¬
   [CDGB.*12]¬ ]vv
 [CDGB.*12]¬ x3
]1 /2 °3 o[Cc]
""")
bass.play("""
[ C*16 [C*12 E*4]vv ] x2 o[Ca]
C*8*3 o[ac]
""")
choir.play("""
[
  (cgCD)*2 (cgCE)*2
  (cvvfE) (cvvfE)
   (cvvfD) (cvvfD)
  (cgCD)*2 (cgCE)*2
  (cvvfE) (cvvfE) (cvvfD) (cvvfD)
]2 *4 °4 oC
[
 (cCD)
]2 *8 °4 o[Cc]
""")
song.sync()

################.
choir.choirize()
choir2.choirize()
#bass.choirize()
song.write(155,songname)
################
