from fractions import Fraction
from .event import Event

# A History contains a list of Events,
# but is also itself an Event with a start and end time.
class History(Event):

  def __init__(self,t,d,props={}):
    Event.__init__(self,t,d,props)
  def copy(self):
    return History(self.t,self.d,self.props)

  # You should override this.
  def allSubEvents(self):
    raise ValueError('History is abstract, allSubEvents must be implemented')
  def insertEvent(self,event):
    raise ValueError('History is abstract, insertEvent must be implemented')
  def clearEvents(self):
    raise ValueError('History is abstract, clearEvents must be implemented')

  def forAllEvents(self,f,*args):
    for e in self.allSubEvents():
      f(e,*args)
  def forAllTime(self,f,*args):
    self.forAllEvents(f,*args)
    f(self,*args)

  def forward(self,dt):
    for e in self.allSubEvents():
      e.forward(dt)
    Event.forward(self,dt)
  def backward(self,dt):
    for e in self.allSubEvents():
      e.backward(dt)
    Event.backward(self,dt)
    
  def expand(self,fac):
    for e in self.allSubEvents():
      e.expand(fac)
    Event.expand(self,fac)
  def contract(self,fac):
    for e in self.allSubEvents():
      e.contract(fac)
    Event.contract(self,fac)

  def repeat(self,times):
    # build newEvs array
    timestep = self.getEndTime()
    newEvs = []
    t = 0
    oldEvs = sorted(self.allSubEvents())
    for _ in range(0,times):
      for oldEv in oldEvs:
        newEv = oldEv.copy()
        newEv.forward(t)
        newEvs.append(newEv)
      t += timestep
    # replace self events with newEvs
    self.clearEvents()
    for newEv in newEvs:
      self.insertEvent(newEv)
    # set new time bounds
    self.setDForEndTime(timestep*times)

  def repeatUntilEndTime(self,endTime):
    timestep = self.getEndTime()
    if timestep == 0:
      raise ValueError('cannot repeat a use repeatUntil for a zero-end-time Melody')

    # build newEvs array
    timestep = self.getEndTime()
    newEvs = []
    t = 0
    done = False
    oldEvs = sorted(self.allSubEvents())
    while t < endTime:
      for oldEv in oldEvs:
        newEv = oldEv.copy()
        newEv.forward(t)
        if newEv.t >= endTime:
          done = True
          break
        newEvs.append(newEv)
      if done:
        break
      t += timestep
    # replace self events with newEvs
    self.clearEvents()
    for newEv in newEvs:
      self.insertEvent(newEv)
    # set new time bounds
    self.setDForEndTime(endTime)
    