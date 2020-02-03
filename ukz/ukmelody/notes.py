from fractions import Fraction
from .note import Note
from .events import Events
from .scale import Scale
from ukz.utils import cycle

################################

class Notes(Events):
    
  def __init__(self):
    Events.__init__(self)
  def blankCopy(self):
    return Notes()
        
  def choirize(self):
    # hashmap: for each (p,l) pair, store
    # the latest note that should be sung.
    hm = {}
    for e in self.events:
      key = (e.p,e.l)
      x = hm.get(key,None)
      if x is None:
        # new (p,l) pair, don't modify e
        hm[key] = e
      elif x.t+x.d < e.t:
        # gap found, update hm
        hm[key] = e
      else:
        # x.t2 = max(x.t2, e.t2)
        x.d = max(x.d, e.t+e.d-x.t)
        # don't play e, it's covered by x.
        # Keep it for its props though.
        e.p = None

  def __injectNotes_h(self,duration,notes):
   for n1 in self.events:
     for n2 in notes:
       p = n1.p + n2.p
       t = n1.t*duration + n2.t
       d = n1.d * n2.d
       l = n1.l + n2.l - 5
       props = n1.props.copy()
       for (k,v) in n2.props.items():
         props[k] = v
       yield Note(p,t,d,l,props)

  def injectNotes(self,duration,notes):
    self.events = list(self.__injectNotes_h(duration,notes))

  def zipDurations(self,notes):
    for (x,y) in zip(self.events, cycle(notes.events)):
      x.d = y.d
