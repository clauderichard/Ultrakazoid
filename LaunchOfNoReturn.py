from ukz import Song

#   Sections:
# Intro
# Launch1
# Silence1
# Silence2
# Launch2
# Stars
# OuterSpace

song = Song("""
  bpm	120
%bell tubular bell o4 v127
%hit church organ o2 v120
%hit orchestra hit o2 v127
%trumpet trumpet o4 v127
%s square o4 v127 50 40 30 20
%s2 square o4 v127 100 85
%choir choir aahs o5 v105 127 84 75 legato
%ding elec piano 1 o5 V120 v127 50 75 100 25 127
%breath reverse cymbal o3 v127
%orch orchestra hit o2 v127
%violin violin o5 v75 legato
%drums standard kit v120 105 90 75
  pv 36 100
""")
#%violin string ensemble 1 o5 v100 127 84 75 0 legato

################
# Intro

song.play("""
%choir
[
(daD)*8 (da^D)*4 (dgD)*4
(daD)*8 (da^D)*4 (dgD)*4
(daD)*8 (da^D)*4 (dCD)*4
(daD)*8 (da^D)*4 (dgD)*4
(daD)*8 (da^D)*4 (dCD)*2 (eCD)*2
]@-2
[
(fa^D)*8 (gCE)*8
(aDF)*8 (aDE)*4 (gCE)*4
]@-1

%s
[
  .*4 [D1ADADad.]/4 .*10
  .*4 [D1ADADad.]/4 .*10
  .*4 [D1ADADad.]/4 .*10
  .*4 [F1D1FD1FDf.]/4 .*10
  .*4 [A1D1AD1ADa.]/4 .*10
]@-1 o1 << [c|| .*11 c@-1 .*11 c@-2 .*11 c@-3]
[
  .*2 [A1^F1A^F1A^Fa^.]/4 << [c|| .*11 c@-1] .*4
    [C2G1C1G1C1GC.]/4 << [c@-1|| .*11 c@-2] .*6
  .*2 [D2A1D1A1D1AD.]/4 << [c|| .*11 c@-1] .*2
    .*2 [C2A1C1A1C1AC.]/4 << [c@-1|| .*11 c@-2] .*6
]@-1 o1

%ding
.*16
[D*2 aC g*3 [gfa.]=1]o1 *2 _8
.*16
[F*2 CE bv*3 [bvaC.]=1]o1 *2 _8
.*16
[A*2 E[GF]/2 D*3 [aC]=1]o1 *2 _8
[D*16]o1 *2

%orch
[
  .*32
  [d*3x2..] .*8 .*16
  [d*3x2..] .*8 .*16
  [(df)*3x2..] .*8 .*16
  [(da)*3x2..] .*8 .*16
  [(da^)*3x2..] .*8 [(eC)*3x2..] .*8 
  [(daD)*3x2..] .*8 [(cC)*3x2 ..] .*8
] /2
""")

################
# Launch1

l = 54*2
#gra = "v2 ~V[C*19C*2e]"
gra = "v2"
grac = "^10"
grat = "~V[C*19C*2f]"
# old 15 scale: [dfbvC] [cefg]^
# new: [ef^gb] [df^ga]
p4 = "[[d--b]=8/3 [d^--a]<<[cd]_5/4=4/3]"

