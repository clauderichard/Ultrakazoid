from abc import abstractmethod
from ukz.melody import Tone,Bend,BendVertex,Fmel,Note,Gradient
from .hmelwithtimes import HmelWithTimes
from fractions import Fraction
from math import floor
from ukz.utils import PwLinFunc
from .hmelnode import HmelNode
from .copyutil import listcopies

################################

class HmelPar(HmelNode):
    
  def __init__(self,children=[],\
  	prechildren=[]):
    HmelNode.__init__(self)
    self.children = list(children)
    self.prechildren = list(prechildren)
  def copyFrom(self,other):
    HmelNode.copyFrom(self,other)
    self.children = listcopies(other.children)
    self.prechildren = listcopies(other.prechildren)
     
  def computeD(self):
    if len(self.children)==0:
      return 0
    return self.lf*self.children[\
     len(self.children)-1]\
     .computeD()
     
  def allNodesWithTimes(self):
    d = 0
    for c in self.prechildren:
      d = c.computeD()
      for nwt in c.allNodesWithTimes():
        yield HmelWithTimes(nwt.t-d,nwt.d,nwt.node)
    d = 0
    for c in self.children:
      d = c.computeD()
      for nwt in c.allNodesWithTimes():
        yield nwt
    yield HmelWithTimes(0,d,self)

  def allChildren(self):
    return self.prechildren + self.children

  def mapChildren(self,f):
    self.children = list(map(f, self.children))
    self.prechildren = list(map(f, self.prechildren))
    return self

  def filterChildren(self,f):
    self.children = list(filter(f, self.children))
    self.prechildren = list(filter(f, self.prechildren))
  
  def durTo(self,d):
    for c in self.prechildren + self.children:
      c.durTo(d)
      
  def playUntil(self,t):
    xs = map(lambda c: \
    	c.playUntil(t), self.children)
    return HmelPar(xs)

################################
