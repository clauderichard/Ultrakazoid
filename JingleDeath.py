from ukz import *
	
conv = 1==1

song = Song()

guitar = song.newPlayer(\
 Instr('overdr',2,{
 	5: 127 if conv else 100,
 	3: 72 if conv else 60 }), \
 Instr('finger elec bass',1,{
  5: 127 if conv else 100 }), \
 Instr('lead square',2,{
  5: 100 if conv else 100 }))
solo = song.newPlayer(\
 Instr('overdr',3,{
  None: 120 if conv else 110,
  5: 127 if conv else 100,
  3: 72 if conv else 60 }))
drums = song.newDrummer('power',{
 5: 90 if conv else 100,
 (38,5): 80 if conv else 95 })
 
song.sync()

drums.play("""
( [ [g..g^.*12 c..c^.*8 g^.]/2
	   [ut^t]/3]_4
	 [.s]=4x4
	 [ b/4x6 b/8x4 b/4x6 b/8x4
	   b/4x6 b/8x4 b/4x4 b/8x8
	   b/4x6 b/8x4 b/4x6 b/8x4
	   b/4x8 b/8x8 b/3x3
	 ]
)
(b c)*4
(
	 ( b/8x=4 [[u^ut^t]@x6 /8 [gc^]/2] )
  [g*3/4x4 g/2x2]
)
""")
guitar.play("""
[c*3a*13 g*3f^*13
 c^*16
]/2 << (cg)
""")

song.sync()
 
guitar.play("""
	[(da) (da)v (da)vv (dv3av4)]^5 *8
	[dc^cc^ ec^ag^ gc^]^6 /4 x=14
	[ag^gc^ f^fec]^6 /4
""")
drums.play("""
( [c*8x3 c*6 g/2x4]
 ( [HS]=1/4 j ) @x=32
)
( g*8 b/12 [.s]=2 j/2 ) @x=8
( b/12 [h^s]=1/2 j/2 ) @x=4
( b/12 [ss]=1/4 j/2 ) @x=2
( b/12 [[u^ut^t]@x4]=2 j/2 ) @x=2
""")
song.sync()

guiadj = "1/15"
guitar.play(f"""
(aE) [c^c^cc^.c^cc^dc^cc^]/4<<(cf^)
 <{guiadj} .*{guiadj}
(gD) [c^c^cc^.c^cc^ed^dc^]/4<<(cf^)
 <{guiadj} .*{guiadj}
(aE)v [c^c^cc^.c^cc^dc^cc^]/4<<(cf^)
 <{guiadj} .*{guiadj}
[ccv]<<[ba^ag^ed^dc^]/4 
 <{guiadj} .*{guiadj}
(aE) [c^c^cc^.c^cc^dc^cc^]/4<<(cf^)
 <{guiadj} .*{guiadj}
(gD) [c^c^cc^.c^cc^ed^dc^]/4<<(cf^)
 <{guiadj} .*{guiadj}
[d^dc^d ag^gg^ Cba^a]/4
 <{guiadj} .*{guiadj}
[g^gf^]/3
 <{guiadj} .*{guiadj}
(fb)*4
""")
drums.play("""
(
 C=4x3
 [.S]x=12
 [jx=12 j/2x=4]
 [ b ( b/10 ) @x=3
   b ( b/10 [..[h..h..h.]^/8] ) @x=3
   b ( b/10 ) @x=3
   (b/10 )@x=2 (b/10 s*2 )@x=2
 ]
)
(
 C=4x3
 [.S]x=8
 [jx=8 .*4 j]
 [ b ( b/10 ) @x=3
   b ( b/10 ) @x=3
   (b/10 [u^ut^t]@x5=2)@x=2
   (b/10 s/5)@x=1
   (b/3 s/3 [ut^t]/3) @x=1
   (bscg)*2
   b/8x=1 b/3x=1
 ]
)
""")

song.sync()

guitar.play("""[
[e..e..e.]/4_1/3 << (cf^C°3)
.*4 [g*3f^*3f*2]/4 << (f^)
[e..e..e.]/4_1/3 << (cf^C°3)
.*6
[[e..g..]_4/3c*4d*2e*20ev*16d*16]/4
 << (cf^C°3)
]v2
""")
drums.play("""
( j*2 x=32
	 [.s]=4 x=28
	[
	.*4 b/8x=4
	.*4 b/10x=4
	.*4 b/12x=12
	]
	[
	 F..F..F.C*8
	 .*8 u..t^..t.
	 F..F..F.C*8
	 h...h...g..g..g.
	 F..F..F.c^.F.F...
	 .*32
	 [sx12]=8 s/2x=6 (jc^).
	]/4
)
""")

