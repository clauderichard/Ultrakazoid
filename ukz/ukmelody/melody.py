from fractions import Fraction
from .scale import Scale,pitchToWhiteIndex
from .note import Note
from .notes import Notes
from .gradient import Gradient,GradientVertex
from .gradients import Gradients
from .voice import Voice
from .event import Event
from ukz.utils import PwLinFunc

################################

class Melody:
    
  def __init__(self):
    self.time = 0
    self.voices = []
  def reset(self):
    self.time = 0
    self.voices = []
  def copy(self):
    m = Melody()
    m.voices = []
    for v in self.voices:
      m.voices.append(v.copy())
    return m

  def sortNotes(self):
    for v in self.voices:
      v.sortNotes()
  def sortGradients(self):
    for v in self.voices:
      v.sortGradients()
  def sort(self):
    self.sortNotes()
    self.sortGradients()

  def forAllNotes(self,f,*args):
    for v in self.voices:
      v.forAllNotes(f,*args)
  def forAllGradients(self,f,*args):
    for v in self.voices:
      v.forAllGradients(f,*args)
  def forAllEvents(self,f,*args):
    for v in self.voices:
      v.forAllEvents(f,*args)
  def forAllTime(self,f,*args):
    self.forAllEvents(f,*args)
    # Apply to to self.time with a hack
    e = Event(0,self.time)
    f(e,*args)
    self.time = e.t + e.d

  def getCompatibleVoiceForNote(self,note):
    if not self.voices:
      self.voices.append(Voice())
    return self.voices[0]
  def getCompatibleVoiceForGradient(self,gradient):
    for v in self.voices:
      if v.isCompatibleWithGradient(gradient):
        return v
    vv = Voice()
    self.voices.append(vv)
    return vv
  def getCompatibleVoiceForVoice(self,voice):
    for v in self.voices:
      if v.isCompatibleWithVoice(voice):
        return v
    vv = Voice()
    self.voices.append(vv)
    return vv

  def insertNote(self,note):
    v = self.getCompatibleVoiceForNote(note)
    v.insertNote(note)
  def insertGradient(self,gradient):
    v = self.getCompatibleVoiceForGradient(gradient)
    v.insertGradient(gradient)
  def insertVoice(self,voice):
    v = self.getCompatibleVoiceForVoice(voice)
    v.insertVoice(voice)
  def insertMelody(self,melody):
    for v in melody.voices:
      self.insertVoice(v)
  def appendNote(self,note):
    if isinstance(note,list):
      t = self.time
      for n in note:
        self.time = t
        self.appendNote(n)
    elif isinstance(note,int):
      n = Note(note)
      n.forward(self.time)
      self.insertNote(n)
      self.time += n.d
    elif isinstance(note,Note):
      note.forward(self.time)
      self.insertNote(note)
      self.time += note.d
    else:
      raise ValueError('unsupported argument type')
  def appendGradient(self,gradient):
    gradient.forward(self.time)
    v = self.getCompatibleVoiceForGradient(gradient)
    v.insertGradient(gradient)
  def appendVoice(self,voice):
    voice.forAllEvents(Event.forward,self.time)
    v = self.getCompatibleVoiceForVoice(voice)
    v.insertVoice(voice)
  def appendMelody(self,melody):
    newTime = self.time + melody.time
    melody.forAllEvents(Event.forward,self.time)
    self.insertMelody(melody)
    self.time = newTime
      
  def processNoteProps(self,func,*propNames):
    for v in self.voices:
      v.processNoteProps(func,*propNames)
  def processNotePropsAll(self,func,*propNames):
    for v in self.voices:
      v.processNotePropsAll(func,*propNames)
 
  def expandTo(self,time):
    factor = Fraction(time,self.time)
    self.forAllTime(Event.expand,factor)

  def repeat(self,times):
    for v in self.voices:
      v.repeat(self.time,times)
    self.time *= times
  def repeatUntil(self,time):
    for v in self.voices:
      v.repeatUntil(self.time,time)
    self.time = time
    
  def choirize(self):
    for v in self.voices:
      v.choirize()
      
  def scaleAt(self,index):
    notes = self.voices[0].notes
    pitches = map(lambda n: n.p, notes)
    scale = Scale(list(pitches))
    return scale.scaleAt(index)

  #######################

  def injectMelody(self,mel):
    stime = self.time
    ns = list(self.allNotes())
    self.reset()
    for n in ns:
      m = mel.copy()
      m.forAllNotes(Note.translateUp,n.p)
      m.forAllNotes(Note.addL,n.l-5)
      m.forAllTime(Event.expand,n.d)
      m.forAllTime(Event.forward,\
       n.t*mel.time)
      self.insertMelody(m)
    #for v in self.voices:
    #  v.injectVoice(mel.time,mel.voices[0])
    self.time = stime*mel.time

  def zipDurations(self,mel):
    for v in self.voices:
      v.zipDurations(mel.voices[0])
      
  def expand(self,fac):
    self.forAllTime(Event.expand,fac)
  def isEmpty(self):
    for v in self.voices:
      if v.notes.events:
        return False
  def startTimeForGradient(self):
    x = 0
    for v in self.voices:
      if v.notes.events:
        x = min(0,v.notes.events[0].t)
    return x
  def lastNoteTime(self):
    m = 0
    for v in self.voices:
      mm = max(map(lambda n: n.t, \
       v.notes.events))
      m = max(m,mm)
    return m
  def allNotes(self):
    for v in self.voices:
      for n in v.notes:
        yield n
  def bendWithMelody(self,\
   mel,typ,v1,v2,p1,p2):
    g = Gradient(typ,0,1)
    g.t = self.startTimeForGradient()
    if self.time!=0 or \
     not self.isEmpty():
      g.d = self.time
    else:
      g.d = mel.lastNoteTime()
    g.d -= g.t
    for n in mel.voices[0].notes:
      val = PwLinFunc.interpolate(\
       p1,p2,v1,v2,n.p)
      g.addVertex(n.t,val,n.props)
    g.normalizeVertexTimes()
    for v in self.voices:
      if not v.isCompatibleWithGradient(g):
        raise ValueError('Gradient incompatible')
      v.insertGradient(g)
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
  def durationUntilEnd(self,arg):
    m = {}
    for n in self.allNotes():
      if n.d < self.time - n.t:
        n.d = self.time - n.t
      x = m.get(n.p,None)
      if x is None:
        m[n.p] = []
      m[n.p].append(n)
    for p,ns in m.items():
      for i in range(0,len(ns)-1):
        a = ns[i]
        b = ns[i+1]
        if a.t+a.d > b.t:
          a.d = b.t-a.t
