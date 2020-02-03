from ukz import *

song = Song()

guitar = song.newPlayer(\
 'nylon',1,{5:100})
drums = song.newDrummer(\
 'power',{5:100})
 
guitar.play("""
[
 [cegdfe]<<[cfe]/10 x=8
 [cdecc^d^]<<[cd^d]/10 x=8
] <$[cd^f^g]
[c-C4]=2
[(cegb)^*5(cegb)=11]/4
[c& ev g]=2 <<: [c (cc^)^ (cc^e)^]
[cevgvaa^c^g...]¬ =8
""")
drums.play("""
(
 (h^ [b.b.S.bsbsb.S.b.]/4 ) :x=16
 c*8x2
)
( R/2 [.s]=1 ) :x=8 ~[cCcC1]
( b/12 r/6 [.s]=2 ) :x=8 o[C[cC]x3]
( b/16 r/4 [h^s]=1 ) :x=8 ~[cCcC1] o[C[cC]x3]
[c.cc.c.c.cc.c.cc]/4 <<: [ (bsg) (H^) ]
""")
song.sync()

guitar.play("""
[cevgvaa^c^g...]¬ =8 °9
[cfgCcabbvcC] _3
""")
drums.play("""
.*8
( b/16 r/4 [h^s]=1 ) :x=8 ~[cCcC1] o[C[cC]x3]
""")

song.write(120,'template')