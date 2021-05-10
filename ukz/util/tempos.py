from ukz.midi.config import MidiConfig

class Tempos:

    def __init__(self,initTempo):
        self.ts = {0:initTempo}
        self.initTempo = initTempo
        
    def items(self):
        return self.ts.items()
        
    def __setitem__(self,i,v):
        self.ts[i] = v
        
    # Returns how many seconds for a
    # number of beats into the song
    def ticksToSeconds(self,ticks):
        secs = 0
        time = 0
        tempo = self.initTempo * MidiConfig.tpb
        for t,te in sorted(self.items()):
            if t > ticks:
                break
            secs += (t-time) * 60 / tempo
            tempo = te * MidiConfig.tpb
            time = t
        secs += (ticks-time) * 60 / tempo
        return secs
