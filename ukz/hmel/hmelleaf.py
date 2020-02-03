from abc import abstractmethod
from ukz.melody import Tone,Bend,BendVertex,Fmel,Note,Gradient
from .hmelwithtimes import HmelWithTimes
from fractions import Fraction
from math import floor
from ukz.utils import PwLinFunc
from .hmel import Hmel

################################

class HmelLeaf(Hmel):
    
  def __init__(self,d=1):
    Hmel.__init__(self)
    self.d = d
  def copyFrom(self,other):
    Hmel.copyFrom(self,other)
    self.d = other.d
    
  def allLeaves(self):
    yield self
  def replaceDescendants(self,d,f):
    return f(self)
  def filterDescendants(self,d,f):
    return self if f(self) else None
  def getDescendants(self,d):
    yield self
  
  def allNodesWithTimes(self):
    yield HmelWithTimes(0,self.d,self)
    
  def computeD(self):
    return self.lf*self.d
    
  def durTo(self,d):
    return
