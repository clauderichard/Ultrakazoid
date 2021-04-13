from ukz import *
#yah
# Song name possibly:
#   Level 1 Asteroid Punching

################################
#     Sections:
# Intro1
# MainSlapBass1
# MainMelody1
# MainStars1
# MainSlapBass2
# BossIntro
# BossFight
# BadassPickup
# StupidFast1
# VictoryDance

song = Song("""
	bpm 120
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
# Intro1

song.play("""
%d [(bs)bb(bs)bb(bs)b[u^ut^t]:x2]/4
""")

################################
# MainSlapBass1

song.play("""

%bb
  [ax24 gx8]/4 x4
%b
  [
    aaA1aaE1vaaD1aaC1aaGA
    aaA1aaE1vaaD1ggC1ggG1A1
    aaA1aaE1vaaD1aaC1aaGA
    aaA1aaE1vaaG1ggC2ggG1A1
    aaA1aaE1vaaD1aaC1aaGA
    aaA1aaE1vaaD1ggC1ggG1A1
    aaA1aaE1vaaD1aaC1aaGA
    aaA1aaE1vaa[G1G]x3G1A1
  ] /4

%d c
%d
  [
    [bbsb.bsbb.s.bbs.]x=56 [[shh]x2s(gb)]
    ( [bbsb.bsbb.s.bbs.]x=56) [[(sh^).]x3ss]
  ] /4

%o
  [ a.....g.
    a.....gC
    a.....g.
    a.....g. ]
""")

################################
# MainMelody1

song.play("""
%bb
[ ax7a*2ax7 gx7g*2gx7 
  [ ffffaff g*2CbgCbg*2 ]x2 ]/4 x2
%b
[ ax6a_1/2A*2ax7 gx6g_1/2G*2gx7 
  [ ffFfAfF [G*2CbgCbg*2] ]x2 ]/4 x2

%s
[
 ..A.AEAC1*4B*3A.B*3.BC1BG*7..
 %t ( [ C.C.Cbab*4g*3..
        C.C.CDED*4 b*3g*2 ]
      [ f.f.fecd*4b-1*3..
        f.f.fgab*4 D*3b*2 ]@-2
    )
 % ..A.AEAC1*4B*3A.B*3.BC1D1G1*7..
 %t ( [ C.C.Cbab*4g*3..
        C.C.CDED*4G*3E*2 ]
      [ f.f.fecd*4b-1*3..
        f.f.fgab*4 D*3b*2 ]@-2
    )
    ([A*15. A..A..A*2]
    	 [D*15. C^..C^..C^*2]@-2)
] /4

%d
(
  [cc^]*16
  [
    [ [bbsb.bsbb.s.bbs.]x=32
      [ [sh(hs)shhsh]hsbb(sh)bsh 
        [sh(hs)shhsh]hsbb(sh)bss ]
    ]x2
  ] /4
)
       ||

%o
  [ a...g...[f[...]/4g[.*5]/4]x2 ] x2
""")

song.play("""
%bb
  a*4
  [ [a..]x2 a*2 .egaCbga ]/4
%b
  a*5/2 [aEG^]/2
  [ [A..]x2 A*2 .egaCbga ]/4

%d
  [
    [bbsb.bsbb.s.bbsh]
    [(sg^)hh(sg^)hh(sg^).]
    [.....b(g^s)b]
  ] /4

%o
  [ a... [a*3x3.*7]/4 ]
""")

################################
# MainStars1

song.play("""
%l
[
 [
  [.cfa]/2 [Cb]*3/4 a/2
  g g/2 [d b*9 ]/4
 ]
 [%t
  [..g.C.E.[GF^]*3E.]/4
  [F^*3.F^GF^D*7..]/4
 ]
	[
	 [.cfa]/2 [Cb]*3/4 a/2
  b b/2 [C D*9 ]/4
 ]
 [%t
  [c.c.cde[df^]*4.]/4
  [c.c.cde f^*4 d*3 b-1*2]/4 ^5
  [a*14 .. a..a..aa]/4
 ]
]

%b [
  [ffCfF]*2 [f.]=1 g*2 g f*2
  [ggD]*2 [g.]=1 G*2 G[gbD]*2
  [CgCEG]*2 [C.]=1 E*2 D C*2
  [Dda]*2 [D.]=1 F^*2 F^[agf^]*2
  [ffCfF]*2 [f.]=1 g*2 g f*2
  [ggD]*2 [g.]=1 G*2 G[gbD]*2
  [CgC]*2 [g.]=1 D*2 D[f^aD]*2
  [FCa]*2 [C.]=1 G*2 G[bDG]*2
  [A*5 EDE]*2 [A..]x2 A*2 .*8
]/4 @-1 << (c %bb c@-1)

%bb [
  [ffCff]*2 [f.]=1 g*2 g f*2
  [ggD]*2 [g.]=1 g*2 g[gbD]*2
  [CgCEG]*2 [C.]=1 E*2 D C*2
  [dda]*2 [d.]=1 F^*2 F^[agf^]*2
  [ffCff]*2 [f.]=1 g*2 g f*2
  [ggD]*2 [g.]=1 g*2 g[gbD]*2
  [CgC]*2 [g]=1 D*2 D[f^aD]*2
  [fff]*2 [f.]=1 g*2 g[ggg]*2
  [A*5 EDE]*2 [C^..]x2 C^*2 .*8
]/4 @-3

%o
[fgcdfg]*4
[c*7d*9 f*7g*9]/4
a*4
[a*3x3.*7]/4

%d
(
    c^
 [
  [b.s.bbsb.bs.b.s.]/4 x=36
  [[shhshh(sg^).] .....b(g^s)b]/4
 ]
)

""")

################################
# MainStars2

song.play("""
%o
[dcfg bvC]*4
D*4
[E*3x3.*7]/4

%s
[ 
  a*2 D.[D.]/2x2E F*3 . F. EDE
  C*2C. [E.]/2x2FG*5 .*4

  [%l C*2 F.[F.]/2x2G A*3 . A. GFA
      G*2D. BAGF*5 .*4 ]

  [ %w [D F [F*2]~[c-1*3 c-1 C1*4 C1] ]*8 @1 ]

  [%l A. A. GF^G A*3 D. A.D1.
      [E1D1E1]*3 .*7 ]

]/4

%bb [
  [Aaa[E]_1/2 /2A]*2 A [aEA]*2
  [ [Aaa[E]_1/2 /2A]*2 A [aEA]*2 ]v2
  [ [Aaa[E]_1/2 /2A]*2 A [aEA]*2 ]^3
  [ [Aaa[E]_1/2 /2A]*2 A [EEvD]*2 ]^5
  [ [aa[aaE]_1/2 /2A]*2 A [C^ba]*2 ]v4 o1
  [ [aa[aaE]_1/2 /2A]*2 A [C^DE]*2 ]v2 o1
  [ [Ea[aaE]_1/2 /2A*3/2]*2 a*2 E*2 A*2] o1
  [ [BA]*3 B*6 .  ]o1
]/4 v7 << (c@-2 %b c@-2)
[ f^gg^ ]/4 << (c %b c)

%choir [
  (DFA)(CEG)(FAC)(DGB)
  (bvDF)(CEG)(DF^A)(EG^B) ] *4

%d
  [b.s.bbsb.bs.b.s.]/4 x=16
  [b.s.bbsb.bs.b.s.]/4 x=8
  [b.s.bbsb.b[ut^t]*2]/4 x=4
  [[(hs)..(hs)..(sg^).] .....b(g^s)b]/4
""")

################################
# MainSlapBass2

song.play("""
%bb
  [ax24 gx8]/4 x2
%b
[
    aaA1aaE1vaaD1aaC1aaGA
    aaA1aaE1vaaD1ggC1ggG1A1
    aaA1aaE1vaaD1aaC1aaGA
    aaA1aaE1vaa[G1G]x3G1A1
] /4

%d c@-1
%d
[
[bbsb.bsbb.s.bbs.]x=56 [[(sh^).]x3ss]
] /4

%o
  [ a.....g.
    a.....g. ]

""")

################################
# BossIntro

song.play("""
%t
[c [c.]x3=1 c^ e]
[c [c.]x3=1 c^ e]^3
g^*3 ~~[c|[Cc-1]=1/4]
""")

song.setTempo(180)

song.play("""
%t .~V C

%d
[(c^s)bbsbbsbbsbbsbsb [u^ut^t]:x4]/4
""")

################################
# BossFight

song.play("""
%o
[
    [a......g]*2
    [a.....fg]*2
    [a......g]*2
    [a...C.g.]*2
    [a......g]*2
    [a...d.bv.]*2
    [a......g]*2
    [a...f.g.]*2
] v

%choir [
  [a=28 [fg]=4] <<(cC) 
  [a=24 [Cg]=8] <<(cC) 
  [a=24 [dbv]=8] <<(cC) 
  [a=24 [fg]=8] <<(cC) 
] v

%bb [
 [ [aaaaa*2]x4 aaaag*2a*2 ]x3
   [aaaaa*2]x2 aaaa [fC]*3f*2 [gD]*3g*2 
 [ [aaaaa*2]x4 aaaag*2a*2 ]x3
   [ [aaaaa*2]x2 aaaa ]^3
   [ aaaa [a*2a]x3 a*3 ]v2 
 [ [aaaaa*2]x4 aaaag*2a*2 ]
 [ [aaaaa*2]x2 aaD^aE*3G*3A.C1*3D1^*3D1. ]
 [ [E1*4a*2] [aaaaa*2]x3 aaaag*2a*2 ]
   [ [aaaaa*2]x2 aaaa ]^5
   [ [aaaaa*2] ax4 b*3 a*3 ]^
 [ [aaaaa*2]x4 aaaag*2a*2 ]x3
   [ [aaaaa*2]x2 aaaa ]v4
   [ [aaaaa*2] ax4 C*6 ]v2
] /4 v

%b [
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]*2
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]o1*2
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]*2
 aaaaA1*2 aaaaE1v*2 aaaa F*2ffff G*2ggggG*2gg
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]*2
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]o1*2
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]*2
 CCCCC2*2 CCCCG1*2 CCCC ggggD1*2 gD1^*2gD1^*2 g G*3
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]*2
 aaaaA1*2 aaaaE1v*2 aaD^aE*3G*3A.C1*3D1^*3D1.
 E1*4A1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]*2
 ddddD1*2 ddddD1*2 dddd
   bvx4 Bv*2 bvx4 C1*2 bv Bv*3
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]*2
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]o1*2
 aaaaA1*2 aaaaE1v*2 aaaaD1*2 aaaaC1*2 aaaa[GA]*2
   [[aaaaA1*2]x2 aaaa]v4
   [[aaaaA1*2] aaaa A1^3*6~[[cv4c^4]x4c]]v2
] /4 v

