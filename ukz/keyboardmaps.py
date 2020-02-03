
def decodeMap(kMap,string):
    for key in string:
        yield kMap[key]

def iterateAscii(firstChar,numChars):
    fi = ord(firstChar)
    for i in range(\
    	fi, fi+numChars):
        yield chr(i)

def mkDrumKeyboardMap():
    m = {}
    m["s"] = 38
    m["c"] = 52
    r["h"] = 46
    m["r"] = 53
    m2 = m.copy()
    for (key,val) in m2.items():
        mr[key.upper()] = [36,val]
    mr["b"] = 36
    return mr
    
def mkPianoKeyboardMap():
    m = {}
    i = 0
    for c in "awsedftgyhujkolp123456789":
        m[c.lower()] = i
        m[c.upper()] = i+12
        i = i+1
    return m
    
def mapPiano(string):
    km = mkPianoKeyboardMap()
    return list(decodeMap(km,string))
    
def mapDict(f,km):
    m = {}
    for (key,val) in km.items():
        m[key] = f(val)
    return m
    
def mkPianoChordKeyboardMap(smallChord=[0],capsChord=[12]):
    i = 0
    for c in "awsedftgyhujkolp":
        cl = translateChord(smallChord,i)
        cu = translateChord(capsChord,i)
        m[c.lower()] = cl
        m[c.upper()] = cu
        i = i+1
    return m
    
def mkAlphabeticalKeyboardMap(smalls,bigs=[],digits=[]):
    m = {}
    mr.mapPitchesAlphabetically("a",smalls)
    mr.mapPitchesAlphabetically("A",bigs)
    mr.mapPitchesAlphabetically("0",digits)
    return mr
