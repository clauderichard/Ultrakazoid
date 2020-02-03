
from ukz.melodydecoder import *

def iterateAscii(firstChar,numChars):
    fi = ord(firstChar)
    for i in range(\
    	fi, fi+numChars):
        yield chr(i)

def mkDrumDecoder():
    mr = MelodyDecoder()
    mr["s"] = 38
    mr["c"] = 52
    mr["h"] = 46
    mr["r"] = 53
    dic = mr.dic.copy()
    for (key,val) in dic.items():
        mr[key.upper()] = [36,val]
    mr["b"] = 36
    return mr
    
def getKeyboardScale():
    return "awsedftgyhujkolp123456789"
    
def mkKeyboardDecoder(capsChord=[12],smallChord=[0]):
    mr = MelodyDecoder()
    i = 0
    for c in getKeyboardScale():
        cl = map(lambda j: i+j, smallChord)
        cu = map(lambda j: i+j, capsChord)
        mr[c.lower()] = list(cl)
        mr[c.upper()] = list(cu)
        i = i+1
    return mr
def mkPianoDecoder():
    mr = MelodyDecoder()
    i = 0
    for c in "ahbcidjefkgl":
        mr[c.lower()] = i
        mr[c.upper()] = i+12
        i = i+1
    i = 0
    for c in "nvopwqxrsytz":
        mr[c.lower()] = i
        mr[c.upper()] = i+12
        i = i+1
    return mr
    
def mkAlphabeticalMelodyDecoder(smalls,bigs=[],digits=[]):
    mr = der()
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
    