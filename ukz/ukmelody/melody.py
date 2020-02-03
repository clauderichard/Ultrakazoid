from fractions import Fraction
from .scale import Scale,pitchToWhiteIndex
from .note import Note
from .gradient import Gradient,GradientVertex
from .event import Event
from .history import History
from ukz.utils import PwLinFunc,cycle

class Melody(History):

  def __init__(self,t=0,d=0):
    History.__init__(self,t,d)
    self.notes = []
    self.gradients = []
    for _ in range(0,Gradient.numTypes):
      self.gradients.append([])
    self.choirized = False
  def reset(self):
    self.t = 0
    self.d = 0
    self.notes = []
    self.gradients = []
    for _ in range(0,Gradient.numTypes):
      self.gradients.append([])
    self.choirized = False
  def copy(self):
    m = Melody(self.t,self.d)
    m.notes = []
    for n in self.notes:
      m.notes.append(n.copy())
    for i in range(0,Gradient.numTypes):
      m.gradients[i] = []
      for g in self.gradients[i]:
        m.gradients[i].append(g.copy())
    m.choirized = self.choirized
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
  # insert a note or gradient,
  # without changing time-bounds of the whole melody
  def insertEvent(self,event):
    if isinstance(event,Note):
      self.notes.append(event)
    elif isinstance(event,Gradient):
      self.gradients[event.type].append(event)
  def clearEvents(self):
    self.notes = []
    for i in range(0,Gradient.numTypes):
      self.gradients[i] = []

  def sortNotes(self):
    self.notes.sort()
  def sortGradients(self):
    for gs in self.gradients:
      gs.sort()
  def sort(self):
    self.sortNotes()
    self.sortGradients()
    
  def forAllNotes(self,f,*args):
    for n in self.notes:
      f(n,*args)
  def forAllGradients(self,typ,f,*args):
    for g in self.gradients[typ]:
      f(g,*args)
  def forAllGradientsAllTypes(self,f,*args):
    for gs in self.gradients:
      for g in gs:
        f(g,*args)

  def isIncompatibleWithGradient(self,gradient):
    return gradient.overlapsWithAny(self.gradients[gradient.typ])

  def insertNote(self,note):
    self.notes.append(note)
  def insertGradient(self,gradient):
    self.gradients[gradient.typ].append(gradient)
  def insertMelody(self,melody):
    self.notes.extend(melody.notes)
    for i in range(0,Gradient.numTypes):
      self.gradients[i].extend(melody.gradients[i])
  def appendNote(self,note):
    if isinstance(note,list):
      d = self.d
      for n in note:
        self.d = d
        self.appendNote(n)
    elif isinstance(note,int):
      self.insertNote(Note(note,self.getEndTime()))
      self.d += 1
    else:
      n = note.copy()
      n.forward(self.getEndTime())
      self.d += n.d
      self.insertNote(n)
  def appendMelody(self,melody):
    m = melody.copy()
    m.forward(self.getEndTime())
    self.d += melody.getEndTime()
    self.insertMelody(m)
      
  def transposeUp(self,numSemitones=1):
    if isinstance(numSemitones,list):
      s = self.copy()
      self.reset()
      for p in numSemitones:
        m2 = s.copy()
        m2.transposeUp(p)
        self.appendMelody(m2)
    else:
      self.forAllNotes(\
       Note.translateUp,numSemitones)
  def chromUp(self,numSemitones=1):
    if isinstance(numSemitones,list):
      s = self.copy()
      self.reset()
      for p in numSemitones:
        m2 = s.copy()
        m2.transposeUp(p)
        self.appendMelody(m2)
    else:
      self.forAllNotes(\
       Note.translateUp,numSemitones)
  def transposeDown(self,numSemitones=1):
    self.forAllNotes(\
     Note.translateDown,numSemitones)
      
  # Todo: ProcessNoteProperties (like Cosmic Blitz used)

  def choirize(self):
    # hashmap: for each (p,l) pair, store
    # the latest note that should be sung.
    hm = {}
    for e in self.notes:
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
    self.choirized = True

  # like choirize, but just get rid of overlaps,
  # don't really merge. For avoiding midi errors.
  def deinterleave(self):
    # hashmap: for each (p,l) pair, store
    # the latest note that should be sung.
    hm = {}
    for e in self.notes:
      key = e.p
      x = hm.get(key,None)
      if x is None:
        # new p, don't modify e
        hm[key] = e
      elif x.t+x.d < e.t:
        # gap found, update hm
        hm[key] = e
      else:
        x.d = min(x.d, e.t-x.t)
        # If the same note at the same time, just take the second one.
        if x.d == 0:
          x.p = None
          hm[key] = e
    a = 0

  def scaleAt(self,index):
    notes = self.notes
    pitches = map(lambda n: n.p, notes)
    scale = Scale(list(pitches))
    return scale.scaleAt(index)
    
  def injectMelody(self,mel):
    #etime = self.getEndTime()
    timefac = mel.getEndTime()
    ns = self.notes.copy()
    gss = list(map(lambda g: g.copy(), self.gradients))
    self.clearEvents()
    for n in ns:
      m = mel.copy()
      m.forAllNotes(Note.translateUp,n.p)
      m.forAllNotes(Note.addL,n.l-5)
      m.expand(n.d)
      m.forward(n.t*timefac)
      self.insertMelody(m)
    for gs in gss:
      for g in gs:
        g.expand(timefac)
        self.insertGradient(g)
    self.t *= timefac
    self.d *= timefac

  def zipNoteDurations(self,melody):
    for (x,y) in zip(self.notes, cycle(melody.notes)):
      x.d = y.d

  def expand(self,fac):
    self.forAllTime(Event.expand,fac)
  def hasNotes(self):
    return not self.notes.events
  def lastNoteStartTime(self):
    mm = max(map(lambda n: n.t, \
       self.notes.events))
    return max(0,mm)
    
  def getStartTimeForBend(self):
    return self.t
  def getDurationForBend(self,bendMel):
    if self.d != 0 or self.hasNotes():
      return self.d
    return bendMel.lastNoteStartTime() - bendMel.t

  def bendWithMelody(self,\
   mel,typ,v1,v2,p1,p2):
    g = Gradient(typ,0,1)
    g.t = self.getStartTimeForBend()
    g.d = self.getDurationForBend(mel)
    for n in mel.notes:
      val = PwLinFunc.interpolate(\
       p1,p2,v1,v2,n.p)
      g.addVertex(n.t,val,n.props)
    g.normalizeVertexTimes()
    if self.isIncompatibleWithGradient(g):
      raise ValueError('Gradient incompatible')
    self.insertGradient(g)
  def volumeBendWithMelody(self,mel):
    self.bendWithMelody(mel,\
     Gradient.volumeTyp,\
     0,1,0,12)
  def pitchBendWithMelody(self,mel):
    self.bendWithMelody(mel,\
     Gradient.pitchBendTyp,\
      -2,2,0,24)

  def lock(self,arg):
    self.forAllNotes(Note.lock)
  def durationUntilEnd(self):
    m = {}
    et = self.getEndTime()
    for n in self.notes:
      if n.getEndTime() < et:
        n.setDForEndTime(et)
      x = m.get(n.p,None)
      if x is None:
        m[n.p] = []
      m[n.p].append(n)
    # get rid of overlaps?
    for _,ns in m.items():
      for i in range(0,len(ns)-1):
        a = ns[i]
        b = ns[i+1]
        if a.t+a.d > b.t:
          a.d = b.t-a.t
          
  def preen(self):
    ns = []
    for n in sorted(self.notes):
      if n.p is not None:
        ns.append(n)
    self.notes = ns
