from ukz import *

song = Song()

drums = song.addDrumsTrack(120)
guitar = song.addTrack(\
	[(overdrivenGuitar,2,100)\
	,(churchOrgan,2,90)])

drums.playMelody(ukd("""
gx4
[
( b=64 h°=16 l=32 [.s]=16 c )
( b=128 h°=16 l=48 [.s]=16 )
( b=128 g=16 l=64 [.s]=8 )
( b=256 h°=32 g=8 l=96 [.s]=32 )
(C [.h°]=4)
] *16
[
(b=32 h°=4 [.s]=2 )*8
(b=48 h°=4 [.s]=2 )*8
(b=48 h°=16 [.s]=4 )*8
(b=48 h°=16 l=24 [.s]=4 )*8
(g b=64 h°=16 l=24 [.s]=8 )*8
(g=4 b=64 h°=16 l=32 [.s]=8 )*8
(g=4 b=128 h°=32 l=48 [.s]=8 )*8
(g=8 b=128 h°=32 l=48 [.s]=16 )*8
(g=4 b=192 h°=16 l=64 [.s]=8 )*8
(g=2 b=256 h°=8 l=96 [.s]=4 )*8
C*8
C*4
T4T3T2T1
(bgc)*10
]
"""))

guitar.playMelody(ukz("""
.*4
[(CG) (C#G#) (EA) (D#G#)
(CF#) (C#G) (FA#) (DA)
(C#G)
]*8
[
(D#G#)*3/2 (DG)*13/2
(bF)*8 (CF#)*3/2 (bF)*13/2
(C#F#)*4 (DG)*4
(D#A)*4 (EA#)*4
(Gc2)*3/2 (F#B)*13/2
(FA#)*3/2 (F#B)*13/2
(FAc2#)*3/2 (EG#c2)*13/2
(FAc2#)*3 (EG#c2)*5
(CF#)*8
(aD#)*8
(f#)*8
d#*8
c*8
]
"""))

song.write(120,"Doom Smash")
