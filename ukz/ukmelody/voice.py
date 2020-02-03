from fractions import Fraction
from .scale import Scale,pitchToWhiteIndex
from .note import Note
from .notes import Notes
from .gradient import Gradient
from .gradients import Gradients

################################

################################

class Voice:
  
  def __init__(self):
    self.notes = Notes()
    self.gradients = []
    for _ in range(0,Gradient.numTypes):
      self.gradients.append(Gradients())
  def reset(self):
    self.notes = []
    self.gradients = [] * Gradient.numTypes
  def copy(self):
    v = Voice()
    v.notes = self.notes.copy()
    for i in range(0,Gradient.numTypes):
      v.gradients[i] = \
       self.gradients[i].copy()
    return v
        
  def sortNotes(self):
    self.notes.sort()
  def sortGradients(self):
    for gs in self.gradients:
      gs.sort()
  def sort(self):
    self.sortNotes()
    self.sortGradients()

  def forAllNotes(self,f,*args):
    self.notes.forAll(f,*args)
  def forAllGradients(self,typ,f,*args):
    self.gradients[typ].forAll(f,*args)
  def forAllGradientsAllTypes(self,f,*args):
    for gs in self.gradients:
      gs.forAll(f,*args)
  def forAllEvents(self,f,*args):
    self.forAllNotes(f,*args)
    self.forAllGradientsAllTypes(f,*args)

  def insertNote(self,note):
    self.notes.insert(note)
  def insertGradient(self,gradient):
    self.gradients[gradient.typ].insert(gradient)
  def insertVoice(self,voice):
    self.notes.events.extend(voice.notes)
    for i in range(0,Gradient.numTypes):
      self.gradients[i].events.extend(voice.gradients[i])

  def repeat(self,timestep,times):
    self.notes.repeat(timestep,times)
    for gs in self.gradients:
      gs.repeat(timestep,times)
  def repeatUntil(self,timestep,time):
    self.notes.repeatUntil(timestep,time)
    for gs in self.gradients:
      gs.repeatUntil(timestep,time)
    
  def choirize(self):
    self.notes.choirize()

  def injectVoice(self,duration,voice):
    self.notes.injectNotes(duration,voice.notes)
    
  def zipDurations(self,voice):
    self.notes.zipDurations(voice.notes)

  #######################

  def isCompatibleWithVoice(self,voice):
    for i in range(0,Gradient.numTypes):
      if self.gradients[i].overlapsWith(voice.gradients[i]):
        return False
    return True
  def isCompatibleWithGradient(self,gradient):
    if self.gradients[gradient.typ].overlapsWith(gradient):
      return False
    return True
    
  #######################
