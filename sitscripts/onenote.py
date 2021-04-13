from ukz import *

song = Song("""
	bpm 100
%b trumpet o4
""")

################################

song.play("""
%b c
""")

song.write("onenote")