song.play(f"""

%bell
[
[
 [ce]*3 [dgD b]*2 e*2 g^*2
 [aC]*3 [DgD a]*2 b*4
 [a^C]*3 [aCA E]*2 D*4
 [CE]*3 [DgD b]*2 [EG^]=4
 [AG]*3 [F^GA D]*2 G*4
 [DC]*3 [aEA G]*2 [F^D]=4
] <<(cC)

] {gra} o-1

%hit
[
[
 c=3 e=3 d=6 a=2 e=4
 a=3 c=3 d=6 f=2 g=4
 a^=3 a1=3 a=6 e=2 d=4
] << (cC)
] x2 {gra}

%choir
[
  (f^b)=2 |
[
  (ef^gC)=3
  (ef^gb)=3
  (df^ga)=6
  (ceab)=2
  (eg^ab)=4
  (a-1dea)=3
  (efgC)=3
  (df^ga)=6
  (cfga)=2
  (dgab)=4
  (fbvCD)=3
  (egab)=3
  (eaCE)=6
  (f^gbE)=2
  (f^ga[F^D]=1)=4
]
[
  (gf^CE)=3
  (gf^bE)=3
  (f^ga[D]=1)=6
  (abCE)=2
  (g^abE)=4
  (eaDE)=3
  (gCEG)=3
  (gaDF^)=6
  (gaCF)=2
  (abDG)=4
  (bvCDF)=3
  (gaCE)=3
  (eaCE)=6
  (f^gbE)=2
  (f^gaD)=4
]

] {grac}

%drums
[
h^  |
( c^*3 l*3 [b*6b.bbb.b*2x3]/6 [h^.[h^h^h^]=1]=3 ) :x=3
( c*3 [h^ll] [b]*3 ) :x=3
( h^ [b.bb[bb]=1 b]/3 [.s]=4 ) :x=6
( h^*2 [(bs)(bt^u^)(btu)]=2 ) :x=2
( c*4 [b.bb[bb]=1 b]/3 [.(sh^)]=4 [h^*3 [lx3]=1] ) :x=4
] x={l}
""")

################################
# Middle1

tralast = "v7"
l2 = 4
l = 16*6 - l2
ldrum1 = 8*8
ldrum2 = l - ldrum1

song.play(f"""
%bell
[ [a^...C...
  D...BG.A
  A^...C1...
  D1..a1D...] v12
  [F^D.aC...
  F^D.aC...] {tralast}
]*2 << (cC)

%hit
[ a^*4 C*2 g*2
  D*4 g*4
  a^*4 C*4
  D*4 D*4
  [D*4 F*2 C*2
  D*4 F*2 C*2] {tralast}
]*2 << (cC)

%choir
[(bvDFA^)*4 (CEGC1)*4]*2
[(DFAD1)*4 (DGbD1)*4]*2
[(bvDF[C1A^]=1)*4 (CEGC1)*4]*2
[(DF^AD1)*4 (D[GF^]=1AD1)*4]*2
[
  [(DF^AD1)*4 (CFAC1)*2 (CEGC1)*2]*2
  [(D[F^*2GF^]=1AD1)*4 (CFAC1)*2 (C/2EGC1)*2]*2
]  {tralast}

%ding
[
  .*1 [e*2d]o1=1 |
  [c*2e]o1=1 B*5
  B [a*2g]o1=1 F^*6
  
  .*1 [G*2F^]=1
  [D*2E]=1 G*5
  G [A*2B]=1 C1^*2 A*4

  .*1 [e*2d]o1=1
  [c*2e]o1=1 B*5
  B [a*2g]o1=1 F^*6
]_8 v2 << (C)
[
  [g.f^e.]o1 /3
]_4 v2 << (C)
[D/3_8 E*16] v2 << (C)
  (
    [
      bD.. ....
      bv... C...
      bD.. ....
      bv... C...
    ] << [c.C@-2]
    [
      DG.. ....
      D... F...
      DF.. ....
      D... F...
    ] << [.c@-1.]
  )/3 o1 _4

%drums
[
( [ll] [.s]=4
	 [.*12
	  [u^.u^u^u^.u.uuu.t^.t^t^t^.t.ttt.]=4
	 ]
	 [c*8c^*8]
	 [b.bbb.]/6
) :x={ldrum1}

( [l*2] [.s]=4
	 [.*12
	  [u^.u^u^u^.u.uuu.t^.t^t^t^.t.ttt.]=4
	 ]
	 [c*4g^*4c^*8]
	 [[b.bbb.b.bbb.]]/6
) :x={ldrum2}

( [l.l.] [.s]=4
	 [u^.u^.u^.u.u.u.t^.t^.t^.t.t.t.]=4
	 b/3
) :x={l2}
  || g
]

""")

################################
# Silence1

