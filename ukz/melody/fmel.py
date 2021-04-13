from ukz.util import mkFraction,linearInterpolate
from .scale import Scale
from .note import Note
from .gradient import Gradient,Bend
from ukz.util import PwLinFunc
from .chordswalker import ChordsWalker
from ukz.midi.config import MidiConfig

class Fmel:

    def __init__(self):
        self.d = 0
        self.notes = []
        self.gradients = []
    
    def forward(self,dt):
        for e in self.notes:
            e.t += dt
        for e in self.gradients:
            e.t += dt
        return self
    def backward(self,dt):
        for e in self.notes:
            e.t -= dt
        for e in self.gradients:
            e.t -= dt
        return self
    def backwardLeaveT(self,dt):
        for e in self.notes:
            e.t -= dt
        for e in self.gradients:
            e.t -= dt
        self.d -= dt
        return self
    def backwardByEnd(self):
        return self.backwardLeaveT(self.d)


    def expand(self,fac):
        for e in self.notes:
            e.t *= fac
            e.d *= fac
        for e in self.gradients:
            e.t *= fac
            e.d *= fac
        self.d *= fac
        return self
    def contract(self,fac):
        if fac==0:
            raise ValueError('Cannot contract by a factor of zero.')
        for e in self.notes:
            e.t //= fac
            e.d //= fac
        for e in self.gradients:
            e.t //= fac
            e.d //= fac
        self.d //= fac
        return self
    def expandTo(self,duration):
        n = MidiConfig.tpb*duration
        d = self.d
        for e in self.notes:
            e.t = (e.t*n)//d
            e.d = (e.d*n)//d
        for e in self.gradients:
            e.t = (e.t*n)//d
            e.d = (e.d*n)//d
        self.d = (self.d*n)//d
        return self

    def repeat(self,times):
        timestep = self.d
        newNotes = []
        newGradients = []
        oldNotes = self.notes
        oldGradients = self.gradients
        oldNotes.sort()
        oldGradients.sort()
        t = 0
        for _ in range(0,times):
            for oldNote in oldNotes:
                newNotes.append(oldNote.copyForwarded(t))
            for oldGradient in oldGradients:
                newGradients.append(oldGradient.copyForwarded(t))
            t += timestep
        self.notes = newNotes
        self.gradients = newGradients
        self.d = timestep*times
        return self

    def repeatUntil(self,endTime):
        endTimeT = endTime*MidiConfig.tpb
        timestep = self.d
        if timestep == 0:
            raise ValueError('cannot repeat a use repeatUntil for a zero-end-time Fmel')

        # build newEvs array
        newNotes = []
        newGradients = []
        t = 0
        done = False
        oldNotes = self.notes
        oldGradients = self.gradients
        oldNotes.sort()
        oldGradients.sort()
        while t < endTimeT:
            for oldNote in oldNotes:
                newNote = oldNote.copyForwarded(t)
                if newNote.t >= endTimeT:
                    done = True
                    break
                newNotes.append(newNote)
            for oldGradient in oldGradients:
                newGradient = oldGradient.copyForwarded(t)
                if newGradient.t >= endTimeT:
                    done = True
                    break
                newGradients.append(newGradient)
            if done:
                break
            t += timestep
        # replace self events with newEvs
        self.notes = newNotes
        self.gradients = newGradients
        # set new time bounds
        self.d = endTimeT
        return self

    def __eq__(self,other):
        return isinstance(other,Fmel) \
          and abs(self.d - other.d) < 0.00001 \
          and self.notes == other.notes \
          and self.gradients == other.gradients
        
    def applyOp(self,f,*a):
        f(self,*a)

    def setNoteDurs(self,d):
        # tuple for fraction
        d = MidiConfig.tpb*d
        for n in self.notes:
            n.d = d
        return self
    
    def sortNotes(self):
        self.notes.sort()
    def sort(self):
        self.sortNotes()
        self.gradients.sort()
        
    def insertMelody(self,melody):
        self.notes.extend(melody.notes)
        self.gradients.extend(melody.gradients)

    def appendMelody(self,melody):
        shiftTime = self.d
        for newNote in melody.notes:
            newNote.t += shiftTime
            self.notes.append(newNote)
        for newGrad in melody.gradients:
            newGrad.t += shiftTime
            self.gradients.append(newGrad)
        self.d += melody.d

    def lastNoteStartTime(self):
        mm = max(map(lambda n: n.t, self.notes))
        return max(0,mm)
    def __firstNoteStartTime(self):
        mm = min(map(lambda n: n.t, self.notes))
        return min(0,mm)

    def durToEnd(self):
        et = self.d
        for n in self.notes:
            n.d = max(n.d, et - n.t)

    def durTo(self,et,setLag=False):
        et = et*MidiConfig.tpb
        for n in self.notes:
            n.d = et - n.t
        if setLag:
            self.d = et
        return self

    def injectMelody(self,mel):
        met = mel.d
        tpb = MidiConfig.tpb
        newNotes = []
        newGradients = []

        for lnote in self.notes:
            for rnote in mel.notes:
                newnote = Note(lnote.p+rnote.p,
                  (lnote.t*met + lnote.d*rnote.t)//tpb,
                  (lnote.d*rnote.d)//tpb,
                  lnote.l+rnote.l,
                  lnote.c if rnote.c is None else rnote.c)
                newNotes.append(newnote)
            for rgrad in mel.gradients:
                newgrad = Gradient(rgrad.typ,
                  (lnote.t*met + lnote.d*rgrad.t)//tpb,
                  (lnote.d*rgrad.d)//tpb,
                  rgrad.bend,
                  rgrad.c)
                newGradients.append(newgrad)

        for lgrad in self.gradients:
            newgrad = Gradient(lgrad.typ,
              (lgrad.t*met) // tpb,
              (lgrad.d*met) // tpb,
              lgrad.bend,
              lgrad.c)
            newGradients.append(newgrad)

        self.d = (self.d * met) // tpb
        self.notes = newNotes
        self.gradients = newGradients

        return self

    def filterNotes(self,f):
        self.notes = list(filter(f, self.notes))
        return self

    def sharp(self):
        for n in self.notes:
            n.p += 1
        return self

    def flat(self):
        for n in self.notes:
            n.p -= 1
        return self

    def octavesUp(self,o):
        dp = o*12
        for n in self.notes:
            n.p += dp
        return self

    def transposeUp(self,dp):
        for n in self.notes:
            n.p += dp
        return self

    def transposeDown(self,dp):
        for n in self.notes:
            n.p -= dp
        return self

    def addLoudness(self,l):
        for n in self.notes:
            n.l = n.l + l
        return self

    def mapToBend(self,minPitch,maxPitch):
        v1 = 0
        v2 = 127
        et = self.lastNoteStartTime()
        vs = []
        if et==0:
            for n in self.notes:
                val = linearInterpolate(minPitch,maxPitch,v1,v2,n.p)
                vs.append((0,val))
        else:
            for n in self.notes:
                val = linearInterpolate(minPitch,maxPitch,v1,v2,n.p)
                vs.append((n.t,val))
        return Bend(et,vs)

    def mapToEqualBend(self,minPitch,maxPitch):
        v1 = 0
        v2 = 127
        st = 0
        et = self.lastNoteStartTime()
        vs = []
        if et==0:
            for n in self.notes:
                val = linearInterpolate(\
                minPitch,maxPitch,v1,v2,n.p)
                vs.append((0,val))
        else:
            for n in self.notes:
                val = linearInterpolate(\
                minPitch,maxPitch,v1,v2,n.p)
                vs.append((n.t,val))
        return Bend(et,vs)

    def mapToCyclicBend(self,minPitch,maxPitch,resultD):
        v1 = 0
        v2 = 127
        st = min(0,self.__firstNoteStartTime())
        vs = []
        prevT = st
        prevP = None
        leadupNotes = []
        cyclNotes = []
        for n in self.notes:
            if n.t >= 0:
                cyclNotes.append(n)
            else:
                leadupNotes.append(n)
        for n in leadupNotes:
            vt = n.t - st
            val = linearInterpolate(minPitch,maxPitch,v1,v2,n.p)
            prevT = n.t - st
            prevP = n.p
            vs.append((vt,val))
        ti = 0
        while True:
            b = False
            for n in cyclNotes:
                if n.t + ti - st > resultD:
                    if prevT < resultD:
                        # must insert extra point at the end
                        endPitch = linearInterpolate(prevT,n.t+ti,prevP,n.p,resultD)
                        val = linearInterpolate(minPitch,maxPitch,v1,v2,endPitch)
                        vs.append((resultD,val))
                    b = True
                    break
                vt = n.t + ti - st
                val = linearInterpolate(minPitch,maxPitch,v1,v2,n.p)
                prevT = n.t + ti - st
                prevP = n.p
                vs.append((vt,val))
            if b:
                break
            ti += self.d
        return Bend(resultD,vs)

    def applyWholeBendFromMelody(self,ctrl,minPitch,maxPitch,mel):
        bend = mel.mapToBend(minPitch,maxPitch)
        g = Gradient(ctrl,0,self.d,bend)
        self.gradients.append(g)
        return self
        
    def applyEqualBendFromMelody(self,ctrl,minPitch,maxPitch,mel):
        bend = mel.mapToEqualBend(minPitch,maxPitch)
        g = Gradient(ctrl,0,mel.lastNoteStartTime(),bend)
        self.gradients.append(g)
        return self
        
    def applyCyclicBendFromMelody(self,ctrl,minPitch,maxPitch,mel):
        bend = mel.mapToCyclicBend(minPitch,maxPitch,self.d)
        g = Gradient(ctrl,0,self.d,bend)
        self.gradients.append(g)
        return self

    # def filterToScale(self,mel):
    #     ps = set()
    #     for n in mel.notes:
    #         ps.add(n.p % 12)
    #     self.notes = list(filter(lambda n: n.p%12 in ps, self.notes))
    #     TODO: reduce start times of notes appropriately
        
    def parallelMapIntoScales(self,mel):
        self.repeatUntil(mel.d // MidiConfig.tpb)
        self.sortNotes()
        w = ChordsWalker(mel.notes)
        for n in self.notes:
            w.go(n.t)
            n.p = Scale(sorted(w.ns))[n.p]

    def setIForNones(self,c):
        for n in self.notes:
            if n.c is None:
                n.c = c
        for g in self.gradients:
            if g.c is None:
                g.c = c
    