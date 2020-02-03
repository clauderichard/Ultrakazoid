from fractions import Fraction
from .event import Event

class Events:

  def __init__(self):
    self.events = []
  def reset(self):
    self.events = []
  def blankCopy(self):
    print('whaaa')
    return Events()
  def __iter__(self):
    return iter(self.events)

  def copy(self):
    es = self.blankCopy()
    es.events.extend(map(\
     lambda e: e.copy(), self.events))
    return es

  def forAll(self,f,*args):
    for e in self.events:
      f(e,*args)

  def sort(self):
    self.events.sort()

  def repeat(self,timestep,times):
    newEvs = []
    t = 0
    for _ in range(0,times):
      for e in self.events:
        ee = e.copy()
        ee.forward(t)
        newEvs.append(ee)
      t += timestep
    self.events = newEvs

  def repeatUntil(self,timestep,time):
    newEvs = []
    t = 0
    done = False
    while t < time:
      for e in self.events:
        ee = e.copy()
        ee.forward(t)
        if ee.t >= time:
          done = True
          break
        newEvs.append(ee)
      if done:
        break
      t += timestep
    self.events = newEvs
    
  def insert(self,event):
    self.events.append(event)
  def insertAll(self,events):
    self.events.extend(events)

  def processProps(self,func,*propNames):
    for e in sorted(self.events):
      vs = []
      b = True
      for pn in propNames:
        v = e.props.get(pn,None)
        if v is None:
          b = False
          break
        vs.append(v)
      if b:
        func(e,*vs)
  def processPropsAll(self,func,*propNames):
    for e in sorted(self.events):
      vs = []
      for pn in propNames:
        v = e.props.get(pn,None)
        vs.append(v)
      func(e,*vs)

  def overlapsWith(self,events):
    if isinstance(events,Event):
      for x in self.events:
        if x.overlapsWith(events):
          return True
      return False
    if isinstance(events,Events):
      for x in self.events:
        if events.overlapsWith(x):
          return True
      return False
    if not isinstance(events,list):
      raise ValueError('overlapsWith only supports list and Event argument')
    if not self.events or not events:
      return False
    xs = iter(sorted(self.events))
    ys = iter(sorted(events))
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
