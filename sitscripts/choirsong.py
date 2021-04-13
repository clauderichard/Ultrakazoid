from ukz import *

song = Song("""
	bpm 150
%t choir aa o5 legato v120 90
""")

song.play("""
%t (ce)/32 x=8
""")
song.play("""
%t [(cg@-1)/4(ca@-1)/4]x8
""")
song.play("""
%t [(df)(dg)(dav)(da)(da^)(db)]/3x3
""")

song.write("choirsong")
