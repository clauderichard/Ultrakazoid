
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
        
    def getSingleton():
        if DrumPitchDecoder.instance is None:
            DrumPitchDecoder.instance = DrumPitchDecoder()
        return DrumPitchDecoder.instance
        
    def mapchar(self,string,pitch):
        self.pitchmap[string] = pitch
        
    def __getitem__(self,string):
        #if len(string) != 1:
        #    raise ValueError("drum pitches can't have modifiers, you can only capitalize them")
        c = ord(string[0])
        iscaps = c >= ord('A') and c <= ord('Z')
        #letter = c + ord('a') - ord('A') if iscaps else c 
        s = string.lower()
        # if iscaps then we'll add the exrra pitch.
        p = self.pitchmap[s]
        return [p,DrumPitchDecoder.capsExtraPitch] if iscaps else [p]
        