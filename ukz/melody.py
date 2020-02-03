from fractions import Fraction
from ukz.numerize import numerize
from ukz.scale import *
from ukz.loudness import *

################################

def choirizeSinglePitch(tims):
    t1 = None
    t2 = None
    for (t,d) in tims:
        if t1 is not None:
            if t > t2:
                yield (t1,t2-t1)
                t1 = t
                t2 = t+d
            else:
                t2 = max(t2,t+d)
        else:
            t1 = t
            t2 = t+d
    if t1 is not None:
        yield (t1,t2-t1)

################################

class Note:
  
  def __init__(self,p,t=0,d=1,l=5,props={},b=0):
    self.p = p
    self.t = t
    self.d = d
    self.l = l
    self.b = b
    self.props = props.copy()

  def copy(self):
    return Note(self.p,self.t,self.d,self.l,self.props,self.b)
  def applyToCopy(self,f,*args):
    r = self.copy()
    f(r,*args)
    return r
  def __str__(self):
    return f"p{self.p} t{self.t} d{self.d} l{self.l}"
  def __repr__(self):
    return self.__str__()
  
  def __lt__(self,other):
    return self.t < other.t
    
  def alterP(self,f):
    self.p = f(self.p)
    
  def stretchBy(self,fac):
    self.t *= fac
    self.d *= fac
  def durStretchBy(self,fac):
    self.d *= fac

  def setP(self,p):
    self.p = p
  def setT(self,t):
    self.t = t
  def setD(self,d):
    self.d = d
  def setL(self,l):
    self.l = l
  def setB(self,b):
    self.b = b
  def setProps(self,props):
    self.props = props.copy()
  def setProp(self,name,val):
    self.props[name] = val
  
  def addP(self,dp):
    self.p += dp
  def addT(self,dt):
    self.t += dt
  def addD(self,dd):
    self.d += dd
  def addL(self,dl):
    self.l += dl

  def subP(self,dp):
    self.p -= dp
  def subT(self,dt):
    self.t -= dt
  def subD(self,dd):
    self.d -= dd
  def subL(self,dl):
    self.l -= dl

  def atScale1(self,sc):
    self.p = sc[self.p]

