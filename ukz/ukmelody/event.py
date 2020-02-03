from fractions import Fraction
from ukz.midi import Limits

class Event:
  
  def __init__(self,t,d,props={}):
    self.t = t
    self.d = d
    self.props = props.copy()
  def copy(self):
    return Event(self.t,self.d,self.props)
  def __eq__(self,other):
    return self.t == other.t \
     and self.d == other.d \
     and self.props == other.props

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
    
  def getStartTime(self):
    return self.t
  def getEndTime(self):
    return self.t + self.d
  def setDForEndTime(self,endTime):
    self.d = endTime - self.t

  def checkLimits(self):
    Limits.checkTime(self.t)
    Limits.checkDuration(self.d)

  def expand(self,fac):
    self.t *= fac
    self.d *= fac
  def contract(self,fac):
    if fac==0:
      raise ValueError('Cannot contract Event by a factor of zero, as that would be dividing by zero.')
    self.t = Fraction(self.t,fac)
    self.d = Fraction(self.d,fac)
  def expandToEndTime(self,endTime):
    et = self.getEndTime()
    if et == 0:
      raise ValueError('Cannot expand zero-end-time event until some target end time')
    factor = Fraction(endTime,et)
    self.expand(factor)


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
  def overlapsWithAny(self,events):
    for e in events:
      if self.overlapsWith(e):
        return True
    return False

def eventListsOverlap(events1,events2):
  xs = iter(sorted(events1))
  ys = iter(sorted(events2))
  x = next(xs)
  y = next(ys)
  try:
    while True:
      if x.overlapsWith(y):
        return True
      if x.t < y.t:
        x = next(xs)
      else:
        y = next(ys)
  except StopIteration:
    return False