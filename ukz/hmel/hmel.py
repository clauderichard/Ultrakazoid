from abc import abstractmethod
from ukz.melody import Tone,Bend,BendVertex,Fmel,Note,Gradient
from fractions import Fraction
from math import floor
from ukz.utils import PwLinFunc
from .copyutil import trycopy

################################

class Hmel:
  
  def __init__(self):
    self.pitchBend = None
    self.volumeBend = None
    self.lf = 1
  def copyFrom(self,other):
    self.pitchBend = trycopy(other.pitchBend)
    self.volumeBend = trycopy(other.volumeBend)
    self.lf = other.lf

  def copy(self):
    x = self.__class__()
    x.copyFrom(self)
    return x

################################
# (needed?)

  def isHmelNote(self):
    return False

################################
# Abstract methods

  @abstractmethod
  def allNodesWithTimes(self):
    pass

  def allHmelNotesWithTimes(self):
    for x in self.allNodesWithTimes():
      if x.node.isHmelNote():
        yield x

  @abstractmethod
  def computeD(self):
    pass

  @abstractmethod
  def playUntil(self,t):
    pass

  @abstractmethod
  def allLeaves(self):
    pass
  @abstractmethod
  def allNotes(self):
    pass

  @abstractmethod
  def replaceDescendants(self,d,f):
    pass

  @abstractmethod
  def filterDescendants(self,d,f):
    pass

  @abstractmethod
  def durTo(self,t):
    pass

  @abstractmethod
  def getDescendants(self,d):
    pass

################################

  def getFlattenedNotes(self):
    for nwt in self.allHmelNotesWithTimes():
      tn = nwt.node.tone
      yield Note(tn.p,nwt.t,nwt.node.dur,tn.l)
  def getFlattenedPitchGradients(self):
    for nwt in self.allNodesWithTimes():
      if nwt.node.pitchBend is None:
        continue
      g = Gradient(Gradient.pitchBendTyp,nwt.t,nwt.d)
      for ve in nwt.node.pitchBend.vs:
        g.addVertex(ve.t, ve.v)
      yield g
  def getFlattenedVolumeGradients(self):
    for nwt in self.allNodesWithTimes():
      if nwt.node.volumeBend is None:
        continue
      g = Gradient(Gradient.volumeTyp,nwt.t,nwt.d)
      for ve in nwt.node.volumeBend.vs:
        g.addVertex(ve.t, ve.v)
      yield g
  def flatten(self):
    d = self.computeD()
    m = Fmel()
    m.notes = list(self.getFlattenedNotes())
    m.gradients[Gradient.pitchBendTyp] = \
     list(self.getFlattenedPitchGradients())
    m.gradients[Gradient.volumeTyp] = \
     list(self.getFlattenedVolumeGradients())
    m.t = 0
    m.d = d
    return m
    
  def mapToBend(self,typ,\
   v1,v2,p1,p2):
    vs = []
    mel = self.flatten()
    et = mel.lastNoteStartTime()
    if et==0:
      et = 1
    for n in mel.notes:
      t = Fraction(n.t,et)
      val = PwLinFunc.interpolate(\
       p1,p2,v1,v2,n.p)
      vs.append(BendVertex(t,val))
    return Bend(vs)

  def repeatUntil(self,t):
    d = self.computeD()
    times = floor(t/d)
    if times*d < t:
      cl = self.playUntil(t-times*d)
      from .hmelrep import HmelRep
      return HmelRep(self,times,cl)
    else:
      return self.repeat(times)
  def repeat(self,times):
    from .hmelrep import HmelRep
    return HmelRep(self,times)
    
  def forEachTone(self,f,*a):
    for n in self.allNotes():
      f(n.tone,*a)
    return self

  def mapEachD(self,f):
    for n in self.allLeaves():
      n.d = f(n.d)
    return self
  def mapEachDur(self,f):
    for n in self.allNotes():
      n.dur = f(n.dur)
    return self

  def listLeaves(self,d):
    return self.getDescendants(-1)
  def replaceLeaves(self,f):
    return self.replaceDescendants(-1,f)
  def filterNotes(self,f):
    return self.filterDescendants(\
     -1, lambda n: f(n) \
     if self.isHmelNote() \
     else True)
  
  def transposeUp(self,dp=1):
    return self.forEachTone(Tone.transposeUp,dp)
  def transposeDown(self,dp=1):
    return self.forEachTone(Tone.transposeDown,dp)
  def blendWithLoudness(self,l=5):
    return self.forEachTone(Tone.blendWithLoudness,l)

  def lockP(self):
    return self.forEachTone(Tone.lockP)
  def lockL(self):
    return self.forEachTone(Tone.lockL)

  def expand(self,f):
    self.mapEachD(lambda x: x*f)
    self.mapEachDur(lambda x: x*f)
    return self
  def contract(self,f):
    return self.expand(Fraction(1,f))
  def expandTo(self,d):
    return self.expand(Fraction(\
     d, self.computeD()))
    	
  def setDur(self,d):
    return self.mapEachDur(lambda x: d)
  def durToEnd(self):
    self.durTo(self.computeD())
    return self

  def blowUpLeavesIntoMelody(self,mel):
    return self.replaceLeaves(lambda l: l.blowUpInto(mel))

################################
