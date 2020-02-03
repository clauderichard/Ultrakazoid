from ukz import *

song = Song()

trumpet = song.newPlayer(\
 'trumpet',6,{5:100})
choir = song.newPlayer(\
 'choir',5,{5:70})
drums = song.newDrummer(\
 'stan',{
 5:90,
 (38,5):127,
 (36,5):95,
 (52,5):70,
 (55,5):105,
 (53,5):105,
 (59,5):120
 })
 
drums.play("""
([H^°7.HH]=2 ) @x=16
""")
choir.play("""
(egC)*4 (fgC)*4
(egC)*4 (fgD)*4
""")
song.sync()
 
trumpet.play("""
c*3d e*2ee [f.e.f...]=2
e*4 ....
.ccd eeee [f.e.f...]=2
e*4 ....
.def ggga [g.f.e...]=2
d*4 ....
.def ggga [bv.a.g...]=2
[f*3 .]/2 [a.g.f...]=2 
 [e*3 .]/2 [g.f.e...]=2
d*4 ....
c*3d e*2ee [f.e.f...]=2
e*4 .. [d.c.d...]=2
c*4
""")
choir.play("""
(egC)*3 (gbD) (gCE)*4 (fCD)*2
(gCE)*8
(egC)*3 (gbD) (gCE)*4 (fCD)*2
(gCE)*8
(gbD)*3 (aCF) (bDG)*4 (gCE)*2
(gbD)*8
(gbD)*3 (aCF) (CEG)*4 (CGBv)*2
(CFA)*4 (CEG)*4 (bDG)*4 (gbD)*4
(egC)*3 (gbD) (gCE)*4 (fCD)*2
(gCE)*6 (gbD)*2
(egC)*4
""")
drums.play("""
[
 ([H^°7.HH]=2 ) @x=8
 (b/8 l/4 [u^ut^t]@x6=2) @x=2
 (c*8 h^/2 b/12 l/4 [.s]=1 ) @x=8
 [ [c..c..c.]^/4 |
  (c^*8 h^ b/16 l/6 [.s]=1/2 ) @x=8
  (s/8 b/16) @x=2
 ]
 (
  (c*8 h^ b/24 l/3 [.g(sc^)g]=2 ) @x=8
  [.*7 [g..c^]/4 ]
 )
 (c*8 h^/2 b/24 l/6 [.s]=1 ) @x=10
 [ (g*8 h^ b/32 l/3 [.s]=1 ) @x=8
 ]
 [ [gx8]^=2 |
   (g^*4 c^*4 h^ b/32 l/4 [hs]=1/4 ) @x=4
   (c^*4 h^ b/48 l/8 [hs]=1/4 ) @x=4
   ( b/48
   	  [[u^u][ut^][t^t]]@x5=2
   	) @x=2
 ]
 ( (cc^)*8 
 	  lx3=2 h^ b/64
 	  [.g]=2 [.s]=4
 	) @x=8
 	[ c^ |
 	  (cg)*4
 	  (
 	  	 S/8
 	  	 [[g..]x4[g.]x1c.]/4
 	  	) @x=4
 	]
 	( c*8 [.s]=1/2 b/24 g/4 ) @x=8
 	( ( b/24 ) @x=2
 		 [(cs)x3.]=2
 	)
 	( cc^
 		 [ [tt^]@x8=2
 		   sx8=1 (sx3=1 [g^gc^]=1)
 		 ]
 	)
 	(scc^)*2
  ( 	[(Su)(St^)(St).]=2
  	 [lx3.]/2
  )
 	(cgbsc^g^l)*2
 	( [u^ut^t]x8=2 b/64*100/134x=2
 	)
 	C*4
]
""")
song.sync()
song.gradualTempo(120,-20,90,-5)

choir.choirize()

song.write(120,'metaldrummerboy')