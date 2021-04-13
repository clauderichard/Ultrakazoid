from ukz.melody import Fmel,Note
from ukz.midi.config import MidiConfig

################################

class Hmel:
    
    def __init__(self):
        self.ops = []
        self.c = None
    
################################
# Abstract methods

    def getDescendants(self,d):
        raise Exception("not implemented")
    
    def flatten(self):
        raise Exception("not implemented")

################################
    
    def applyOp(self,f,*a):
        self.ops.append((f,a))
    
################################

class HmelNode(Hmel):

    def __init__(self,precs,cs,postcs):
        Hmel.__init__(self)
        self.precs = list(precs)
        self.cs = list(cs)
        self.postcs = list(postcs)
    
    def flattenStep1(self):
        raise Exception("not implemented")

    def flatten(self):
        m = self.flattenStep1()
        for o,args in self.ops:
            o(m,*args)
        if self.c is not None:
            m.setIForNones(self.c)
        return m

    def getDescendants(self,d):
        if d==0:
            yield self
        else:
            for c in self.cs:
                for x in c.getDescendants(d-1):
                    yield x

class HmelSeq(HmelNode):

    def __init__(self,precs,cs,postcs):
        HmelNode.__init__(self,precs,cs,postcs)
        
    def flattenStep1(self):
        mel = Fmel()
        for c in self.precs:
            fc = c.flatten()
            mel.appendMelody(fc)
        mel.backwardByEnd()
        for c in self.cs:
            fc = c.flatten()
            mel.appendMelody(fc)
        t = mel.d
        for c in self.postcs:
            fc = c.flatten()
            mel.appendMelody(fc)
        mel.d = t
        return mel


class HmelPar(HmelNode):

    def __init__(self,precs,cs,postcs):
        HmelNode.__init__(self,precs,cs,postcs)

    def flattenStep1(self):
        mel = Fmel()
        for c in self.precs:
            fc = c.flatten()
            fc.backwardByEnd()
            mel.insertMelody(fc)
        for c in self.cs:
            fc = c.flatten()
            mel.insertMelody(fc)
            mel.d = fc.d
        for c in self.postcs:
            fc = c.flatten()
            mel.insertMelody(fc)
        return mel
    
# ################################

class HmelNote(Hmel):
        
    def __init__(self,p,d):
        Hmel.__init__(self)
        self.p = p
        self.d = d

    def getDescendants(self,d):
        yield self

    def flatten(self):
        mel = Fmel()
        mel.notes.append(Note(self.p,0,self.d,0,self.c))
        mel.d = self.d
        for o,args in self.ops:
            o(mel,*args)
        return mel

################################

class HmelRest(Hmel):
        
    def __init__(self,d):
        Hmel.__init__(self)
        self.d = d

    def getDescendants(self,d):
        yield self

    def flatten(self):
        mel = Fmel()
        mel.d = self.d
        for o,args in self.ops:
            o(mel,*args)
        return mel

################################

def mkHmelSeq(precs,cs,postcs):
    return HmelSeq(precs,cs,postcs)
def mkHmelPar(precs,cs,postcs):
    return HmelPar(precs,cs,postcs)
def mkHmelNote(p):
    return HmelNote(p,MidiConfig.tpb)
def mkHmelRest():
    return HmelRest(MidiConfig.tpb)

################################