song.play(f"""
%choir
[
  (b G)*6
    (bv F)*3
    (a F)*3
  (b D)*3
    (b D)*3
  (a C)*6
  (b D)*6
  (a [EF]=1)*6
  (b G)*6
] @-2

%ding
  (
    [
      gbC b.a
      bvDF DFA
      B.. G..
    ] << [c.C@-2]
    [
      DDF D.E
      DFA FC1F1
      G1.. B..
    ] << [.c@-1.]
  )/3 o1 _4

  (
    [
      [gbC b.g]v2
      gbC D..
      [gbD GED]v2
      D.. G..
    ] << [c.C@-2]
    [
      [DDF D.D]v2
      DDF B..
      [DDG BBB]v2
      B.. D1..
    ] << [.c@-1.]
  )/3 o1 _4

""")

################################
# Silence2

song.play(f"""
%choir
[
  (g b D)
  (f bv D)
  ( (g C E) ||
   )
  ( (g C E) ||
    %ding [g@2 C@1 E]/9@-1 o2 _4
   )
  (g bv Ev)
  (a C F)
  (av C Ev)
  ( (a^ D E) ||
    %ding [bv@2 E@1 Bv]/9@-1 o2 _4
   )
  ( (a^ D F) ||
    %ding [f@2 D@1 F]/9@-1 o2 _4
   )
  ( (a^ D F) ||
   )
  (bv D G)
  ( (a C^ F) ||
    %ding [a@2 C^@1 A]/9@-1 o2 _4
   )
  ( (a C^ E) ||
    %ding [e@2 a@1 E]/9@-1 o2 _4
   )
  (a C^ E)
  (a D^ F^)
  ( (g b F^) ||
    %ding [g@2 b@1 E]/9@-1 o2 _4
    %orch [e]@1 _4
   )
  (g b E)*2
  (g b F^)
  ( (f^ b E)*2 ||
    %ding [b@2 F^@1 B]/9@-1 o2 _4
    %orch [b*2 b*2]@1
    %drums [hx3@-1 hx3]/3 @-1
   )
  (
    (f^ [b*3 [b*11 .]=1 .*2]=1 Ev)*2 ||
    %drums [
      ([h^x3 gx3] [.*3 [(bu)bb(bt^)bb]/3 [(bu^).(bu^)(bu^)(bu^).]/6 ] )
    ]/3 @1
    %s2
      [
        [c--g--c]=1 ^2 <$ [b-1evg] 
        [g--c b--e a--d]=1  <$ [b-1evf^]
      ] @1 ~V[fC]
  )
]*3 @-1

""")

################################
# Launch2

l = 54*2
tgrav = "^12"
tgrac = ""
tgra = ""
gra = f"{tgra} ~V[C*19C*2e]"
grasq = f"{tgra} ~V[C*19C*2f]"
grac = f"{tgrac} ~V[C*19C*2g^]"
grav = f"{tgrav} ~V[C*19C*2g^]"
grat = f"{tgra} ~V[C*19C*2f]"
lafade = "~V[Cba]"
lafadeAfter = "~V[ac]"
lafade2 = "~V[Cbafc]"
# old 15 scale: [dfbvC] [cefg]^
# new: [ef^gb] [df^ga]
p4 = "[[d--b]=8/3 [d^--a]<<[cd]_5/4=4/3]"

