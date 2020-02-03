
class Melody:
    
    def __init__(self):
        self.curTime = 0
        self.notes = []
        self.curFlag = 0
        
    def addNote(self,pitch,duration,mustMove=True):
        ps = [pitch]
        if isinstance(pitch,list):
            ps = pitch
        for p in ps:
            note = (self.curTime,p,duration)
            self.notes.append(note)
        if mustMove:
            self.curTime = self.curTime + duration
    
    def play(self,pitch,duration,mustMove=True):
        return self.addNote(pitch,duration,mustMove)
    
    def forward(self,duration):
        self.curTime = self.curTime + duration
    def timeFlag(self):
        self.curFlag = self.curTime
    def goToFlag(self):
        self.curTime = self.curFlag

def zipRhythm(rhythm,s):
    ret = ""
    l1 = len(rhythm)
    l2 = len(s)
    for i in range(0,min(l1,l2)):
        r = rhythm[i]
        c = s[i]
        x = c + " "*(r-1)
        ret = ret + x
    return ret
    
def mix(m1,m2):
    ret = Melody()
    ret.notes = m1.notes + m2.notes
    return ret
    