song.sync()

guitar.play(f"""
[
 [(cg)^(cg)]*3/2 cv2
 [(cg)v*3(cg)vv*5]/2
 [(cg)(cg)v]*3/2 cv2
 [(cg)^*3(cg)^^*5]/2
]x2 <{guiadj} .*{guiadj}
""")
solo.play("""
 C1*3/2 ~[C*6[Gg]x6]
 B*3/2 ~[C*6[Gg]x6]
 [ccvcvv] <<
  [c<^[9-4]]/6 $[cd^f^a]
 E1*2 ~[C*6[C2c]x9]
 [cvcc^] <<
  [c<^[4-9]]/6 $[cd^f^a]
 c<^[1-16]/8 ^20
 [[df^][dvf][ce]]@x4 =3 ^30
 (AD1^)^4*2 ~[F^*6[cC]<^[12-0]]
 (AD1^)^4v*2 ~[F^*6[cC]<^[12-0]]
 [dc^c] << [ [c<^[8-1-7]]
  $[cd^f^a] ] ^4 _3/2 =4
 [CC^DD^EF] @x5 ^8 =3
 [C^DD^E]^14@x4=3/2
 (D1F1)^5*7/2 ~[cF^]
""")
drums.play("""
(c ( [js]=1/2 b/12 ) @x=24)
( j/2 [.s]=2 b/12 ) @x=4
( j/2 s/6 b/12 ) @x=2
( j/2 s/8 b/12 ) @x=2
""")

song.sync()

guitar.play("""
[
 [ed^dd^dc^]=1 (gD)/2
 [d^dc^dc^c]=1 [d^f^c^]/2<<(cg)
 [c^cdc^d^de]<<[f^d^c]/6
 [f^]/2<<(cg)
 [ed^dd^dc^]=1 (gD)/2
 [d^dc^dc^c]=1 [c^df]/2<<(cg)
 [c^cdc^d^d]<<[f^d^c]/6
 e<<(cf^C°3)
]^5
""")
drums.play("""
(
	 [ c*7 [gc^]/2
	   c .*6 C^ ]
	 ( j/2 [.s]=2 b/12 ) @x=15
	 .*16
)
""")

song.sync()

guitar.play("""
[
 [f..f..f.]/4_1/3 << (cf^C°3)
 .*4 [d*3c^*3c*2]/4 << (f^)
 [f..e..e.]/4_1/3 << (cf^C°3)
 .*5 [ee]=1 << (cf^C°3)
 [ [g..g..]/4_1/3 f*9/2 [d...]/2
 ] << (cf^C°3)
 [ c^*8 ] << (cf^Cv°3)
 ]
""")
drums.play("""
(
 [ ( [hs]=1/4 b/12 ) @x=12
   ( b/12 [u^u^ut^]@x8=4 ) @x=4
   ( [hs]=1/4 b/12 ) @x=4
   ( [u^ut^t]@x4=2 b/12 ) @x=2
   C^
 ]
 [
  [[j..j..j.]=2 .*6] x2
  [j..j..j.]=2 .*4 j .*1
 ]_1
)
( c*8 j*8 b*8 ) @x=4
( b/12 [[sx4bb]x4sx8]=4 ) @x=4
( c*4 [js]=1/2 b/12 ) @x=4
(  s/8 b/12 ) @x=2
[U^U]@x4 =1 [T^T^T]=1
( j bs ) =8
""")
solo.play("""[
.*24
.*4
(FD1)1 *2 ~[[C1cCc]x3C1]
c<^[0-15] ^14 =2
c<^[8-0-9-0-8-0-9-0-8-0-3]
 _2 =4 $[cc^f^a] ^5
[Cgd^c]^23 @x4 =2
c<^[0-10]^15 =1
[D^FF^]/3^23
(CF^G)^23 ~[C1C1c]
]
""")

song.sync()

song.write(110,'jingledeath' \
	+ ('_conv' if conv else ''))