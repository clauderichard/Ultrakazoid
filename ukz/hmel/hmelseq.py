from abc import abstractmethod
from ukz.melody import Tone,Bend,BendVertex,Fmel,Note,Gradient
from .hmelwithtimes import HmelWithTimes
from fractions import Fraction
from math import floor
from ukz.utils import PwLinFunc
from .hmelnode import HmelNode
from .copyutil import listcopies

################################

class HmelSeq(HmelNode):

  def __init__(self,\
   children=[],prechildren=[],postchildren=[]):
    HmelNode.__init__(self)
    self.children = list(children)
    self.prechildren = list(prechildren)
    self.postchildren = list(postchildren)
  def copyFrom(self,other):
    HmelNode.copyFrom(self,other)
    self.children = listcopies(other.children)
    self.prechildren = listcopies(other.prechildren)
    self.postchildren = listcopies(other.postchildren)
  
  def allNodesWithTimes(self):
    # prechildren
    t = 0
    xs = []
    for c in reversed(self.prechildren):
      d = c.computeD()
      t -= d
      for nwt in c.allNodesWithTimes():
        xs.append(HmelWithTimes(t+nwt.t,nwt.d,nwt.node))
    for x in reversed(xs):
      yield x
    # children
    t = 0
    for c in self.children:
      d = c.computeD()
      for nwt in c.allNodesWithTimes():
        yield HmelWithTimes(t+nwt.t,nwt.d,nwt.node)
      t += d
    selfD = t
    # postchildren
    for c in self.postchildren:
      d = c.computeD()
      for nwt in c.allNodesWithTimes():
        yield HmelWithTimes(t+nwt.t,nwt.d,nwt.node)
      t += d
    yield HmelWithTimes(0,selfD,self)

  def allChildren(self):
    return self.prechildren + self.children + self.postchildren

  def mapChildren(self,f):
    self.prechildren = list(map(f, self.prechildren))
    self.children = list(map(f, self.children))
    self.postchildren = list(map(f, self.postchildren))
    return self

  def filterChildren(self,f):
    self.children = list(filter(f, self.children))
    self.prechildren = list(filter(f, self.prechildren))
    self.postchildren = list(filter(f, self.postchildren))
  
  def computeD(self):
    return self.lf*sum(map(lambda x: \
     x.computeD(), self.children))

  def durTo(self,d):
    dd = d
    for c in self.children:
      c.durTo(dd)
      dd -= c.computeD()
      
  def playUntil(self,t):
    tt = 0
    xs = []
    for c in self.children:
      if tt >= t:
        return HmelSeq(xs)
      d = c.computeD()
      if tt+d <= t:
        xs.append(c)
      else:
        xs.append(c.playUntil(t-tt))
        return HmelSeq(xs)
      tt += d
    return HmelSeq(xs)

################################
