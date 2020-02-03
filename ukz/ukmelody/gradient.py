from .event import Event
from ukz.utils import PwLinFunc
from math import floor,ceil
from fractions import *

class GradientVertex:

  def __init__(self,time,val):
    self.t = time
    self.v = val
  def copy(self):
    return GradientVertex(self.t,self.v)
  def __eq__(self,other):
    return self.t == other.t \
     and self.v == other.v

class Gradient(Event):

  volumeTyp = 0
  pitchBendTyp = 1
  numTypes = 2

  def __init__(self,typ=0,t=0,d=1):
    Event.__init__(self,t,d)
    self.typ = typ
    self.vs = []
  def copy(self):
    g = Gradient(self.typ,self.t,self.d)
    for v in self.vs:
      g.vs.append(v.copy())
    return g
  def __eq__(self,other):
    return Event.__eq__(self,other) \
     and self.typ == other.typ \
     and self.vs == other.vs
      
  def normalizeVertexTimes(self):
    s = self.vs[len(self.vs)-1].t
    if s==0:
      for v in self.vs:
        v.t = 0
    else:
      for v in self.vs:
        v.t = Fraction(v.t,s)
      
  def addVertex(self,t,val,props={}):
    v = GradientVertex(t,val)
    self.vs.append(v)
    for a,b in props.items():
      self.props[a] = b
        
  def mappedVals(self,x0,x1,y0,y1):
    g = Gradient(\
     self.typ,self.t,self.d)
    for v in self.vs:
      vv = PwLinFunc.interpolate(\
       x0,x1,y0,y1,v.v)
      g.addVertex(v.t,vv)
    return g
      
  def absTimeVertices(self):
    for v in self.vs:
      t = PwLinFunc.interpolate(\
       0,1,self.t,self.t+self.d,v.t)
      yield GradientVertex(t,v.v)
        
  def getIntPoints(self,v0):
    (t1,v1) = (self.t,floor(v0))
    for tv in self.absTimeVertices():
      (t2,v2) = (tv.t,floor(tv.v))
      if t1==t2:
        yield GradientVertex(\
         t2,v2)
      elif v1<v2:
        for v in range(v1+1,v2+1):
          t = PwLinFunc.interpolate(\
             v1,v2,t1,t2,v)
          yield GradientVertex(t,v)
      elif v1>v2:
        for v in range(\
         v1-1,v2-1,-1):
          t = PwLinFunc.interpolate(\
           v2,v1,t2,t1,v)
          yield GradientVertex(t,v)
      (t1,v1) = (t2,v2)
