
from ukz.melody import *
from ukz.decoder import *

class MelodyDecoder(Decoder):

    def __init__(self):
        Decoder.__init__(self)
    
    def extractPitches(self,p):
        if isinstance(p,list):
            return p
        elif isinstance(p,tuple):
            return self.extractPitches(p[0])
        else:
            return [p]
    def extractDuration(self,p):
        if isinstance(p,list):
            return 1
        elif isinstance(p,tuple):
            return p[1]
        else:
            return 1
            
    def decode(self,keys):
        melody = Melody()
        for (c,dur) in patternToSpaceLength(keys):
            p = self.dic.get(c,-1)
            if p==-1 or not c:
                melody.forward(dur)
            else:
                d = self.extractDuration(p)
                ps = self.extractPitches(p)
                if d <= 0:
                    d = dur + d
                for pp in ps:
                    melody.addNote(pp,d,False)
                melody.forward(dur)
        return melody
        
def patternToSpaceLength(string):
    ret = []
    cur = None
    dur = 0
    for s in string:
        if s == " ":
            dur = dur + 1
        else:
            if dur>0:
                ret.append((cur,dur))
            cur = s
            dur = 1
    if dur>0:
        ret.append((cur,dur))
    return ret
