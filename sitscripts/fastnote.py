from ukz import *

song = Song("""
	bpm 600
	tpb 256
%b trumpet o4
%d standard kit
""")

################################

song.play(""" .*2 """)

song.play("""
%b
a=2
%d
b=2
b/16x=2
b/32x=2
b/64x=2
b/128x=2
b/256x=2

""")

song.write("fastnote")