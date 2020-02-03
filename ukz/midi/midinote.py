from .limits import Limits

class MidiNote:
  
  def __init__(self,p,t,d,v):
    self.p = p
    self.t = t
    self.d = d
    self.v = v

  def checkLimits(self):
    Limits.checkPitch(self.p)
    Limits.checkTime(self.t)
    Limits.checkDuration(self.d)
    Limits.checkVelocity(self.v)
    
  def shouldWrite(self):
    if self.p is None:
      return False
    if self.t is None:
      return False
    if self.d is None:
      return False
    if self.v is None:
      return False
    return True
  