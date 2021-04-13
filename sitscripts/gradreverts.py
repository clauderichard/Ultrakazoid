from ukz import *

song = Song("""
	bpm 90
%x alto sax o3 v110
%x bari sax o3 v110
""")

################################

song.play("""
%x
[A~[cc2]] AE A~[cc-2] AE

""")

song.write("gradreverts")