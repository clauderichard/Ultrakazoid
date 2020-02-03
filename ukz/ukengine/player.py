from abc import abstractmethod
#from ukz.midi import *
from ukz.uklang import ukd,ukz
from ukz.utils import cartProd
from .instr import Instr,Drums
from ukz.melody import Fmel,Gradient
#from .note import *
#from .gradient import *
from fractions import Fraction

########################

class PlayerBase:

  def __init__(self):
    self.fmel = Fmel()

  @abstractmethod
  def getInstrs(self):
    pass

  @abstractmethod
  def parseUk(self,ukzStr):
    pass

  def play(self,ukStr):
    melody = self.parseUk(ukStr)
    self.fmel.appendMelody(melody)

  def goto(self,other):
    if isinstance(other,int):
      self.fmel.d = other
    elif isinstance(other,Fraction):
      self.fmel.d = other
    elif isinstance(other,PlayerBase):
      self.fmel.d = other.fmel.d
    else:
      raise ValueError('Unsupported argument type')

  def writeMelody(self,midiw,instr):
    instr.writerSwitchToInstr(midiw)
    instr.writeProgramChange(midiw)
    instr.writeInitialVolume(midiw)
    self.writeNotes(midiw,instr,self.fmel.notes)
    self.writePitchGradients(midiw,instr,\
     self.fmel.gradients[Gradient.pitchBendTyp])
    self.writeVolGradients(midiw,instr,\
     self.fmel.gradients[Gradient.volumeTyp])
      
  def writeNotes(self,midiw,instr,notes):
    for note in notes:
      instr.writeNote(midiw,note)
      
  def writePitchGradients(self,midiw,instr,gradients):
    for gradient in gradients:
      instr.writePitchGrad(midiw,gradient)
  def writeVolGradients(self,midiw,instr,gradients):
    for gradient in gradients:
      instr.writeVolGrad(midiw,gradient)

  def write(self,midiw):
    self.fmel.sort()
    #if not self.fmel.choirized:
    self.fmel.deinterleave()
    self.fmel.preen()
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
    self.fmel.choirize()
  