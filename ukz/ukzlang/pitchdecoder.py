from ukz.songconfig import DrumPitchUkz
    
class PitchDecoder:

    pitchmap = { }

    @classmethod
    def init(cls):
        cls.pitchmap = {
            "c": 0,
            "d": 2,
            "e": 4,
            "f": 5,
            "g": 7,
            "a": 9,
            "b": 11,
            "s": DrumPitchUkz.snare,
            "h": DrumPitchUkz.hiHatClosed,
            "r": DrumPitchUkz.rideCymbal1,
            "l": DrumPitchUkz.rideBell,
            "t": DrumPitchUkz.tom1,
            "u": DrumPitchUkz.tom3,
            "m": DrumPitchUkz.metronomeClosed,
            "j": DrumPitchUkz.jingleBell,
        }
        for c,v in list(cls.pitchmap.items()):
            cls.pitchmap[c.upper()] = v + 12
        # cls.pitchmap['^'] = 1
        # cls.pitchmap['v'] = -1
        for i in "0123456789":
            cls.pitchmap[i] = 12 * (ord(i)-ord("0"))

    @classmethod
    def decode(cls,code):
        p = 0
        transposingUp = False
        transposingDown = False
        directPitching = False
        p = 0
        for c in code:
            if c=="p":
                p = 0
                directPitching = True
            elif c=="^":
                p += 1
                transposingUp = True
                transposingDown = False
            elif c=="v":
                p -= 1
                transposingUp = False
                transposingDown = True
            elif directPitching:
                try:
                    dp = cls.pitchmap[c]
                    if dp==1 or dp==-1:
                        raise ValueError(f"Char '{c}' not valid here")
                    p = p*10 + dp//12
                except KeyError:
                    raise ValueError(f"Char '{c}' not valid here")
            else:
                try:
                    dp = cls.pitchmap[c]
                    if transposingUp:
                        # dp is semitones in octave shift, 
                        # but want that to be num of semitones.
                        # already transposed ^ or v so apply -1
                        p += dp//12 - 1
                    elif transposingDown:
                        p -= dp//12 - 1
                    else:
                        p += dp
                except KeyError:
                    raise ValueError(f"Char '{c}' not valid here")
        if directPitching:
            return p + 10000
        return p

