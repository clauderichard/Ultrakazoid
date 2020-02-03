from midiutil import *
from math import *
from ukz.midibuilder import *
from ukz.instrument import *
from ukz.melody import *

class TrackRoute:
    def __init__(self,\
     trackNumber,channelNumber):
        self.tr = trackNumber
        self.ch = channelNumber

class Track(Melody):

    def __init__(self,instrument):
        Melody.__init__(self)
        self.instrument = instrument
        if isinstance(self.instrument,int):
            self.instrument = mkInstrument(self.instrument)
        self.volumeGradients = []
        self.curInterpreter = ""
        self.curRoutes = []
    
    def addVolumeGradient(self,time1,time2,volume1,volume2):
        self.volumeGradients.append((time1,time2,volume1,volume2))
    def addFadeIn(self,dt):
        if dt<0:
            self.addVolumeGradient(\
            	self.curTime+dt,self.curTime,0,127)
        else:
            self.addVolumeGradient(\
            	self.curTime,self.curTime+dt,0,127)
    def addFadeOut(self,dt):
        if dt<0:
            self.addVolumeGradient(\
            	self.curTime+dt,self.curTime,127,0)
        else:
            self.addVolumeGradient(\
            	self.curTime,self.curTime+dt,127,0)
   
    def getCurMinstrs(self):
        return self.instrument.config[self.curInterpreter]
    def genCurRoutes(self,trg):
        self.curRoutes = []
        for minstr in self.getCurMinstrs():
            self.curRoutes.append(\
            	minstr.genTrackRoute(trg))
    
    def writeInstrumentChange(self):
        for (tr,mi) in zip(self.curRoutes,self.getCurMinstrs()):
            tn = tr[0]
            cn = tr[1]
            prog = mi.program
            logg("addProgramChange",tn,cn,0,prog)
            midifile.addProgramChange(tn,cn,0,prog)
            
    def write(self,midi,routes,interpreter):
        minstrs = self.instrument.config[interpreter]
        minstri = iter(minstrs)
        #writeInstrumentChange(0,\
        #	self.instrument)
        for (tn,cn) in routes:
            minstr = next(minstri)
            prog = minstr.program
            #logg("addProgramChange",tn,cn,0,prog)
            midi.addProgramChange(tn,cn,0,prog)
            vels = minstr.velocities
            for (t1,t2,v1,v2) in self.volumeGradients:
                #vvvv = list(intsFromTo(v1,v2))
                #print(vvvv)
                #print(tn,t1,t2,v1,v2)
                for vk in intsFromTo(v1,v2):
                    beta = (vk-v1)/(v2-v1)
                    alpha = 1 - beta
                    tnow = alpha*t1 + beta*t2
                    #print("addControllerEvent",tn,cn,tnow,7,vk)
                    midi.addVolumeChange(tn,cn,tnow,vk)
            for (t,p,d,l) in sorted(self.notes):
                if p is None:
                    continue
                vel = vels[l]
                pp = p + 12*minstr.octave
                if pp<0:
                    raise ValueError("pitch was negative")
                if d<0:
                    raise ValueError("duration was negative")
                midi.addNote(tn,cn,pp,t,d,vel)

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
class TrackRouteGenerator2:
    def __init__(self):
        self.tn = 0
        self.cn = 0
    def genDrums(self):
        t = self.tn
        self.tn = self.tn + 1
        return TrackRoute(t,9)
    def genTrack(self):
        t = self.tn
        self.tn = self.tn + 1
        c = self.cn
        self.cn = self.cn + \
         (2 if self.cn==8 else 1)
        return TrackRoute(t,c)
