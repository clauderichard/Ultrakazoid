from abc import abstractmethod
from ukz.melody import Tone,Bend,BendVertex,Fmel,Note,Gradient
from fractions import Fraction
from math import floor
from ukz.utils import PwLinFunc
from .hmelleaf import HmelLeaf
from .copyutil import trycopy

################################

class HmelNote(HmelLeaf):
    
  def __init__(self,d=1,tone=None):
    HmelLeaf.__init__(self,d)
    self.tone = tone
    self.dur = d
  def copyFrom(self,other):
    HmelLeaf.copyFrom(self,other)
    self.tone = trycopy(other.tone)
    self.dur = other.dur
    
  def isHmelNote(self):
    return True

  def allNotes(self):
    yield self

  def durTo(self,d):
    self.dur = d
    return self
    
  def playUntil(self,t):
    if t>=self.d:
      return self
    else:
      x = self.copy()
      x.dur = min(self.d,t)
      return x
      
  def blowUpInto(self,mel):
    m = mel.copy()
    m.transposeUp(self.tone.p)
    m.blendWithLoudness(self.tone.l)
    m.expand(self.dur)
    m.lf *= Fraction(self.d,self.dur)
    if m.pitchBend is None:
      m.pitchBend = self.pitchBend
    if m.volumeBend is None:
      m.volumeBend = self.volumeBend
    if self.tone.pl:
      m.lockP()
    if self.tone.ll:
      m.lockL()
    return m

################################
