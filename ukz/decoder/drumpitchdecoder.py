
class DrumPitchDecoder:
    def __init__(self,capsExtraPitch=36):
        self.capsExtraPitch = capsExtraPitch
        self.pitchmap = {}
        # B 36 bass drum
        # S 38 snare
        # R 53 ride bell
        
        # T 2 floor toms, 4 toms
        # H 3 high hats
        # CGR 6 cymbals
        #  (2 ride 1 splash)
        #  (2 crash 1 chinese)
        
        # T4 hi tom
        # T3 himid tom
        # T2 lomid tom
        # T1 lo tom
        # f#,f2 hi floor tom
        # f,f1 lo floor tom
        # h hihat closed
        # h# hihat pedal
        # ho hihat open
        # g chinese cymbal
        # g# splash cymbal
        # C,C# crash cymbals
        # r ride bell
        # R,R# ride cymbals
        
        # m metronome click
        # M metronome bell
        
        # stuff i don't care about:
        # K 37 side stick
        # P 39 hand clap
        # G 54 tambourine
        # V 56 cowbell
        # some other bass stuff
        # treble:
        # A triangles
        # other treble but who cares
        self.mapchar("b",36)
        self.mapchar("s",38)
        self.mapchar("S",[38,36])
        #self.mapchar("r1",38)
        #self.mapchar("r2",38)
        self.mapchar("h",46)
        self.mapchar("c",49)
        self.mapchar("g",42)
        self.mapchar("p",44)
        self.mapchar("c",52)
        # "r# g##"
        self.mapchar("a",51)
        #self.mapchar("b",59)
        #self.mapchar("c",55)
        self.mapchar("d",42)
        self.mapchar("e",44)
        self.mapchar("f",46)
    def mapchar(self,string,pitch):
        self.pitchmap[ord(string)] = pitch
        
    def __getitem__(self,string):
        if len(string) != 1:
            raise ValueError("drum pitches can't have modifiers, you can only capitalize them")
        c = ord(string)
        iscaps = c >= ord('A') and c <= ord('Z')
        letter = c + ord('a') - ord('A') if iscaps else c 
        # if iscaps then we'll add the exrra pitch.
        p = self.pitchmap[letter]
        return [p,self.capsExtraPitch] if iscaps else [p]