song.play(f"""
%trumpet
 [
[
 [c*5.c.ccc.c.c.]<<(fa) (dg). (ea)*18
]o1 /6 ^7
.*12
[
 [c*5.c.cccvv.c.c.]<<(ea) (gb). (gC)*18
]o2 /6
.*12
[
 [c*5.c.ccc.c.c.]<<(fa^) (dg). (ea)*18
]o2 /6
.*12
[
 [c*5.c.ccc.c.c.]<<(fa) (dg). (ea)*18
]o1 /6 ^7
.*12
[
 [c*5.c.cccvv.c.c.]<<(ea) (gb). (gC)*18
]o2 /6
.*12
[
 [c*5.c.ccc.c.c.]<<(fa^) (dg). (ea)*18
]o2 /6
.*12
 ] {grat}

%bell
[
[
 [ce]*3 [dgD b]*2 e*4
 [ac]*3 [dgD a]*2 g*4
 [da]*3 [aca g]*2 d*4
 [ce]*3 [dgD b]*2 e*4
 [aC]*3 [DaD a]*2 b*4
 [a^a]*3 [aCa g]*2 f^*4
] <<(cC)

] {gra}

%hit
[
[
 c=3 e=3 d=6 a=2 e=4
 a=3 c=3 d=6 f=2 g=4
 a^=3 a1=3 a=6 e=2 d=4
 c=3 e=3 d=6 a=2 e=4
 a=3 c=3 d=6 f=2 g=4
 a^=3 a1=3 a=6 e=2 d=4
] << (cC)
]  {gra}

%s
[
 [c--C--c]=3 <$ [cef^g]
 [d--D]v_6/4 x5=3 <$ [cvef^g] {lafade}
   [ || [d--D]v_6/4 x5=3 <$ [cvef^g] {lafadeAfter} ]
 %s2
 [cde]<<[cddv]<<[ddvc]=6 <$ [df^ga]
 [[C--c]x2]_5/4=2 <$ [eabC]
 {p4}=4 <$ [eg^ab]
 [c--C--c]=3 <$ [acde]
 [d--D]v_6/4 x5=3 <$ [fgCE] {lafade}
   [ || [d--D]v_6/4 x5=3 <$ [fgCE] {lafadeAfter} ]
 %s
 [cde]<<[cddv]<<[ddvc]=6 <$ [df^ga]
 [[C--c]x2]_5/4=2 <$ [fgaC]
 {p4}=4 <$ [gabD]
 [c--C--c]=3 <$ [dfbvC]
 [d--D]v_6/4 x5=3 <$ [aEGB] {lafade}
   [ || [d--D]v_6/4 x5=3 <$ [aEGB] {lafadeAfter} ]
 %s2
 [cde]<<[cddv]<<[ddvc]=6 <$ [abce]
 [[C--c]x2]_5/4=2 <$ [ef^gb]
 {p4}=4^ <$ [df^ga]
  
 [c--C--c]^=3 <$ [cef^g]
 [d--D]_6/4 x5=3 <$ [egbF^] {lafade}
   [ || [d--D]_6/4 x5=3 <$ [egbF^] {lafadeAfter} ]
 %s
 [cde]<<[cddv]<<[ddvc]^^=6 <$ [df^ga]
 [[C--c]x2]^_5/4=2 <$ [eabC]
 {p4}=4^ <$ [eg^ab]
 [c--C--c]^=3 <$ [acde]
 [d--D]^2_6/4 x5=3 <$ [cfgE] {lafade}
   [ || [d--D]v_6/4 x5=3 <$ [cfgE] {lafadeAfter} ]
 %s2
 [cde]<<[cddv]<<[ddvc]^^=6 <$ [df^ga]
 [[C--c]x2]^_5/4=2 <$ [fgaC]
 {p4}=4^ <$ [gabD]
 [c--C--c]^=3 <$ [dfbvC]
 [d--D]^_6/4 x5=3 <$ [aEGB] x2 {lafade2}

] {tgra}

%choir
[
  (b)=2 |
[
  (ef^gC)=3
  (ef^gb)=3
  (df^ga)=6
  (ceab)=2
  (eg^ab)=4
  (a-1dea)=3
  (efgC)=3
  (f^gaD)=6
  (fgaC)=2
  (gabD)=4
  (fbvCD)=3
  (egab)=3
  (eaCE)=6
  (f^gbE)=2
  (f^ga[F^D]=1)=4
]
[
  (gf^CE)=3
  (gf^bE)=3
  (f^ga[D]=1)=6
  (abCE)=2
  (g^abE)=4
  (eaDE)=3
  (gCEG)=3
  (gaDF^)=6
  (gaCF)=2
  (abDG)=4
  (bvCDF)=3
  (aCEA)=3
  (aCEA)=6
  (gbEG)=2
  (gaDF^)=4
]

] @1 x={l}  {grac}

%drums
[
( c*3 l*3 [b*6b.bbb.b*2x3]/6 [g.[ggg]=1]=3 ) :x=3
( c^*3 [gll] [b]*3 ) :x=3
( g [b]/12 [.s]=4 ) :x=6
( g*2 [(bt^u^)(btu)(btu)]=2 [.s] ) :x=2
( c*4 [glgl] [bb]/8 [.s]=4 [... lx3=1] ) :x=4

( c*3 l*3 [b*6b.bbb.b*2x3]/6 [g.[ggg]=1]=3 ) :x=3
( c^*3 [gll] [b]*3 ) :x=3
( g [b]/12 [.s]=4 ) :x=6
( g*2 [(bt^u^)(btu)(btu)]=2 ) :x=2
( c*4 [glgl] [bb]/8 [.s]=4 [... lx3=1] ) :x=4

( c*3 l*3 [b*6b.bbb.b*2x3]/6 [g.[ggg]=1]=3 ) :x=3
( c^*3 [gll] [b]*3 ) :x=3
( g [b]/12 [.s]=4 ) :x=6
( g*2 [(bt^u^)(btu)(btu)]=2 ) :x=2
( c*4 [glgl] [bb]/8 [.s]=4 [... lx3=1] ) :x=4

( c*3 l*3 [b*6b.bbb.b*2x3]/6 [g.[c^x3]=1]=3 ) :x=3
( c^*3 [gll] [b]*3 ) :x=3
( g [b]/12 [.s]=4 ) :x=6
( g*2 [(bt^u^)(btu)(btu)]=2 ) :x=2
( c*4 [glc^l] [bb]/8 [.s]=4 [... lx3=1] ) :x=4

( c*3 l*3 [b*6b.bbb.b*2x3]/6 [g.[c^x3]=1]=3 ) :x=3
( c^*3 [gll] [b]*3 ) :x=3
( g [b]/12 [.s]=4 ) :x=6
( g*2 [(bt^u^)(btu)(btu)]=2 ) :x=2
( c*4 [glc^l] [bb]/8 [.s]=4 [... lx3=1] ) :x=4

( c*3 l*3 [c*6c.ccc.c*2x3]/6<<(bs) [g.[(c^s)x3]=1]=3 ) :x=3
( c^ c g b s )*15
]
""")