%d  (
  ( h^
   [ b..bs.b...b.s.b.
     b..bs.b...b.s.bb
     b..bs.b...b.s.b.
     b..bs.b...b.sb.b
     b..bs.b...b.s.b.
     b..bs.b...b.s.bb
     b..bs.b...b.s.(bs).
   ] /4
  ) :x=28 ||
  c
) 
""")

song.play("""
%t
[
 e. | [fa]*3C. [DG]*3E.
 [A...]*4 
]/4 v

%d
( b/4 [[sh^h^]x=8[sh^h^]x=7s] /4 ) :x=4

( g*64
  h^
   [ b..bs.b...b.s.b.
     b..bs.b...b.s.bb
     b..bs.b...b.s.b.
     b..bs.b...b.sb.b
     b..bs.b...b.s.b.
     b..bs.b...b.s.bb
     b..bs.b...b.s.b.
     b..bs.bl.bl.sl..
   ] /4
) :x=32

( c^*64
  h^
   [ b..bs.b...b.s.b.
     b..bs.b...b.s.bb
     ([b..bs.b...b.s.b.
       b..bs.b...b.sb.b]
       [.*12 .. l.l..u..u.t^..t^..tt||(tgg^)]
     )
     b..bs.b...b.s.b.
     b..bs.b...b.s.bb
     b..bs.b...b.s.b.
     b..bs.b...g.(s)(gb).b
   ] /4
) :x=32

