from midiutil import *
from ukz.scheme import *
from ukz.melody import *
from ukz.numerize import *

# Loudness and Volume
pianississimo = 0
pianissimo = 1
piano = 2
mezzopiano = 3
mezzoforte = 4
forte = 5
fortissimo = 6
fortississimo = 7

defaultVolumes = \
 [30,40,50,60,70,80,90,100]

# Midi interpreter names
fluidR3 = "fluidR3"

# A MidiInstrument occupies 
# one track and one channel 
# in a midi file.
# Settings:
    # program: instrument number in
    #          MIDI standard.
    # octave: translate every note 
    #         by this much times 12.
    # volumes: 8 volume numbers,
    #          one for each loudness.
class MidiInstrument:
    def __init__(self,\
    	program=0,octave=3,volumes=False):
        self.program = program
        self.octave = octave
        self.volumes = volumes
        if not self.volumes:
            self.volumes = \
             defaultVolumes

class Instrument:
    def __init__(self,config={}):
        self.config = config
        if "" not in self.config:
            self.config[""] = \
             [MidiInstrument()]
    
    def setForInterpreter(\
    	self,interpreterName,\
    	midiInstruments):
        self.config[interpreterName]\
         = midiInstruments
    
    def setDefault(\
    	self,midiInstruments):
        self.setForInterpreter( \
        	"",midiInstruments)


class MidiTrackChannel:
    def __init__(self,trackI,channelI):
        self.trackI = trackI
        self.channelI = channelI

class Track:

    def __init__(self,instrument):
        self.instrument = instrument
        self.curLoudness = 4
        self.curTime = 0
        self.notes = []
    
    def addNote(self,pitch,duration=1,loudness=-1):
        t = self.curTime
        p = value(pitch)
        d = numerize(value(duration))
        ld = self.curLoudness \
         if loudness<0 else loudness
        self.notes.append((\
        	t,p,d,ld))
        
    def addChord(self,chord,duration=1,loudness=-1):
        for p in value(chord):
            self.addNote(p,duration,loudness)

    def addMelody(self,melody):
        tm = 0
        ti = self.curTime
        for (t,p,d,l) in melody.notes:
            self.forward(t-tm)
            self.addNote(p,d,l)
            tm = t
        self.curTime = ti

    def forward(self,duration):
        self.curTime = \
         self.curTime + \
         numerize(value(duration))
         
    def write(self,midifile,routes,interpreter):
        minstrs = self.instrument.config[interpreter]
        minstri = iter(minstrs)
        for (tn,cn) in routes:
            minstr = next(minstri)
            prog = minstr.program
            midifile.addProgramChange(tn,cn,0,prog)
            vs = minstr.volumes
            for (t,p,d,l) in self.notes:
                v = vs[l]
                pp = p + 12*minstr.octave
                #if debug:
                #print("addNote",\
                #	tn,cn,pp,t,d,v)
                midifile.addNote(\
                 tn,cn,pp,t,d,v)

class TrackRouteGenerator:
    def __init__(self):
        self.tn = 0
        self.cn = 0
    def genDrums(self):
        t = self.tn
        self.tn = self.tn + 1
        return (t,9)
    def genTrack(self):
        t = self.tn
        self.tn = self.tn + 1
        c = self.cn
        self.cn = self.cn + \
         (2 if self.cn==8 else 1)
        return (t,c)

class Song:
    
    def __init__(self):
        self.tracks = []

    # you can't call this after calling init
    def addTrack(self,instrument):
        tr = Track(instrument)
        self.tracks.append(tr)
        return tr
        
    # make all tracks go to the
    # specified time. 
    def goto(self,to):
        t = 0
        if isinstance(to,Track):
            t = to.curTime
        else:
            t = to
        for track in self.tracks:
                track.curTime = t

    # must call this after calling init
    def write(self,initTempo,name,interpreter=""):
        numTr = 0
        tncs = []
        tncgen = TrackRouteGenerator()
        for tr in self.tracks:
            minstrs = tr.instrument.config[interpreter]
            numTr = numTr + \
             len(minstrs)
            tnc = []
            for mi in minstrs:
                tnc.append(tncgen.genTrack())
            tncs.append(tnc)
        midifile = MIDIFile(numTr)
        midifile.addTempo(0,0,initTempo)
        tri = 0
        for tr in self.tracks:
            tr.write(midifile,tncs[tri],interpreter)
            tri = tri + 1
        with open(name + ".mid", "wb") as output_file:
            midifile.writeFile(output_file)
