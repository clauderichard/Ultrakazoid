from midiutil import *
from math import *
from ukz.midibuilder import *
from ukz.instrument import *
from ukz.melody import *
from ukz.parser import *
from ukz.cubicgradient import *

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
    self.isDrums = instrument.isDrums()
    self.enabled = True
    self.writtenNotesCount = 0
    self.name = ""
    self.maxVolume = 96
    self.pitchBends = []
        
  def setVolume(self,v):
    self.instrument.setVolume(v)
    self.maxVolume = 96
  def setVel(self,pitch,loudness,vel):
    self.instrument.setVel(pitch,loudness,vel)
  def setVelAllPitch(self,loudness,vel):
    self.instrument.setVelAllPitch(loudness,vel)
       
        
  def addVolumeGradient(self,time1,time2,volume1,volume2):
    self.volumeGradients.append((time1,time2,volume1,volume2))
  def addFadeIn(self,dt):
    if dt<0:
      self.addVolumeGradient(\
      	self.time+dt,self.time,0,self.maxVolume)
    else:
      self.addVolumeGradient(\
       self.time,self.time+dt,0,self.maxVolume)
  def addFadeOut(self,dt):
    if dt<0:
      self.addVolumeGradient(\
       self.time+dt,self.time,self.maxVolume,0)
    else:
      self.addVolumeGradient(\
       self.time,self.time+dt,self.maxVolume,0)
   
  def getCurMinstrs(self):
    return self.instrument.config[self.curInterpreter]
  def genCurRoutes(self,trg):
    self.curRoutes = []
    for minstr in self.getCurMinstrs():
      self.curRoutes.append(\
       minstr.genTrackRoute(trg))
    
  def writeInstrumentChange(self,midifile):
    for (tr,mi) in zip(self.curRoutes,self.getCurMinstrs()):
      tn = tr[0]
      cn = tr[1]
      prog = mi.program
      logg("addProgramChange",tn,cn,0,prog)
      midifile.addProgramChange(tn,cn,0,prog)
  
  def extractPitchBends(self):
    self.pitchBends = []
    v = self.maxVolume
    for n in self.notes:
      if n.b != 0:
        self.pitchBends.append(\
        (n.t,n.t+n.d,n.b,0))
        self.volumeGradients.append(\
         (n.t,n.t+n.d,v//2,v))
            
  def writePitchBends(self,midi,tn,cn):
    self.extractPitchBends()
    for (t1,t2,v1,v2) in self.pitchBends:
      for (t,v) in polGradPts(\
       2,t1,t2,v1*64,v2*64):
        midi.addPitchBend(tn,cn,t,v*64-1)
            
  def write(self,midi,routes,interpreter):
    if not self.enabled:
      return
    minstrs = self.instrument.midiInstruments
    minstri = iter(minstrs)
    #writeInstrumentChange(0,\
    #	self.instrument)
    for (tn,cn) in routes:
      minstr = next(minstri)
      prog = minstr.program
      midi.addProgramChange(tn,cn,0,prog)
      midi.addVolumeChange(tn,cn,0,minstr.volume)
      #loudnessMap = minstr.loudnessMap
      lMap2 = minstr.loudnessMap2
      self.writePitchBends(midi,tn,cn)
      for (t1,t2,v1,v2) in self.volumeGradients:
        for vk in intsFromTo(v1,v2):
          beta = (vk-v1)/(v2-v1)
          alpha = 1 - beta
          tnow = alpha*t1 + beta*t2
          midi.addVolumeChange(tn,cn,tnow,vk)
      for n in sorted(self.notes):
        if n.p is None:
          continue
        #vel = loudnessMap[l]
        pp = n.p + 12*minstr.octave
        if pp > 127:
            raise ValueError("The pitch number... is TOO DAMN HIGH!!!")
        vel = lMap2.getVel(pp,n.l)
        if pp<0:
          raise ValueError("pitch was negative")
        if n.d<0:
          raise ValueError("duration was negative")
        midi.addNote(tn,cn,pp,n.t,n.d,vel)
        self.writtenNotesCount = self.writtenNotesCount + 1
    self.writtenNotesCount //= len(minstrs)

  def play(self,ukzStr):
    if self.isDrums:
      self.appendMelody(ukd(ukzStr))
    else:
      self.appendMelody(ukz(ukzStr))

class TrackRouteGenerator:
    def __init__(self):
        self.tn = 0
        self.cn = 0
    def genDrums(self):
        t = self.tn
        self.tn = self.tn + 1
        if t>15 or self.cn>15:
          raise "too many channels used"
        return (t,9)
    def genTrack(self):
        t = self.tn
        self.tn = self.tn + 1
        c = self.cn
        self.cn = self.cn + \
         (2 if self.cn==8 else 1)
        if t>15 or c>15:
          raise "too many channels used"
        return (t,c)
