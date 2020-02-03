
from ukz.scheme import *

class Scale:
    def __init__(self,chord):
        self.chord = chord
    def __getitem__(self,index):
        cd = value(self.chord)
        l = len(cd)
        o = index//l
        i = index%l
        return cd[i] + o*12
    def translate(self,interval):
        return Scale(translateChord(\
        	self.chord))

def bindPitch(pitch,minPitch,maxPitch):
    p = pitch
    while p < minPitch:
        p = p + 12
    while p > maxPitch:
        p = p - 12
    return p

def bindChord(chord,minPitch,maxPitch):
    return list(map(lambda p:\
    	bindPitch(p,minPitch,maxPitch),\
    	chord))
    	
def translatePitch(pitch,interval):
    return 	pitch+interval

def translateChord(chord,interval):
    return list(map(lambda p:\
    	translatePitch(p,interval),\
    	chord))
