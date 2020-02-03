from ukz.ukengine import Players,Song
from ukz.uklang import ukz,ukd
from ukz.midi import programs

def ukztest(input,prog=4,octave=4,tempo=120):
    song = Song()
    ts = []
    progs = prog if isinstance(prog,list) \
     else [programs[prog]] if isinstance(prog,str) \
     else [prog]
    for p in progs:
      track = song.newPlayer(p,octave,{5:120})
      track.play(input)
    song.write(tempo,"ukz_test")
    
def ukdtest(input,tempo=120):
    song = Song()
    track = song.newDrummer({5:120})
    track.play(input)
    song.write(tempo,"ukd_test")
