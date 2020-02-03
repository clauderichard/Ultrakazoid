from midiutil import *
from math import *
from ukz.midibuilder import *
from ukz.instrument import *
from ukz.track import *

class Song:
    
    def __init__(self):
        self.tracks = []

    # you can't call this after calling init
    def addTrack(self,instrument):
        instr = instrument #\
         #if isinstance(instrument,Instrument)
         #else Instrument
        tr = Track(instrument)
        self.tracks.append(tr)
        return tr
        
    def addSimpleTrack(self,program=0,octave=0,volumes=100):
        vols = volumes if isinstance(volumes,list) else [volumes]*8
        instr = Instrument()
        instr.setDefault([\
        	MidiInstrument(\
        	program,octave,vols)])
        return self.addTrack(instr)
        
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

    def computeMaxTime(self):
        t = 0
        for tr in self.tracks:
            t = max(t,tr.curTime)
        return t

    # must call this after calling init
    def write(self,initTempo,name,interpreter=""):
        MidiLog.init()
        numTr = 0
        troutes = []
        trg = TrackRouteGenerator()
        for tr in self.tracks:
            minstrs = tr.instrument.config[interpreter]
            numTr = numTr + \
             len(minstrs)
            troute = []
            for mi in minstrs:
                (t,c) = mi.genTrackRoute(trg)
                troute.append((t,c))
            troutes.append(troute)
        midi = MidiBuilder(numTr)
        #logg("construct MIDIFile",numTr)
        #midifile = MIDIFile(numTr)
        #logg("addTempo",0,0,initTempo)
        midi.addTempo(0,initTempo)
        tri = 0
        for tr in self.tracks:
            tr.write(midi,troutes[tri],interpreter)
            tri = tri + 1
        midifilename = f"../AMidi/{name}.mid"
        midi.writeFile(midifilename)
        #with open(midifilename, "wb") as output_file:
        #    logg("writeFile",midifilename)
        #    midifile.writeFile(output_file)
        songLength = self.computeMaxTime()
        songLength = songLength * 60 / initTempo
        songLengthM = floor(songLength)//60
        songLengthS = floor(songLength) - 60*songLengthM
        print('Song written!')
        print('  Title:',name)
        print(f"  Approx Length: {songLengthM}:{songLengthS//10}{songLengthS%10}")
        MidiLog.close()