################################
# Stars

song.play(f"""
%ding
(
[
  b |
  CEG E. D
  DF^A GF^D
  EB EG^B...

  aCE CEG
  F^ED ... .a
  bDG DFBv B..
]o1 << ([c@1.C@-3]=1) _8
[
  e |
  gbC b. a
  gaD aaf^
  aE bEE...

  eaC gCE
  agf^ ... .c
  deb fCD G..
]o1 << ([.C@-2.]=1) _8
)
[A@1 C1@-2 D1@-2 A1@-3]o1 =1 _8

%choir
[
   (f^gCE)=3
   (f^gbE)=3
   (gaDF^)=6
   (bCEA)=2
   (
     (abEG^)=6 ||
     %drums
     [.*3 [h@-3 h@-2 h@-1 h^*3]/3] ~V[g^]
   )
   (deCA)=3
   (fgCE)=3
   (gaDF^)=6
   (gaCF)=2
   (abDG)=3
   (CDFBv)=3
   (aEGB)=3
   ((aCEA)=6||
     %drums [.*1 p84*3] ~V[f^]
   )
] ~V[g^]
""")

################################
# OuterSpace

song.play(f"""

%choir
[
 [ 
   (bv C D F)  =3
   (gv av Dv F)  =3
   (g av bv Ev) =3
   (av Dv Ev F) =4
   (
     (av a b E) =3 ||
     %violin [G^*3 [F^*10 EEv]/4 D*5~V[CCc]]
   )
   (bv b Dv Gv) =3
   (a D E F^) =6
   (
     (g b C D) =3 ||
     %violin [b*3 [C^*10 DE]/4 D*7~V[CCc]]
   )
   (a C^ D E) =3
   ((bv D Ev G) =4 || %drums [. p84*6~V[f]])
   (bv D Ev F) =5
   (
     (C E F G) =3 ||
     %violin [[F*9 GAA^]/4 B*10~V[CCc]]
   )
   (C E F G)v =6
   (D F^ G A) =4
   ( (b E G^ A) =4 ||
     %drums [p84*6~V[f]]
   )
   (
     (b D G A) =4 ||
     %violin [G*4 [A*9 BC1^D1]/4 D1^*12~V[CC*2c]]
   )
   (C^ D E A) =3
 ] ~V[g^f^]
 (
   (C^ D E A)^ =24 ~V[f^f^*4c] ||
    %drums [p84*6~V[c]]
 )
]
""")

################################

song.write('Launch of No Return')