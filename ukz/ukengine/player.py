#from math import *
#from ukz.midi import *
from ukz.uklang import ukd,ukz
from ukz.utils import cartProd
from .instr import Instr,Drums
from ukz.ukmelody import Melody
#from .note import *
#from .gradient import *
from fractions import Fraction

########################

class PlayerBase:

  def __init__(self):
    self.melody = Melody()

  def getInstrs(self):
    return []

  def parseUk(self,ukzStr):
    return Melody()

  def play(self,ukStr):
    melody = self.parseUk(ukStr)
    self.melody.appendMelody(melody)

  def goto(self,other):
    if isinstance(other,int):
      self.melody.time = other
    elif isinstance(other,Fraction):
      self.melody.time = other
    elif isinstance(other,PlayerBase):
      self.melody.time = other.melody.time
    else:
      raise ValueError('Unsupported argument type')

  def writeMelody(self,midiw,instr):
    for voice in self.melody.voices:
      self.writeVoice(midiw,instr,voice)
      
  def writeVoice(self,midiw,instr,voice):
    instr.writerSwitchToInstr(midiw)
    instr.writeProgramChange(midiw)
    instr.writeInitialVolume(midiw)
    self.writeNotes(midiw,instr,voice.notes)
    for gs in voice.gradients:
      self.writeGradients(midiw,instr,gs)
      
  def writeNotes(self,midiw,instr,notes):
    for note in notes:
      instr.writeNote(midiw,note)
      
  def writeGradients(self,midiw,instr,gradients):
    for gradient in gradients:
      instr.writeGradient(midiw,gradient)

  def write(self,midiw):
    self.melody.sort()
    for instr in self.getInstrs():
      self.writeMelody(midiw,instr)
        
########################

class Drummer(PlayerBase):

  def __init__(self,*args):
    PlayerBase.__init__(self)
    a0 = args[0]
    if isinstance(a0,Drums):
      if len(args) > 1:
        raise ValueError("Cannot have more than one Drums instrument")
      self.drums = a0
    else:
      ars = []
      for a in args:
        x = a if isinstance(a,list) else [a]
        ars.append(x)
      ys = list(cartProd(*ars))
      if len(ys) > 1:
        raise ValueError('Too many drums')
      yargs = ys[0]
      self.drums = Drums(*yargs)

  def getInstrs(self):
    return [self.drums]

  def parseUk(self,ukStr):
    return ukd(ukStr)
    
  def writeProgramChange(self,midiw):
    midiw.switchToDrums()

########################

class Player(PlayerBase):

  def __init__(self,*args):
    PlayerBase.__init__(self)
    a0 = args[0]
    if isinstance(a0,Instr):
      self.instrs = list(args)
    else:
      ars = []
      for a in args:
        x = a if isinstance(a,list) else [a]
        ars.append(x)
      ys = cartProd(*ars)
      self.instrs = list(map(lambda y: Instr(*y), ys))

  def getInstrs(self):
    return self.instrs

  def parseUk(self,ukStr):
    return ukz(ukStr)

  def choirize(self):
    self.melody.choirize()
  