( c*28 h^
 [   b..bs.b...b.s.b.
     b..bs.b...b.s.bb
     b..bs.b...b.s.b.
     b..bs.b...b.sb.b
     b..bs.b...b.s.b.
     b..bs.b...b.s.bb
     b..bs.[bbb]=4s.[bbb]=4
   ] /4
) :x=28 ||

%l
.*4
(
 [
  .*4 [D1C1E1v]*3/2_4 .*7/2
    [F^EEv]*3/2_4 .*7/2
    [GAB*2/3]*3/2_4
    [(B^)(B)]*4
    (A)*8
 ]v o-1
 .*64
)
.*8
    [ [C1G]*3 A*2 ]v /2 _8.*4
    [ AGEEv ]v /2 _8.*6
    [GEvDa]v /2 _8.*6
    
%t
  .*4 .*32
  .*8 
  .*3
[ 
   .. d^. [eg]*3a. [CD^]*3D.
 [E...]*4 
]/4 v

""")

song.play("""
%d
( b/3 [[s.]x2[u^ut^t]:x2=8]=16 /4 ) :x=4
|| g
""")

################################
# BadassBrass

badbass1 = """ [
  ax8 C*2 ax4 D*4 aaC*2aa [D^DC*2]*2
  aaaaA1*2 aaaaE1v*2 [aaa]=4
  aD1*2aD1^*2 [aaa]=3 D1*2 [C1^C1BBv]=5
] /4 v """
badbbass1 = """ [
  ax8 c*2 ax4 d*4 aac*2aa [d^dc*2]*2
  aaaaa*2 aaaaa*2 [aaa]=4
  aa*2aa*2 [aaa]=3 a*2 [aaaa]=5
] /4 v """
badbass2 = """ [
  a^x4 (A^*2|| %o a^) a^x4 (A^*2|| %o a^) [aaaa]^
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a^x4 (A^*2|| %o a^) a^x4 (A^*2|| %o a^) [aaaa]^
  a*2x2 [C*2 a]=4 A*2 [aa^aA^]=6
] /4 v """
badbass22 = """ [
  a^x4 (A^*2|| %o a^) a^x4 (A^*2|| %o a^) [aaaa]^
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a^x4 (A^*2|| %o a^) a^x4 (A^*2|| %o a^) [aaaa]^
  a*2x2 [C*2 a]=4 A*2 [aavggv]=6
] /4 v """
badbbass2 = """ [
  a^x4 a^*2 a^x4 a^*2 [aaaa]^
  a*2x2 a*2 ax4 a*2 aaaa
  a^x4 a^*2 a^x4 a^*2 [aaaa]^
  a*2x2 [c*2 a]=4 a*2 [aa^aa^]=6
] /4 v """
badbbass22 = """ [
  a^x4 a^*2 a^x4 a^*2 [aaaa]^
  a*2x2 a*2 ax4 a*2 aaaa
  a^x4 a^*2 a^x4 a^*2 [aaaa]^
  a*2x2 [c*2 a]=4 a*2 [aavggv]=6
] /4 v """
badbass3 = """ [
  fx8 C1*2 fx4 E1v*4 ffA*2aa [D*2~[cC*3Cc*4c]C*2]*2
  ggggA1*2 ggggE1v*2 [ggg]=4
  gD1*2gD1^*2 [ggg]=3 D1*2 [D1vC1BBv]=5
  ax4 (A*2|| %o a) ax4 (A*2|| %o a) [aaaa]
  a*2x2 [C*2 a]=4 A*2 [aa^aC1]=6
  ax4 (A*2|| %o a) ax4 (A*2|| %o a) [aaaa]
  a*2x2 [C*2 a]=4 A*2 [aa^aA^]=6
] /4 v """
badbbass3 = """ [
  fx8 f*2 fx4 f*4 fff*2ff [D^DC*2]*2
  ggggg*2 ggggg*2 [ggg]=4
  gg*2gg*2 [ggg]=3 g*2 [gggg]=5
  ax4 a*2 ax4 a*2 [aaaa]
  a*2x2 [c*2 a]=4 a*2 [aa^aC]=6
  ax4 a*2 ax4 a*2 [aaaa]
  a*2x2 [c*2 a]=4 a*2 [aa^aa^]=6
] /4 v """

song.play(f"""
%bell [a-2 *2]v

