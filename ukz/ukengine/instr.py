from .amp import Amp
from ukz.midi import \
 programs,drumKits,Limits,\
 MidiNote,DrumPitch
from ukz.ukmelody import Note,Gradient
from math import floor
from fractions import *

################################

class InstrBase:
  
  def __init__(self,\
   isDrums,prog,amp):
    self.isDrums = isDrums
    self.prog = prog
    self.amp = amp if \
     isinstance(amp,Amp) \
     else Amp(amp)

  def writerSwitchToInstr(self,midiw):
    raise Exception('must implement method in derived class')

  def writeProgramChange(self,midiw):
    prog = self.prog
    midiw.addProgramChange(0,prog)
    
  def writeInitialVolume(self,midiw):
    midiw.addVolumeChange(0,self.amp[None])

  def mapNoteToMidiNote(self,note):
    return MidiNote(0,0,1,1)

  def writeNote(self,midiw,note):
    mn = self.mapNoteToMidiNote(note)
    if mn.shouldWrite():
      midiw.addMidiNote(mn)
      
  def writeVolGrad(self,\
   midiw,g):
    mv = self.amp[None]
    v0 = Fraction(\
     midiw.lastVolume,mv)
    gg = g.mappedVals(0,1,\
     Limits.minVolume,mv)
    for gv in gg.getIntPoints(v0):
      t = gv.t
      val = gv.v
      midiw.addVolumeChange(t,val)
  def writePitchGrad(self,\
   midiw,g):
    mv = self.amp[None]
    v0 = Fraction(\
     midiw.lastPitchBend1,mv)
    gg = g.mappedVals(-2,2,\
     Limits.minPitchBend1,\
     Limits.maxPitchBend1)
    for gv in gg.getIntPoints(v0):
      t = gv.t
      midiw.addPitchBend1(t,gv.v)
  def writeGradient(self,\
   midiw,gradient):
    if gradient.typ == \
     Gradient.volumeTyp:
      self.writeVolGrad(\
       midiw,gradient)
    else:
      self.writePitchGrad(\
       midiw,gradient)

################################

class Instr(InstrBase):
  
  def __init__(self,\
   prog=0,octave=0,amp={}):
    p = prog if isinstance(prog,int) \
     else programs[prog]
    InstrBase.__init__(\
     self,False,p,amp)
    self.octave = octave
    
  def writerSwitchToInstr(self,midiw):
    midiw.switchToInstr()
    self.writeProgramChange(midiw)
  
  def mapNoteToMidiNote(self,note):
    if note.p is None:
      return MidiNote(note.p,note.t,note.d,Limits.minVelocity)
    p = note.p + 12*self.octave
    v = self.amp[p,note.l]
    return MidiNote(p,note.t,note.d,v)

################################

class Drums(InstrBase):
  
  def __init__(self,\
   kit=0,amp={}):
    p = kit \
     if isinstance(kit,int) \
     else drumKits[kit]
    InstrBase.__init__(\
    	self,True,p,amp)
  
  def writerSwitchToInstr(self,midiw):
    midiw.switchToDrums()
    self.writeProgramChange(midiw)
  
  def mapNoteToMidiNote(self,note):
    if (note.p == None):
      return MidiNote(None,note.t,note.d,0)
    v = self.amp[note.p,note.l]
    p = DrumPitch.mapToMidi(note.p)
    return MidiNote(p,note.t,note.d,v)

################################