class Melody:
    
  def __init__(self,notes=[],time=0):
    self.time = time
    self.notes = list(notes)
        
  def reset(self):
    self.time = 0
    self.notes = []
        
  def copy(self):
    return Melody(map(lambda n: n.copy(),self.notes),self.time)
        
  def addNote(self,pitch,duration=1,loudness=5,props={},b=0):
    if isinstance(pitch,list):
      for p in pitch:
        self.addNote(p,duration,loudness,props,b)
      return
    t = self.time
    p = pitch
    d = numerize(duration)
    if d<=0:
      raise ValueError("duration must be strictly positive")
    ld = loudness
    self.notes.append(Note(p,t,d,ld,props,b))
        
  def checkDups(self):
    np = None
    self.notes.sort()
    for n in self.notes:
      if np is None:
        continue
      if np.p==n.p and np.t==n.t:
        raise Exception("Duplicate notes! Not cool!")
      np = n
        
  def addMelody(self,melody):
    tm = 0
    ti = self.time
    for n in melody.notes:
      self.forward(n.t-tm)
      self.addNote(n.p,n.d,n.l,n.props,n.b)
      tm = n.t
    self.time = ti
    self.checkDups()

  def forward(self,duration):
    self.time = \
     self.time + \
     numerize(duration)
  def goto(self,other):
    if isinstance(other,Melody):
      self.time = other.time
    else:
      self.time = numerize(other)
         
  def appendNote(self,pitch,duration=1,loudness=5,props={}):
    self.addNote(pitch,duration,loudness,props)
    self.time += duration
  def appendMelody(self,melody):
    self.addMelody(melody)
    self.time += melody.time
    
  def mapNotes1(self,f,fac):
    return map(lambda n: \
     Note.applyToCopy(n,f,fac), \
     self.notes)
  def mapNotesNow1(self,f,fac):
    self.notes = list(map(lambda n: \
     Note.applyToCopy(n,f,numerize(fac)), \
     self.notes))
    return self

  def setProp(self,name,val):
    for n in self.notes:
      n.setProp(name,val)
  def setProps(self,props):
    for n in self.notes:
      n.setProps(props)
  def processProps(self,func,*propNames):
    for n in sorted(self.notes):
      vs = []
      b = True
      for pn in propNames:
        v = n.props.get(pn,None)
        if v is None:
          b = False
          break
        vs.append(v)
      if b:
        func(n,*vs)
  def processPropsAll(self,func,*propNames):
    for n in sorted(self.notes):
      vs = []
      for pn in propNames:
        v = n.props.get(pn,None)
        vs.append(v)
      func(n,*vs)

  def stretched_notes(self,fac):
    return self.mapNotes1(Note.stretchBy,fac)
  def durStretched_notes(self,fac):
    return self.mapNotes1(Note.durStretchBy,fac)
  def durExtended_notes(self,extratime):
    return self.mapNotes1(Note.addD,extratime)
  def translated_notes(self,fac):
    return self.mapNotes1(Note.addP,fac)
  def louded_notes(self,loudness):
    return self.mapNotes1(Note.setL,loudness)

        
  def stretch(self,factor):
    self.mapNotesNow1(Note.stretchBy,factor)
    self.time = self.time*numerize(factor)
    return self
  def contract(self,factor):
    return self.stretch(Fraction(1,factor))
  def translateUp(self,dp):
    return self.mapNotesNow1(Note.addP,dp)
  def translateDown(self,dp):
    return self.mapNotesNow1(Note.subP,dp)
  def durExtend(self,dt):
    return self.mapNotesNow1(Note.addT,dt)

  def stretchTo(self,time):
    return self.stretch(divide(time,self.time))
  def durSet(self,factor):
    fac = numerize(factor)
    self.mapNotesNow1(Note.setD,fac)
  def durStretch(self,factor):
    fac = numerize(factor)
    self.mapNotesNow1(Note.durStretchBy,fac)
  def durContract(self,factor):
    return self.durStretch(Fraction(1,factor))
  def durShorten(self,removedTime):
    return self.durExtend(-removedTime)

  def setLoudness(self,loudness):
    ld = numerize(loudness)
    self.mapNotesNow1(Note.addL,ld-5)
  
  def bend(self,b):
    self.mapNotesNow1(Note.setB,b)
    
  def repeatedUntil_h(self,dt):
    for n in self.notes:
      yield n.applyToCopy(Note.addT,dt)
  def repeatUntil2(self,time):
    notes = []
    t = 0
    done = False
    while t < time:
      for n in self.notes:
        if n.t+t >= time:
          done = True
          break
        notes.append(n.applyToCopy(Note.addT,t))
      if done:
        break
      t = t + self.time
    self.notes = notes
    self.time = time
    return self
  def repeat(self,times):
    notes = []
    t = 0
    for _ in range(0,times):
      notes.extend(self.repeatedUntil_h(t))
      t = t + self.time
    self.notes = notes
    self.time = t
    return self
    
  def crescendo_h(self,il,fl):
    self.notes.sort()
    for n in self.notes:
      x = n.t / self.time
      y = 1-x
      ll = x*fl + y*il
      yield n.applyToCopy(Note.setL,ll)
  def crescendo(self,initialLoudness,finalLoudness):
    self.notes = list(\
    	self.crescendo_h(\
    	initialLoudness,finalLoudness))
    return self
    
  def hashNotesByPitchLoudness(self):
    m = {}
    for n in sorted(self.notes):
      ts = m.get((n.p,n.l),None)
      if ts is not None:
        ts.append((n.t,n.d))
      else:
        m[(n.p,n.l)] = [(n.t,n.d)]
    return m
  def choirizedNotes(self):
    m = self.hashNotesByPitchLoudness()
    for (pl,tims) in m.items():
      for (t,d) in choirizeSinglePitch(tims):
        yield Note(pl[0],t,d,pl[1],{})
  def choirize(self):
    self.notes = list(self.choirizedNotes())

  def backward(self,dt):
    self.time -= dt
    self.mapNotesNow1(Note.subT,dt)

    # def insertedMelody(self,mel):
    #   ret = Melody()
    #   for n in self.notes:
    #     if n.p is None:
    #       continue
    #     ret.time = n.t * mel.time
    #     m = mel.copy().translateUp(n.p)\
    #      .stretch(n.d)\
    #      .setLoudness(n.l)
    #     ret.addMelody(m)
    #   ret.time = self.time*mel.time
    #   return ret
      
  def insertMelody_h(self,mel):
   for n1 in self.notes:
       for n2 in mel.notes:
        p = n1.p + n2.p
        t = n1.t*mel.time + n2.t
        d = n1.d * n2.d
        l = n1.l + n2.l - 5
        props = n1.props.copy()
        for (k,v) in n2.props.items():
          props[k] = v
        yield Note(p,t,d,l,props)
          
  def insertMelody(self,mel):
    notes = list(self.insertMelody_h(mel))
    self.time *= mel.time
    self.notes = notes
  def insertMelodyRev(self,mel):
    mel.insertMelody(self)
      
  def atScale2(self,mel):
    sc = Scale(list(map(lambda n: n.p, mel.notes)))
    for n in self.notes:
      n.p = sc[pitchToWhiteIndex(n.p)]
  def atScale(self,mel):
    sc = Scale(list(map(lambda n: n.p, mel.notes)))
    for n in self.notes:
      n.p = sc[n.p]
    
  def adjustLoudnessForPitch(self,p,dl):
    for n in self.notes:
     if n.p == p:
       n.addL(dl)
       
  # returns array of note arrays.
  # Each note array never has more than
  # one note on at once.
  def splitVoices(self):
    num = 0
    arrs = []
    ts = []
    for n in sorted(self.notes):
      k = -1
      maxtf = -1
      dup = False
      for i in range(0,num):
        ni = arrs[i][len(arrs[i])-1]
        if n.b==ni.b and \
         n.t==ni.t and \
         n.d==ni.d:
          k = i
          dup = True
          break
        if n.t >= ts[i] and ts[i]>maxtf:
          k = i
          maxtf = ts[i]
      if k<0:
        k = num
        ts.append(0)
        arrs.append([])
        num += 1
      ts[k] = n.t+n.d
      nk = n.copy()
      if dup:
        nk.b = 0
      arrs[k].append(nk)
    return arrs
      