%choir
[
  [c*4 c^cc^c]*4x2
  [cv4*2 cv2*2 c*4]*4
] v4 @-1

%b  {badbass1}
%bb  {badbbass1}

%t
[ ..C[.D*2.C.D^DC*2]/2 ] v o-1

%d (f^ (
	l
	[b.s.[bs..(bs)...]/2 ]
) :x=16 )
""")

song.play(f"""
%b  {badbass2} 
%bb  {badbbass2}

%d (
	l
	[b.s.[bs..(bs)...]/2 ]
) :x=16
""")
song.play(f"""
%b  {badbass1}
%bb  {badbbass1}

%t
[ ..C[.D*2.C.D^DC*2]/2 ] v o-1

%w
F1*16 v ~[c-2 c-1*10 c-1 c2*4 c2 c-2*15 c-2]
[%l [a^..D..F. E*6 e. f..C..bv. a*8] ]/2 v _2

%d (
	l
	[b.s.[bs..(bs)...]/2 ]
) :x=16
""")

song.play(f"""
%b  {badbass22} 
%bb  {badbbass22}

%d (
	l
	[b.s.[bs..(bs)...]/2 ]
) :x=16
""")

song.play(f"""
%b {badbass3}

%bb {badbbass3}

%w
.*6 F1*18 v ~[c-2 c-1*4 c-1 c-2*8 c-2 c2*8 c2 c-1*16 c-1]

