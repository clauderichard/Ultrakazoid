
from ukz.melody import *

#class MelodyReader:

    def __init__(self):
        self.pitchMap = {}
    def mapPitch(self,ch,pitch):
        self.pitchMap[ch] = pitch
    
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
    
    def readToMelody(self,strings,melody,mustMove=True):
        strs = [strings] if isinstance(strings,str) else strings
        origtime = melody.curTime
        for s in strs:
            melody.curTime = origtime
            for (c,dur) in patternToSpaceLength(s):
                p = self.pitchMap.get(c,-1)
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
        if not mustMove:
            melody.curTime = origtime

    def mkMelody(self,string):
        mel = Melody()
        self.readToMelody(string,mel,True)
        return mel
        
    def read(self,string):
        return self.mkMelody(string)
        
    #def readWithRhythm(self,rhythm,strings):
        
        
    def mapPitchesAlphabetically(self,firstChar,values):
        i = ord(firstChar)
        for val in values:
            key = chr(i)
            self.mapPitch(key,val)
            i = i + 1
        
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
    
def mkDrumMelodyReader():
    mr = MelodyReader()
    mr.mapPitch("b",36)
    mr.mapPitch("s",38)
    mr.mapPitch("S",[36,38])
    mr.mapPitch("c",52)
    mr.mapPitch("C",[36,52])
    mr.mapPitch("h",46)
    mr.mapPitch("H",[36,46])
    #dic = mr.pitchMap.copy()
    #for (key,val) in dic:
        #mr.mapPitch(key.upper(),[36,val])
    return mr
    
def getKeyboardScale():
    return "awsedftgyhujkolp"
    
def mkKeyboardMelodyReader(capsChord=[12],smallChord=[0]):
    mr = MelodyReader()
    i = 0
    for c in getKeyboardScale():
        cl = map(lambda j: i+j, smallChord)
        cu = map(lambda j: i+j, capsChord)
        mr.mapPitch(c.lower(), list(cl))
        mr.mapPitch(c.upper(), list(cu))
        i = i+1
    return mr
    
def mkAlphabeticalMelodyReader(smalls,bigs=[],digits=[]):
    mr = MelodyReader()
    mr.mapPitchesAlphabetically("a",smalls)
    mr.mapPitchesAlphabetically("A",bigs)
    mr.mapPitchesAlphabetically("0",digits)
    return mr
def mkScaleMelodyReader(scale,capsChord=[0]):
    smallA = ord("a")
    bigA = ord("A")
    mr = MelodyReader()
    for i in range(0,7):
        smallKey = chr(smallA + i)
        bigKey = chr(bigA + i)
        mr.mapPitch(smallKey,scale[i])
        chord = []
        for cc in capsChord:
            chord.append(scale[cc])
        mr.mapPitch(bigKey,chord)
    return mr
def mkMinorMelodyReader(capsChord=[0]):
    scale = [0,2,3,5,7,8,10,12,14,15,17,19,20,22,24]
    return mkScaleMelodyReader(scale,capsChord)
def mkMajorMelodyReader(capsChord=[0]):
    scale = [0,2,4,5,7,9,11,12,14,16,17,19,21,23,24]
    return mkScaleMelodyReader(scale,capsChord)
    