from ukz import *

song = Song("""
	bpm 150
%s square o4 v110 70
%t choir aa o5 legato v120 90
""")

song.play("""
%s c*8
%t [(cg@-1)/4(ca@-1)/4]x8
""")
song.play("""
%s c | d || e
""")
song.play("""
%t (GDvF^)*2
""")

song.write("pipesong")