%d (
	l
	[b.s.[bs..(bs)...]/2 ]
) :x=32
""")

################################
# BadassPickup

song.play("""
%choir
 [cv4*4 cv1 c^ ]*4 @-1

%b  [
[
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a*2x2 [C*2 a]=4 A*2 [aa^aA^]=6
] /4 v x2
[
  [ a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa ] ^3
  [ a*2x2 [E*2 a]=4 A*2 ] ^5 [aa^aA^]=6
] /4 v
[
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a*2x2 [C*2 a]=4 A*2 [aa^aA^]=6
] /4 v
[
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a*2x2 [C*2 a]=4 A*2 [aa^aA^]=6
] /4 v x2
[
  [ a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa ] ^3
  [ a*2x2 [E*2 a]=4 A*2 ] ^5 [aa^aA^]=6
] /4 v
[
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a*2x2 [C*2 a]=4 A*2 [aCbbv]=6
] /4 v
]

%bb  [
[
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a*2x2 [C*2 a]=4 A*2 [aa^aa^]=6
] /4 v x2
[
  [ a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa ] ^3
  [ a*2x2 [E*2 a]=4 A*2 ] ^5 [aa^aa^]=6
] /4 v
[
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a*2x2 [C*2 a]=4 A*2 [aa^aa^]=6
] /4 v
[
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a*2x2 [C*2 a]=4 A*2 [aa^aa^]=6
] /4 v x2
[
  [ a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa ] ^3
  [ a*2x2 [E*2 a]=4 A*2 ] ^5 [aa^aa^]=6
] /4 v
[
  a*2x2 (A*2|| %o a) ax4 (A*2|| %o a) aaaa
  a*2x2 [C*2 a]=4 A*2 [aCbbv]=6
] /4 v
]

%w  [
.*32
 G*4 [F^*3 F^*3~[ccCCcc] [EE]*2]/3
 D*20/3~=[c*2/3cC1]
] v o1

%t
.*48 《
 [E.E]=1 | G*7/2 ./2
 [F^*2.F^F^G A.A.F^.]=4  A*4
 %  [
 	[a.a]=1 | C*7/2 ./2
 [D*2.DDE [F^.]x2D.]=4  E*4  ]@-1
》 v

%d (
	 l
	 [.s]
  [b.b..b.b.b.bbbbb b.b..b.b.b.b[bbb]=4]/4
) :x=56
(
	 l
	 [.s]
  [b]/4
) :x=4
(
	 l
	 [s..s..s.sx8]/4
  [b]/4
) :x=4 || c^

%choir
[ (aA)*16 (CG)*4 (DF^)*4 (aE)*8 ]v
[ (a)*8 (a)*8 [CDa]*4 ]v

%bell
[a-1 *2]v
""")

################################
# StupidFast1

song.play("""
%bb
av/4x=32

%b
(
  [[ AC1D1D1^E1AA1E1G1D1^D1*2/3
    AC2A1G1A1E1G1D1^D1C1A^*2/3
   ] *3 _1
   [ [AC1D1D1^E1AA1E1G1D1^E1*2/3]
    [AC2A1E1G1A1E1D1^D1C1A^*2/3]
   ] *3 _1
  ]
  [ [.aa]x=32x2 _3/4 ]x2
) /4 v

