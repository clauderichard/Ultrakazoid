
class DrumPitchDecoder:
    capsExtraPitch = 36
    
    instance = None

    def __init__(self):
        self.pitchmap = {}
        
        self.mapchar("b",36)
        self.mapchar("s",38)
        self.mapchar("h",42)
        self.mapchar("h#",44)
        self.mapchar("h°",46)
        self.mapchar("c",49)
        self.mapchar("c#",57)
        self.mapchar("r",59)
        self.mapchar("r#",51)
        self.mapchar("g",52)
        self.mapchar("g#",55)
        self.mapchar("l",53)
        self.mapchar("l#",56)
        
        self.mapchar("f1",41)
        self.mapchar("f2",43)
        self.mapchar("t1",45)
        self.mapchar("t2",47)
        self.mapchar("t3",48)
        self.mapchar("t4",50)
        
        self.mapchar("m",33)
        self.mapchar("m°",34)
        
    @classmethod
    def getSingleton(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance
        
    def mapchar(self,string,pitch):
        self.pitchmap[string] = pitch
        
    # Returns an array of pitch numbers, because
    # there might be an extra bass pedal with it.
    def __getitem__(self,string):
        c = ord(string[0])
        iscaps = c >= ord('A') and c <= ord('Z')
        s = string.lower()
        # if iscaps then we'll add the extra pitch.
        p = self.pitchmap[s]
        return [p,DrumPitchDecoder.capsExtraPitch] if iscaps else [p]
        