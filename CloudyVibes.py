from ukz import *

song = Song()

drums = song.addDrumsTrack(127)
guitar = song.addTrack(\
	[(acousticGuitarNylon,3,127)\
	#,(churchOrgan,2,90)
	])
bass = song.addTrack([\
	(electricBassFinger,2,120)\
	#,(5,3,127)\
	])
choir = song.addTrack(\
	[(choirAahs,4,80)\
	#,(churchOrgan,2,90)
	])

drums.playMelody(ukd("""
[
( b/8 [h°*3x2 h°*2x5]=4 ) @x=4
[ T4x4 T3x4 T2x4 T1x4 ] =2
([ T4x2 T3x2 T2x2 T1x2 ]x3 gx2*12) =2
]
	
[(

 ( [b.b.b.bbbbb.b.b.]
  [....s..s.s..s...]
 )/4 x8
 
 c
)]

( [h.h.h°.hh°hh°h.h°.h.]
 )/4 x6
 ([T4x6 T3x6 T2x6 T1x6]=4 rx4)=4
 (bx24=1 [g..g..g.g.g.g.gc#]=1)=4
 
[(

 ( [b.b.b.bbbbb.b.b.]
  [....s..s.s..s...]
 )/4 x8
 
 c
)]

C#*12
"""))

guitar.playMelody(ukz("""
.x8
[
 [[CEGBD2]=1 (C#EG#BD#2)
  [E2C2#AF#D]=1 (D#F#A#C2#F2)
 ]*4
 [[F#AC2#E2]=1 [EG#BC#2]=1
 (DF#AC#2E2)=2
 ]*2x2
]

[
[CEFGC2GFE]x2=4
[C#EF#G#C2#G#F#E]x2=4
[CEFGC2GFE]x2=4
[DF#AB]x2=2 [C#F#AB]x2=2
[ [bDF#]=2 (bDF#A)=3/2
  [A]=1/2 [C2#BAF#]=2x2 ]=4
[ [DFA]=2 (DFAC2)=3/2
  [A]=1/2 [D2C2BAGAC2D2]=4 ]=4
[[E2D2#BG#]x6]=4
[ [D#2x8 D2x8]=1 [A#x6
  Gx6 D#x6]=1 ]=4
]

[
 [[CEGBD2]=1 (C#EG#BD#2)
  [E2C2#AF#D]=1 (D#F#A#C2#F2)
 ]*4
 [[F#AC2#E2]=1 [EG#BC#2]=1
 (DF#AC#2E2)=2
 ]*2x2
]

[C#FD#F#FG#F#A#G#C2A#C2#C2D2#]=4
C2#*8

"""))

bass.playMelody(ukz("""
.x8
[
 [C C# D D# ]*4
 [ F# E D*2 ]*2x2
]

[
C=4 C#=4
C=4 D=2 C#=2
b=4 D=4
E=4 D#=4
]

[
 [ C C#
   D D#
 ]*4
 [F# E D*2 ]*2x2
 
 C#*12
]
"""))

choir.addFadeIn(0)
choir.playMelody(ukz("""
.x8
[
 [(CEGB) (C#EG#B)
  (C2#AF#D) (D#F#A#C2#)
 ]*4
 [(F#AC2#E2G2#) (EG#BC#2F2#) (DF#AC#2E2)*2
 ]*2x2
]

[
(CEFG)=4+12
(C#EF#G#)=4+12
(CEGB)=4+12
[(DF#AC2#)=2 (C#F#AC2#)=2 ]+12
(bDF#A)=4 (DFAC)=4
(EG#BD2#)=4 (D#GA#D2F2)=4
]

[
 [(CEGB) (C#EG#B)
  (C2#AF#D) (D#F#A#C2#)
 ]*4
 [(F#AC2#E2G2#) (EG#BC#2F2#) (DF#AC#2E2)*2
 ]*2x2
 
 (C#FG#C2D2#)*12
]
"""))

choir.addFadeOut(-8)

song.write(120,"Cloudy Vibes")
