# from midiutil import *
# from ukz import *

# ################################

# officialName = \
#  "Testing"
# song = Song(officialName,200)

# progs = list(range(0,128))
# pitches = [24,31,40]
# pitchI = 0
# for i in range(0,9):
#     pitches.append(\
#      pitches[pitchI]+24)
#     pitchI = pitchI + 1

# track = song.addTrack(0)
# track.curVolume = 100
# track.curPitchShift = 0

# song.init()

# #####################################

# for prog in progs:
#     track.switchProgram(prog)
#     for p in pitches:
#         track.addNote(p,1,True)

# songLength = track.timeShift \
#  * 60 / song.initTempo
    
# song.write()

# print('Song written!')
# print('  Title:',song.name)
# print('  Length:',\
# 	songLength,'seconds')
