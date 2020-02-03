from midiutil import *
from math import *
from ukz.midibuilder import *
from ukz.instrument import *
from ukz.track import *

class Song:
    
    def __init__(self):
        self.tracks = []

    # you can't call this after calling init
    def addTrack(self,a1,a2=None,a3=None):
        i = None
        if a2 is None:
            if isinstance(a1,Instrument):
                i = a1
            elif isinstance(a1,int):
                i = Instrument(\
                	[MidiInstrument(a1)])
            elif isinstance(a1,list):
                mis = []
                for a in a1:
                    mis.append(mkMidiInstrument(a))
                i = Instrument(mis)
            else:
                raise 11
        elif isinstance(a2,int):
            if isinstance(a1,int):
                mi = None
                if a3 is None:
                    mi = MidiInstrument(a1,a2)
                elif isinstance(a3,int):
                    mi = MidiInstrument(a1,a2,a3)
                else:
                    raise 23
                i = Instrument([mi])
            elif isinstance(a1,list):
                mis = []
                if a3 is None:
                  for p in a1:
                    mi = MidiInstrument(p,a2)
                    mis.append(mi)
                elif isinstance(a3,int):
                  for p in a1:
                    mi = MidiInstrument(p,a2,a3)
                    mis.append(mi)
                else:
                    raise 23
                i = Instrument(mis)
            else:
                raise 33
        else:
            raise 112
        tr = Track(i)
        self.tracks.append(tr)
        return tr
        
    def addTracks(self,n,a1,a2=None,a3=None):
        r = []
        for i in range(0,n):
            r.append(self.addTrack(a1,a2,a3))
        return r
        
    def addDrumsTrack(self,loudnessArg=64):
        i = mkDrums(loudnessArg)
        tr = Track(i)
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
            minstrs = tr.instrument.midiInstruments
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
        midifilename = f"../Music/Midi/{name}.mid"
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
