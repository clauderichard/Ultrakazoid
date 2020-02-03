from midiutil import *
from math import *
from ukz.loudness import *

################################

# Midi interpreter names
fluidR3 = "fluidR3"

################################

# A MidiInstrument occupies 
# one track and one channel 
# in a midi file.
# Arguments:
# program: instrument number in
#          MIDI standard.
# octave: translate every note 
#         by this much times 12.
# loudnessArg
class MidiInstrument:
    
  def __init__(self,\
   program,octave,loudnessArg=None):
    self.program = program
    self.octave = octave
    #self.loudnessMap = mkLoudnessMapFromArg(loudnessArg)
    self.loudnessMap2 = mkLoudnessMapFromArg2(loudnessArg)
    self.volume = 96
  
  def setVolume(self,vol):
    self.volume = vol
  
  def genTrackRoute(self,trg):
    return trg.genTrack()
    
  def __str__(self):
    return f"MidiInstrument({self.program},{self.octave},{self.loudnessMap2})"

  def setVel(self,pitch,loudness,vel):
    self.loudnessMap2.setVel(pitch,loudness,vel)
  def setVelAllPitch(self,loudness,vel):
    self.loudnessMap2.setVelAllPitch(loudness,vel)


# MidiDrums occupies one track and
# the drum channel in a midi file.
class MidiDrums(MidiInstrument):
    
    # loudnessArg must have type be one of the following:
    #   int
    #   LoudnessMap
    def __init__(self,loudnessArg=False):
        MidiInstrument.__init__(\
        	self,0,0,loudnessArg)
        	
    def genTrackRoute(self,trg):
        return trg.genDrums()
    
    def __str__(self):
        return f"MidiDrums({self.loudnessMap2})"

################################

# An Instrument is supposed to
# represent a sound. The sound can be
# simulated by combining several
# MidiInstruments.
class Instrument:
  def __init__(self,midiInstruments):
    if isinstance(midiInstruments,list):
      #self.midiInstruments = midiInstruments.copy()
      self.midiInstruments = []
      for mi in midiInstruments:
        i = mkMidiInstrument(mi)
        self.midiInstruments.append(i)
    elif isinstance(midiInstruments,MidiInstrument):
      self.midiInstruments = [midiInstruments]
    else:
      raise ValueError("Invalid type passed to Instrument constructor")
  def isDrums(self):
    return isinstance(self.midiInstruments[0],MidiDrums)
  def setVolume(self,v):
    for mi in self.midiInstruments:
      mi.volume = v
  def setVel(self,pitch,loudness,vel):
    for mi in self.midiInstruments:
      mi.setVel(pitch,loudness,vel)
  def setVelAllPitch(self,loudness,vel):
    for mi in self.midiInstruments:
      mi.setVelAllPitch(loudness,vel)
          
def mkMidiInstrument(a1,a2=None,a3=None):
    if isinstance(a1,tuple):
        aa1 = a1[0] if len(a1)>0 else None
        aa2 = a1[1] if len(a1)>1 else 0
        aa3 = a1[2] if len(a1)>2 else 64
        return MidiInstrument(\
        	aa1,aa2,aa3)
    elif isinstance(a1,MidiInstrument):
        return a1
    elif isinstance(a1,int) and isinstance(a3,dict):
        mi = MidiInstrument(a1,a2)
        for (l,v) in vals(a3):
            mi.setVelAllPitch(l,p)
        return mi
    raise ValueError("a1 must be a tuple for now")
def mkInstrument(a1=0,a2=None,a3=None):
    if isinstance(a1,int):
        octave = a2 if a2 else 0
        loudnessArg = a3 if a3 else 100
        return Instrument([MidiInstrument(a1,octave,loudnessArg)])
    elif isinstance(a1,list):
        mis = []
        for mi in a1:
            mis.append(mkMidiInstrument(mi))
            return Instrument(mis)
    raise ValueError(f"Cannot mkInstrument() with first argument {a1}")
def mkDrums(a=None):
    vel = a if a else 100
    return Instrument([MidiDrums(vel)])

################################

acousticGrandPiano = 0
brightAcousticPiano = 1
electricGrandPiano = 2
honkyTonkPiano = 3
electricPiano1 = 4
electricPiano2 = 5
harpsichord = 6
clavinet = 7

celesta = 8
glockenspiel = 9
musicBox = 10
vibraphone = 11
marimba = 12
xylophone = 13
tubularBells = 14
dulcimer = 15

drawbarOrgan = 16
percussiveOrgan = 17
rockOrgan = 18
churchOrgan = 19
reedOrgan = 20
accordion = 21
harmonica = 22
tangoAccordion = 23

acousticGuitarNylon = 24
acousticGuitarSteel = 25
electricGuitarJazz = 26
electricGuitarClean = 27
electricGuitarMuted = 28
overdrivenGuitar = 29
distortionGuitar = 30
guitarHarmonics = 31

acousticBass = 32
electricBassFinger = 33
electricBassPick = 34
fretlessBass = 35
slapBass1 = 36
slapBass2 = 37
synthBass1 = 38
synthBass2 = 39

violin = 40
viola = 41
cello = 42
contrabass = 43
tremoloStrings = 44
pizzicatoStrings = 45
orchestralHarp = 46
timpani = 47

stringEnsemble1 = 48
stringEnsemble2 = 49
synthStrings1 = 50
synthStrings2 = 51
choirAahs = 52
voiceOohs = 53
synthChoir = 54
orchestraHit = 55

trumpet = 56
trombone = 57
tuba = 58
mutedTrumpet = 59
frenchHorn = 60
brassSection = 61
synthBrass1 = 62
synthBrass2 = 63

sopranoSax = 64
altoSax = 65
tenorSax = 66
baritoneSax = 67
oboe = 68
englishHorn = 69
bassoon = 70
clarinet = 71

piccolo = 72
flute = 73
recorder = 74
panFlute = 75
blownBottle = 76
shakuhachi = 77
whistle = 78
ocarina = 79

lead1Square = 80
lead2Sawtooth = 81
lead3Calliope = 82
lead4Chiff = 83
lead5Charang = 84
lead6Voice = 85
lead7Fifths = 86
lead8BassLead = 87

pad1NewAge = 88
pad2Warm = 89
pad3Polysynth = 90
pad4Choir = 91
pad5Bowed = 92
pad6Metallic = 93
pad7Halo = 94
pad8Sweep = 95

fx1Rain = 96
fx2Soundtrack = 97
fx3Crystal = 98
fx4Atmosphere = 99
fx5Brightness = 100
fx6Goblins = 101
fx7Echoes = 102
fx8SciFi = 103

sitar = 104
banjo = 105
shamisen = 106
koto = 107
kalimba = 108
bagpipe = 109
fiddle = 110
shanai = 111

tinkleBell = 112
agogo = 113
steelDrums = 114
woodblock = 115
taikoDrum = 116
melodicTom = 117
synthDrum = 118
reverseCymbal = 119

guitarFretNoise = 120
breathNoise = 121
seashore = 122
birdTweet = 123
telephoneRing = 124
helicopter = 125
applause = 126
gunshot = 127

################################
