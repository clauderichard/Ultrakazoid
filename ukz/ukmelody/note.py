from ukz.midi import Limits
from .event import Event
from .scale import pitchToWhiteIndex

class Note(Event):
  
  def __init__(self,p=0,t=0,d=1,l=5,\
   props={},locked=False):
    if isinstance(p,Note):
      self.__init__(p.p,p.t,p.d,p.l,p.props)
    else:
      Event.__init__(self,t,d,props)
      self.p = p
      self.l = l
    self.locked = locked
  def copy(self):
    return Note(self.p,self.t,\
     self.d,self.l,\
     self.props.copy(),self.locked)
  def __eq__(self,other):
    return Event.__eq__(self,other) \
     and self.p == other.p \
     and self.l == other.l \
     and self.locked == other.locked
  
  def checkLimits(self):
    Event.checkLimits(self)
    Limits.checkPitch(self.p)
    Limits.checkVelocity(self.l)

  def alterP(self,f):
    if self.p is None:
      return
    self.p = f(self.p)
  def alterL(self,f):
    if self.l is None:
      return
    self.l = f(self.l)
    
  def setP(self,p):
    self.p = p
  def setL(self,l):
    self.l = l
  
  def translateUp(self,dp):
    if self.locked:
      return
    self.alterP(lambda p: p+dp)
  def translateDown(self,dp):
    if self.locked:
      return
    self.alterP(lambda p: p-dp)

  def addL(self,dl):
    self.l += dl
  def subL(self,dl):
    self.l -= dl

  def atScale1(self,sc):
    self.p = sc.scaleAt(self.p)
  def atScale2(self,sc):
    self.p = sc[pitchToWhiteIndex(self.p)]

  def lock(self):
    self.locked = True
