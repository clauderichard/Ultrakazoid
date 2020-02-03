from ukz.melody import *

# A white piano key can be represented as a string:
# c   C in octave 0
# C   C in octave 1
# C#  C# in octave 2
# E4  E in octave 4 (the caps doesn't matter when there's a number)
# f#3 F# in octave 3
# f3# F# in octave 3 (the sharp can come before or after the number)
class WhitePianoKeyRepr:
    def __init__(self,string):
        self.letterChar = ord(string[0])
        si = WhitePianoKeyRepr.findSharpIndex(string)
        (octa,octb) = WhitePianoKeyRepr.whereToParseOctave(string,si)
        self.octaveInt = 0 if octa>=octb else int(string[octa:octb])
        self.sharpValue = 1 if si else 0
    def findSharpIndex(string):
        l = len(string)
        if l <= 1:
            return False
        if string[1] == '#':
            return 1
        if string[l-1] == '#':
            return l-1
        return False
    def whereToParseOctave(string,sharpIndex):
        l = len(string)
        if sharpIndex == 1:
            return (2,l)
        if sharpIndex == l-1:
            return (1,l-1)
        if not sharpIndex:
            return (1,l)
        raise ValueError(f"sharpIndex wasn't an acceptable value! It was {sharpIndex} and len(string) was {l}")

class WhitePianoPitchDecoder:
    def __init__(self,tonicChar='c',tonicPitch=0):
        if len(tonicChar) != 1 or ord(tonicChar) < ord("a") or ord("g") < ord(tonicChar):
            raise ValueError("tonicChar must be single small letter from a to g.")
        self.pitchmap = {}
        tch = ord(tonicChar[0]) # tch = ASCII tonicChar
        sc = [0,2,3,5,7,8,10,12] # white keys a to g
        ti = ord(tonicChar) - ord("a") # index of tonic in sc
        trans = tonicPitch - sc[ti] # transposing interval
        for i in range(0,7):
            pz = sc[i] # pz = pitch if a was zero
            pt = pz + trans # pt = pitch if a is not zero
            c = ord("a")+i # c = ASCII a to g
            if c < tch:
                pt = pt + 12 # move pt by an octave
            self.pitchmap[c] = pt
            self.pitchmap[c + ord("A") - ord("a")] = pt+12
    def __getitem__(self,char):
        if isinstance(char,str):
            return self.pitchmap[ord(char)]
        elif isinstance(char,int):
            return self.pitchmap[char]
            
class PianoPitchDecoder:
    
    instance = None

    def __init__(self):
        self.whitePitchDecoder = WhitePianoPitchDecoder('c',0)
        
    def getSingleton():
        if PianoPitchDecoder.instance is None:
            PianoPitchDecoder.instance = PianoPitchDecoder()
        return PianoPitchDecoder.instance

    def getWhiteSharpPair(arg):
        es = "a valid representation of a piano key (e.g. \"C\" or \"D#\")"
        if isinstance(arg,str):
            if len(arg) > 2:
                raise ValueError(f"arg is too long to be {es}")
            if len(arg) == 0:
                raise ValueError(f"arg must not be empty! Must be {es}")
            c = ord(arg[0])
            if (c < ord("a") and c < ord("A")) or (c > ord("g") and c > ord("G")):
                raise ValueError(f"arg's first character must be a letter from a to g")
            if len(arg) == 1:
                return (c,0)
            if len(arg) == 2:
                if arg[1] != '#':
                    raise ValueError(f"arg's 2nd character (if it has a 2nd) must be '#'")
                return (c,1)
        else:
            raise ValueError(f"arg must be {es}")
            
    def __getitem__(self,string):
        r = WhitePianoKeyRepr(string)
        iscaps = r.letterChar >= ord('A') and r.letterChar <= ord('G')
        letter = r.letterChar + \
         ord('a') - ord('A') \
         if iscaps else r.letterChar 
        # if iscaps then we'll end up adding it again later
        capsBoost = 12 if r.octaveInt == 0 and iscaps else 0
        octaveBoost = 12 * r.octaveInt
        return self.whitePitchDecoder[letter] + r.sharpValue + octaveBoost + capsBoost
        