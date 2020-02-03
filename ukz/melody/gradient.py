from .event import Event
from .bend import Bend,BendVertex
from ukz.utils import PwLinFunc
from math import floor,ceil
from fractions import Fraction

class WGradientVertex:

  def __init__(self,time,val):
    self.t = time
    self.v = val
  def copy(self):
    return WGradientVertex(self.t,self.v)
  def __eq__(self,other):
    return self.t == other.t \
     and self.v == other.v


class Gradient(Event):

  volumeTyp = 0
  pitchBendTyp = 1
  numTypes = 2

  def __init__(self,typ=0,t=0,d=1,\
   bend=None):
    Event.__init__(self,t,d)
    self.bend = Bend() \
     if bend is None else bend
  def copy(self):
    return Gradient(99,\
     self.t,self.d,self.bend.copy())
  def __eq__(self,other):
    return Event.__eq__(self,other) \
     and self.bend == other.bend
      
  def addVertex(self,t,val):
    #v = GradientVertex(t,val)
    #self.vs.append(v)
    bv = BendVertex(t,val)
    self.bend.vs.append(bv)
        
  def mappedVals(self,x0,x1,y0,y1):
    bvs = map(lambda bv: BendVertex(bv.t, \
     PwLinFunc.interpolate(\
     x0,x1,y0,y1,bv.v)),self.bend.vs)
    return Gradient(99,\
     self.t,self.d,Bend(list(bvs)))
      
  def absTimeVertices(self):
    for v in self.bend.vs:
      t = PwLinFunc.interpolate(\
       0,1,self.t,self.t+self.d,v.t)
      yield (t,v.v)
        
  def getIntPoints(self,v0):
    (t1,v1) = (self.t,floor(v0))
    for (tvt,tvv) in self.absTimeVertices():
      (t2,v2) = (tvt,floor(tvv))
      if t1==t2:
        yield BendVertex(\
         t2,v2)
      elif v1<v2:
        for v in range(v1+1,v2+1):
          t = PwLinFunc.interpolate(\
             v1,v2,t1,t2,v)
          yield BendVertex(t,v)
      elif v1>v2:
        for v in range(\
         v1-1,v2-1,-1):
          t = PwLinFunc.interpolate(\
           v2,v1,t2,t1,v)
          yield BendVertex(t,v)
      (t1,v1) = (t2,v2)
