from ukz.midi import Limits
from .event import Event
from .scale import pitchToWhiteIndex

class Note(Event):
  
  def __init__(self,p=0,t=0,d=1,l=5,\
   pLocked=False,lLocked=False):
    if isinstance(p,Note):
      self.__init__(p.p,p.t,p.d,p.l,\
       pLocked,lLocked)
    else:
      Event.__init__(self,t,d)
      self.p = p
      self.l = l
      self.pLocked = pLocked
      self.lLocked = lLocked
  def copy(self):
    return Note(self.p,self.t,\
     self.d,self.l,self.pLocked,self.lLocked)
  def __eq__(self,other):
    return Event.__eq__(self,other) \
     and self.p == other.p \
     and self.l == other.l
  
  def checkLimits(self):
    Event.checkLimits(self)
    Limits.checkPitch(self.p)
    Limits.checkVelocity(self.l)

  def alterP(self,f):
    if self.p is None or self.pLocked:
      return
    self.p = f(self.p)
  def alterL(self,f):
    if self.l is None or self.lLocked:
      return
    self.l = f(self.l)
    
  def setP(self,p):
    self.p = p
  def setL(self,l):
    self.l = l
  
  def translateUp(self,dp):
    self.alterP(lambda p: p+dp)
  def translateDown(self,dp):
    self.alterP(lambda p: p-dp)

  def addL(self,dl):
    self.l += dl
  def subL(self,dl):
    self.l -= dl
    
  def lockP(self):
    self.pLocked = True
  def lockL(self):
    self.lLocked = True

  def atScale1(self,sc):
    self.p = sc.scaleAt(self.p)
  def atScale2(self,sc):
    self.p = sc[pitchToWhiteIndex(self.p)]

  def __lt__(self,other):
    if self.t == other.t:
      return self.p < other.p
    return self.t < other.t
    