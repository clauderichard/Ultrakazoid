from ukz.melody import *

# A piano key can be represented as a string:
# c   C in octave 0
# C   C in octave 1
# C#  C# in octave 2
# E4  E in octave 4 (the caps doesn't matter when there's a number)
# f#3 F# in octave 3
# f3# F# in octave 3 (the sharp can come before or after the number)
# f10# Actually you shouldn't use this. It will interpret 10 as 1+0 basically.
#   You shouldn't have pitches that go all the way to c10, that's insane
#   (although it can technically be within the MIDI range, but barely)

class PianoPitchDecoder:

    instance = None

    def __init__(self):
        self.pitchmap = {
            "c": 0, "C": 12,
            "d": 2, "D": 14,
            "e": 4, "E": 16,
            "f": 5, "F": 17,
            "g": 7, "G": 19,
            "a": 9, "A": 21,
            "b": 11, "B": 23,
            "#": 1
        }
        for i in range(1,10):
            self.pitchmap[f"{i}"] = 12*i
    
    @classmethod
    def getSingleton(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __getitem__(self,code):
        ret = 0
        cap = ord("A") <= ord(code[0]) and ord(code[0]) <= ord("G")
        for c in code:
            p = self.pitchmap.get(c,None)
            if p is None:
                raise ValueError(f"Char '{c}' is not supported in non-drum notes")
            ret += p
            if ord("0") <= ord(c) and ord(c) <= ord("9") and cap:
                ret -= 12
        return ret
        