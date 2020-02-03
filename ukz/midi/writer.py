import midiutil
from ukz.midi.limits import *
from ukz.midi.trackroute import *

class MidiWriter:
    
  def __init__(self,numTracks):
    self.mf = midiutil.MIDIFile(numTracks)
    self.tr = None
    self.ch = None
    self.trg = TrackRouteGenerator()
    self.maxTime = 0
    self.lastVolume = 0
    self.lastPitchBend1 = 0
    
  def __maxt(self,t):
    self.maxTime = max(t,self.maxTime)
    
  def switchToInstr(self):
    route = self.trg.genNonDrums()
    Limits.checkChannel(route.channel)
    Limits.checkTrack(route.track)
    self.tr = route.track
    self.ch = route.channel
  def switchToDrums(self):
    route = self.trg.genDrums()
    Limits.checkChannel(route.channel)
    Limits.checkTrack(route.track)
    self.tr = route.track
    self.ch = route.channel
    
  def addTempo(self,t,tempo):
    Limits.checkTime(t)
    Limits.checkTempo(tempo)
    self.mf.addTempo(0,t,tempo)
    self.__maxt(t)
        
  def addProgramChange(self,t,prog):
    Limits.checkTime(t)
    Limits.checkProgram(prog)
    self.mf.addProgramChange(\
     self.tr,self.ch,t,prog)
    self.__maxt(t)
    
  def addVolumeChange(self,time,vol):
    Limits.checkTime(time)
    Limits.checkVolume(vol)
    self.mf.addControllerEvent(\
     self.tr,self.ch,time,7,vol)
    self.__maxt(time)
    self.lastVolume = vol

  def addPitchBend1(self,time,bend):
    b = Limits.mapPitchBend1(bend)
    Limits.checkTime(time)
    Limits.checkPitchBend(b)
    self.mf.addPitchWheelEvent(\
     self.tr,self.ch,time,b)
    self.__maxt(time)
    self.lastPitchBend1 = bend

  def addNote(self,pitch,time,dur,vel):
    Limits.checkPitch(pitch)
    Limits.checkTime(time)
    Limits.checkDuration(dur)
    Limits.checkVelocity(vel)
    self.mf.addNote(\
    	self.tr,self.ch,\
    	pitch,time,dur,vel)
    self.__maxt(time+dur)
  
  def addMidiNote(self,mn):
    if isinstance(mn.p,list):
      for p in mn.p:
        self.addNote(p,mn.t,mn.d,mn.v)
    else:
      self.addNote(mn.p,mn.t,mn.d,mn.v)
    
  def writeFile(self,fileName):
    with open(fileName, "wb") as o:
      self.mf.writeFile(o)
