from ukz import *

song = Players()

drums = song.newDrummer('power',120)
guitar = song.newPlayer(\
	Instr('overdrive guitar',2,100)\
	,Instr('church organ',2,90))

drums.play("""
gx4
( b/4 h^ l/2 [.s]=1 c*16 ) @x=16
( b/8 h^ l/3 [.s]=1 ) @x=16
( b/8 g l/4 [.s]=2 ) @x=16
( b/16 h^/2 g*2 l/6 [.s]=1/2 ) @x=16
(C*16 [.h^]=4) @x=16

[
(b/4 h^=2 [.s]=4 ) @x=8
(b/6 h^=2 [.s]=4 ) @x=8
(b/6 h^/2 [.s]=2 ) @x=8
(b/6 h^/2 l/3 [.s]=2 ) @x=8
(g=8 b/8 h^/2 l/3 [.s]=1 ) @x=8
(g=2 b/8 h^/2 l/4 [.s]=1 ) @x=8
(g=2 b/16 h^/4 l/6 [.s]=1 ) @x=8
(g=1 b/16 h^/4 l/6 [.s]=1/2 ) @x=8
(g=2 b/24 h^/2 l/8 [.s]=1 ) @x=8
(g=4 b/32 h^ l/12 [.s]=2 ) @x=8
C*8
C*4
T4T3T2T1
(bgc)*10
]
""")

guitar.play("""
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
""")

song.write(120,"Doom Smash")
