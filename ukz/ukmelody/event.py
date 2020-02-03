from fractions import Fraction
from ukz.midi import Limits

class Event:
  
  def __init__(self,t,d,props={}):
    self.t = t
    self.d = d
    self.props = props.copy()
  def copy(self):
    return Event(self.t,self.d,self.props)

  def setT(self,t):
    self.t = t
  def setD(self,d):
    self.d = d
  def setProp(self,name,val):
    self.props[name] = val
  def setProps(self,props):
    for k,v in props.items():
      self.props[k] = v

  def alterT(self,f):
    if self.t is None:
      return
    self.t = f(self.t)
  def alterD(self,f):
    if self.d is None:
      return
    self.d = f(self.d)

  def __lt__(self,other):
    return self.t < other.t
    
  def checkLimits(self):
    Limits.checkTime(self.t)
    Limits.checkDuration(self.d)

  def expand(self,fac):
    self.t *= fac
    self.d *= fac
  def contract(self,fac):
    self.t = Fraction(self.t,fac)
    self.d = Fraction(self.d,fac)

  def forward(self,dt):
    self.t += dt
  def backward(self,dt):
    self.t -= dt

  def durExpand(self,fac):
    self.d *= fac
  def durContract(self,fac):
    self.d = Fraction(self.d,fac)
  def durExtend(self,dd):
    self.d += dd
  def durShorten(self,dd):
    self.d -= dd

  def overlapsWith(self,event):
    if self.t+self.d <= event.t:
      return False   
    if event.t+event.d <= self.t:
      return False
    return True
