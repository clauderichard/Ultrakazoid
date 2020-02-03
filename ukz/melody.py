from fractions import *
from ukz.numerize import *
from ukz.scale import *
from ukz.loudness import *

################################

def chordize(obj):
    if isinstance(obj,int):
        return [obj]
    elif isinstance(obj,list):
        return obj
    raise ValueError(\
    	f"Can only chordize int or list. obj was {obj}")

def legatoTimes(tims):
    t1 = -99
    t2 = -99
    for (t,d) in tims:
        if t1!=(-99):
            if t > t2:
                yield (t1,t2-t1)
                t1 = t
                t2 = t+d
            else:
                t2 = max(t2,t+d)
        else:
            t1 = t
            t2 = t+d
    if t1 != (-99):
        yield (t1,t2-t1)

################################



class Melody:
    
    def __init__(self,\
    	notes=[],time=0,loudness=mezzoforte):
        self.curTime = time
        self.curLoudness = loudness
        self.notes = list(notes)
        
    def copy(self):
        return Melody(self.notes,self.curTime,self.curLoudness)
        
    def addNote(self,pitch,duration=1,loudness=None):
        t = self.curTime
        p = pitch
        d = numerize(duration)
        if d<=0:
            raise ValueError("duration must be strictly positive")
        ld = self.curLoudness \
         if loudness is None \
         else self.curLoudness \
         if loudness<0 \
         else loudness
        self.notes.append((t,p,d,ld))
        
    def addChord(self,chord,duration=1,loudness=-1):
        for p in chord:
            self.addNote(p,duration,loudness)

    def addMelody(self,melody):
        tm = 0
        ti = self.curTime
        for (t,p,d,l) in melody.notes:
            self.forward(t-tm)
            self.addNote(p,d,l)
            tm = t
        self.curTime = ti

    def forward(self,duration):
        self.curTime = \
         self.curTime + \
         numerize(duration)
    def goto(self,other):
        if isinstance(other,Melody):
            self.curTime = other.curTime
        else:
            self.curTime = numerize(other)
         
    def playNote(self,pitch,duration=1,loudness=None,moveBy=None):
        self.addNote(pitch,duration,loudness)
        dt = duration if moveBy is None else moveBy
        self.forward(dt)
    def playChord(self,chord,duration=1,loudness=-1,moveBy=None):
        self.addChord(chord,duration,loudness)
        dt = duration if moveBy is None else moveBy
        self.forward(dt)
    def playMelody(self,melody,moveBy=None):
        self.addMelody(melody)
        dt = melody.curTime if moveBy is None else moveBy
        self.forward(dt)
    
    def stretched_notes(self,fac):
        return map(lambda n:\
         (n[0]*fac,\
         n[1],n[2]*fac,n[3]), \
       	  self.notes)
    def stretched(self,factor):
        fac = numerize(factor)
        notes = self.stretched_notes(fac)
        tim = self.curTime*fac
        ld = self.curLoudness
        return Melody(notes,tim,ld)
    def stretch(self,factor):
        fac = numerize(factor)
        self.notes = list(self.stretched_notes(fac))
        self.curTime = self.curTime*fac
        return self
    def stretchedTo(self,time):
        return self.stretched(divide(time,self.curTime))
    def stretchTo(self,time):
        return self.stretch(divide(time,self.curTime))
    def stretchByAddition(self,time):
        return self.stretch(divide(self.curTime+time,self.curTime))
    
    
    def translated(self,interval):
        i = interval
        notes = map(lambda n:\
         (n[0],\
         n[1]+i,n[2],n[3]), \
       	  self.notes)
        tim = self.curTime
        ld = self.curLoudness
        return Melody(notes,tim,ld)
    def translate(self,interval):
        i = interval
        self.notes = list(map(lambda n:\
         (n[0],\
         n[1]+i,n[2],n[3]), \
       	  self.notes))
        return self
         
    def repeatedUntil_h(self,dt):
        for (t,p,d,l) in self.notes:
            yield (t+dt,p,d,l)
    def repeatedUntil(self,time):
        notes = []
        t = 0
        while t < time:
            notes.extend(repeatedUntil_h(self,t))
            t = t + self.curTime
        return Melody(notes,\
         t,self.curLoudness)
    def repeated(self,times):
        notes = []
        t = 0
        for i in range(0,times):
            notes.extend(self.repeatedUntil_h(t))
            t = t + self.curTime
        return Melody(notes,\
         t,self.curLoudness)
    def repeat(self,times):
        notes = []
        t = 0
        for i in range(0,times):
            notes.extend(self.repeatedUntil_h(t))
            t = t + self.curTime
        self.notes = notes
        self.curTime = t
        return self
    
    def crescendo_h(self,il,fl):
        self.notes.sort()
        for (t,p,d,l) in self.notes:
            x = t / self.curTime
            y = 1-x
            ll = x*b + y*a
            yield (p,t,d,ll)
    def crescendo(self,initialLoudness,finalLoudness):
        a = initialLoudness
        b = finalLoudness
        self.notes = list(\
        	self.crescendo_h(\
        	initialLoudness,finalLoudness))
        return self
    def crescendoed(self,initialLoudness,finalLoudness):
        a = initialLoudness
        b = finalLoudness
        notes = self.crescendo_h(initialLoudness,finalLoudness)
        return Melody(notes,self.curTime,self.curLoudness)
    
    
    def shredize_h(self,dur):
        for (t,p,d,l) in self.notes:
            tt = 0
            while tt<t:
                nextt = min(tt+dur,t)
                yield (tt,p,nextt-tt,l)
                tt = nextt
    def shredized(self,duration):
        return Melody(\
        	self.shredize_h(duration),\
        	self.curTime,self.curLoudness)

    def rhythmized(self,durs):
        notes = []
        t = 0
        for (n,r) in zip(self.notes,durs):
            notes.append((t,n[1],r,n[3]))
            t = t+r
        return Melody(notes,t,self.curLoudness)
    
    def hashNotesByPitchLoudness(self):
        m = {}
        for (t,p,d,l) in sorted(self.notes):
            ts = m.get((p,l),None)
            if ts is not None:
                ts.append((t,d))
            else:
                m[(p,l)] = [(t,d)]
        return m
    def choirizedNotes(self):
        m = self.hashNotesByPitchLoudness()
        for (pl,tims) in m.items():
            for (t,d) in legatoTimes(tims):
                yield (t,pl[0],d,pl[1])
    def choirize(self):
        self.notes = list(self.choirizedNotes())
    def choirized(self):
        notes = list(choirizeNotes(self.notes))
        return Melody(notes,self.curTime,self.curLoudness)

    def louded_notes(self,loudness):
        for n in self.notes:
            yield (n[0],n[1],n[2],loudness)
    def louded(self,loudness):
        ns = self.louded_notes(loudness)
        return Melody(ns,self.curTime,self.curLoudness)

    def __or__(self,other):
        m = self.copy()
        m.playMelody(other)
        return m
    def __and__(self,other):
        ret = Melody()
        ret.notes = self.notes + other.notes
        ret.curTime = max(self.curTime, other.curTime)
        return ret
    def __rshift__(self,dt):
        ret = Melody()
        for (t,p,d,l) in self.notes:
            ret.notes.append((t+dt,p,d,l))
        return ret
    def __lshift__(self,dt):
        return self.__rshift__(-dt)

def shred(pitches,duration=1,loudness=mezzoforte):
    notes = []
    i = 0
    for p in pitches:
        #if p is not None:
        note = (i,p,duration,loudness)
        notes.append(note)
        i = i+1
    return Melody(notes,i,loudness)
    
def rhythmic(noteLengthPairs):
    notes = []
    t = 0
    for (n,l) in noteLengthPairs:
        # todo add duration optional
        d = l
        df = l
        if isinstance(d,tuple):
            (d,df) = d
        for p in chordize(n):
            notes.append((t,p,numerize(d),-1))
        t = t + numerize(df)
    return Melody(notes,t)
    
def mix(m1,m2):
    ret = Melody()
    ret.notes = m1.notes + m2.notes
    return ret
    