%t
[A .*6 [..G.]/4 [A*3C1..A*3G..]/4 A .*4] v
[. . [%s a.e.g*3a]/4o2@-1 .*2 .*2 .*4 [A.|C1*3B..A*6G*4]/4] v
%t
[E .*6 [..D.]/4 [E*3G..E*3D..]/4 E .*4]@-1 v
[E@1 .*5 [E.A.D^*3E]/4 .*4 [E.|G*3F^..E*6D*4]/4]@-1 v
%t
[C^ .*6 [..b.]/4 [C^*3E..C^*3b..]/4 C^ .*4]@-1 v
[C^ .*5 [C^.E.C*3C^]/4 .*4 [C^.|E*3D^..C^*6b*4]/4]@-1 v

%d
[ [(bh^).(bsh^)b] 
] /4 x=32

""")

song.play("""
%bb
a/4x=8
Cv/4x=8

%b
(
  [ [AC1D1D1^E1AA1E1G1D1^D1*2/3]^
    [AC2A1G1C2A1E1G1D1^D1C1*2/3]^3
  ] *3 _1
  [ [[.a^a^]x=32 [.CC]x=32] _3/4 ]
) /4 v

%t
[A .*6 [..A.]/4 [B*3D1..B*3A..]/4 D1 .*3[BvB]/2]
%t
[E .*6 [..E.]/4 [F^*3A..F^*3E..]/4 A .*4]@-1
%t
[C^ .*6 [..C^.]/4 [D^*3F^..D^*3C^..]/4 F^ .*4]@-1

%d
[ [(bh^).(bsh^)b] 
] /4 x=16

""")

song.play("""
%bb
av/4x=16

%b
(
  [ C1^D1D1^E1G1E1C2G1A1E1E1v*2/3
    A C2A1G1A1 E1G1D1^D1C1^C1*2/3
  ] *3 _1
  [ [.aa]x=32x2 _3/4 ]
) /4 v

%t
[C^ .*6 [..b.]/4 [C^*3E..C^*3b..]/4 C^]^11
%t
[A .*6 [..G.]/4 [A*3C1..A*3G..]/4 A]@-1 v
%t
[E .*6 [..D.]/4 [E*3G..E*3D..]/4 E]@-1 v

%d
[ [(bh^).(bsh^)b] 
] /4 x=8

[ [s(bh)(bh)]x8 (sb)x8 
] /4 x=8

""")

song.play("""

%s
[
  [[C2DC1d]<<[FC^a]=3/4]
]x6=8~V[Cd]

%d
(sbg)*10
""")


################################
# VictoryDance

song.setTempo(160)

song.play("""
%d
[g^*4x2 bsb.s.ss]/4
""")

song.play("""
%b
(
  [ [aa]*2 A1.aE1 a*2a.a.
    [f]*4f. F1.fG1 [gEGG^]*2
    [aa]*2 A1.aE1 a*2a.a.
    [f]*4f. F1.fG1 .G[EGG^]*2
  ] /4
) x=40 << (c %bb c)

%t
[ (a@-1C^).. ./2 (f@-1 C) . (g@-1 D) .*3/2
] x=32
(C^@-1E).. ./2 (C@-1 F) . (D@-1 G) .*3/2

%l
.*16
[A.EF C^*4] *2

%d
c^
%d
( [ b...s.bsb.b.s.b.
	  b...s.bsb.b.s.bb
    b...s.bsb.b.s.b.
	  b...s.bsb.b.s.ss
	 ] /4
	 h^
) :x=40

""")
song.play("""
%d
  [bu^ut^tbuusu^ut^t.b.]/4
  [(bg)(bc)(bc^)]*3/4
%t
  .*3 [..(a@-1 C^@-1 E).]/4
  [(b@-1 D@-1 G)
   (b@-1 E@-1 G^)
   (C^@-1 E@-1 A)]*3/4
%b .*7/2 [E.[GG^A]*3]/4
%bb .*7/2 [E.[GG^A]*3]/4 A~Vc*8
%s .*7
[[cCC1C2]<<[aC^E]=1/2]x=3~V[Cc]
""")


song.write("Asteroid Punching")