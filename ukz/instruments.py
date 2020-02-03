
midiVersions = [\
 "Default",\
 "FluidR3"\
 ]

ambientbass = Track()
ambientbass.programs = { \
 "": 52, \
 "FluidR3": 55 \
 }
ambientbass.curVolume = 100
ambientbass.setPitchShift(24)

bass = song.addTrack(4)
bass.curVolume = 100
bass.setPitchShift(36)

rain = song.addTrack(0)
rain.curVolume = 100
rain.setPitchShift(72)

choir = song.addTrack(52)
choir.curVolume = 80
choir.setPitchShift(48)
        
bell = song.addTrack(4)
bell.curVolume = 90
bell.setPitchShift(72)