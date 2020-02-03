from abc import abstractmethod
from ukz.melody import Tone,Bend,BendVertex,Fmel,Note,Gradient
from fractions import Fraction
from math import floor
from ukz.utils import PwLinFunc
from .hmel import trycopy
from .hmelnode import HmelNode
from .hmelwithtimes import HmelWithTimes

################################

class HmelRep(HmelNode):

  def __init__(self,\
   child=None,times=1,remc=None):
    HmelNode.__init__(self)
    self.child = child
    self.times = times
    self.remc = remc
  def copyFrom(self,other):
    HmelNode.copyFrom(self,other)
    self.child = trycopy(other.child)
    self.times = other.times
    self.remc = trycopy(other.remc)

  def allNodesWithTimes(self):
    # children
    t = 0
    d = self.child.computeD()
    nwts = list(self.child.allNodesWithTimes())
    for _ in range(0,self.times):
      for nwt in nwts:
        yield HmelWithTimes(t+nwt.t,nwt.d,nwt.node)
      t += d
    if self.remc is not None:
      d = self.remc.computeD()
      for nwt in \
       self.remc.allNodesWithTimes():
        yield HmelWithTimes(t+nwt.t,nwt.d,nwt.node)
      t += d
    yield HmelWithTimes(0,t,self)

  def allChildren(self):
    yield self.child
    if self.remc is not None:
      yield self.remc
      
  def mapChildren(self,f):
    if self.child is not None:
      self.child = f(self.child)
    if self.remc is not None:
      self.remc = f(self.remc)
    return self

  def filterChildren(self,f):
    if not f(self.child):
      self.child = None
    if not f(self.remc):
      self.remc = None

  def computeD(self):
    x = self.times * self.child.computeD()
    if self.remc is not None:
      x += self.remc.computeD()
    return self.lf * x

  def playUntil(self,t):
    raise Exception("not implemented")

################################
