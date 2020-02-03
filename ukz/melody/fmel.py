from fractions import Fraction
from .scale import Scale,pitchToWhiteIndex
from .note import Note
from .bend import Bend,BendVertex
from .gradient import Gradient
from .event import Event
from .history import History
from ukz.utils import PwLinFunc,cycle

class Fmel(History):

  def __init__(self,t=0,d=0):
    History.__init__(self,t,d)
    self.notes = []
    self.gradients = []
    for _ in range(0,Gradient.numTypes):
      self.gradients.append([])
    #self.choirized = False
  def reset(self):
    self.t = 0
    self.d = 0
    self.notes = []
    self.gradients = []
    for _ in range(0,Gradient.numTypes):
      self.gradients.append([])
    #self.choirized = False
  def copy(self):
    m = Fmel(self.t,self.d)
    m.notes = []
    for n in self.notes:
      m.notes.append(n.copy())
    for i in range(0,Gradient.numTypes):
      m.gradients[i] = []
      for g in self.gradients[i]:
        m.gradients[i].append(g.copy())
    #m.choirized = self.choirized
    return m
  def __eq__(self,other):
    if not Event.__eq__(self,other):
      return False
    if self.notes != other.notes:
      return False
    if self.gradients != other.gradients:
      return False
    return True
    
  # all notes and gradients
  def allSubEvents(self):
    for n in self.notes:
      yield n
    for gs in self.gradients:
      for g in gs:
        yield g
  
  def sortNotes(self):
    self.notes.sort()
  def sortGradients(self):
    for gs in self.gradients:
      gs.sort()
  def sort(self):
    self.sortNotes()
    self.sortGradients()
    
  def insertMelody(self,melody):
    self.notes.extend(melody.notes)
    for i in range(0,Gradient.numTypes):
      self.gradients[i].extend(melody.gradients[i])
  def appendMelody(self,melody):
    m = melody.copy()
    m.forward(self.getEndTime())
    self.d += melody.getEndTime()
    self.insertMelody(m)
  
  def choirize(self):
    # hashmap: for each (p,l) pair, store
    # the latest note that should be sung.
    hm = {}
    self.notes.sort()
    for e in self.notes:
      key = e.p
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
    self.notes = list(filter(lambda x: \
     x.p is not None, self.notes))
    #self.choirized = True

  def lastNoteStartTime(self):
    mm = max(map(lambda n: n.t, \
       self.notes))
    return max(0,mm)

  # like choirize, but just get rid of overlaps,
  # don't really merge. For avoiding midi errors.
  def deinterleave(self):
    # hashmap: for each pitch, store
    # the latest note.
    hm = {}
    for e in self.notes:
      key = e.p
      x = hm.get(key,None)
      if x is None:
        # new p, don't modify e
        hm[key] = e
      elif x.t+x.d <= e.t:
        # gap found, update hm
        hm[key] = e
      else:
        x.d = min(x.d, e.t-x.t)
        # If the same note at the same time, just take the second one.
        if x.d == 0:
          x.p = None
          hm[key] = e
    
  def preen(self):
    ns = []
    for n in self.notes:
      if n.p is not None:
        ns.append(n)
    self.notes = ns
    self.notes.sort()
