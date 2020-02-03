from abc import abstractmethod
from ukz.melody import Tone,Bend,BendVertex,Fmel,Note,Gradient
from fractions import Fraction
from math import floor
from ukz.utils import PwLinFunc
from .hmel import Hmel
from .hmelleaf import HmelLeaf
from .copyutil import trycopy

################################

class HmelRest(HmelLeaf):
    
  def __init__(self,d=1):
    HmelLeaf.__init__(self,d)
  def copyFrom(self,other):
    HmelLeaf.copyFrom(self,other)

  def allNotes(self):
    return []
    
  def durTo(self,d):
    return self
    
  def playUntil(self,t):
    if t>=self.d:
      return self
    else:
      x = self.copy()
      x.dur = min(self.d,t)
      return x

  def blowUpInto(self,mel):
    x = HmelRest()
    x.d = self.d * mel.computeD()
    Hmel.copyFrom(x,mel)
    return x

################################
