
# There are 8 levels of loudness.
# A MidiInstrument has a
# volume number for each loudness.
# Loudnesses: ppp,pp,p,mp,mf,f,ff,fff
pianississimo = 0
pianissimo = 1
piano = 2
mezzopiano = 3
mezzoforte = 4
forte = 5
fortissimo = 6
fortississimo = 7
def mkDefaultVolumes:
    return [30,40,50,60,70,80,90,100]

# A MidiInstrument occupies 
# one track and one channel 
# in a midi file.
# Settings:
    # octave: translate every note 
    #         by this much times 12.
    # volumes: 8 volume numbers,
    #          one for each loudness.

# You can combine MidiInstruments
# to make a different sound.

# You can make a general sound,
# which has a different setting
# for each midi interpreter. 
# Each setting has the interpreter
# name and a list of MidiInstruments.
# This cross-intrepreter sound can
# be called Instrument.
# Different from MidiInstrument.

# List of midi interpreter names
fluidR3 = "fluidR3"

class MidiInstrument:
    def __init__(self,\
    	program=0,octave=3,volumes=False):
        self.program = program
        self.octave = octave
        self.volumes = volumes
        if not self.volumes:
            self.volumes = \
             mkDefaultVolumes()

class Instrument:
    def __init__(self,config={}):
        self.config = config
        if "" not in self.config:
            self.config[""] = \
             [MidiInstrument()]
    
    def setMidiInstrumentsForInterpreter(\
    	self,interpreterName,\
    	midiInstruments):
        self.config[interpreterName]\
         = midiInstruments
    
    def setDefaultMidiInstruments(\
    	self,midiInstruments):
        self.setMidiInstrumentsForInterpreter(\
        	"",midiInstruments)
