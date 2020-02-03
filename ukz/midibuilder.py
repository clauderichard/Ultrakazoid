from midiutil import *

class MidiLog:
    f = None
    enabled = True

    @classmethod
    def init(cls):
        MidiLog.f = open("log.txt",'w')
        
    @classmethod
    def logg(cls,*argv):
      if MidiLog.enabled:
        for a in argv:
          MidiLog.f.write(f"{a} ")
        MidiLog.f.write("\n")
        
    @classmethod
    def close(cls):
        MidiLog.f.close()

def logg(*argv):
    MidiLog.logg(*argv)
        
class MidiBuilder:
    
    def __init__(self,numTracks):
        logg(f"construct MIDIFile(numTracks={numTracks})")
        self.midiFile = MIDIFile(numTracks)
        self.noteCount = 0
    
    def addTempo(self,t,tempo):
        if t<0:
            raise ValueError(f"Called addTempo with negative time t={t}.")
        if tempo<0:
            raise ValueError(f"Called addTempo with negative tempo tempo={tempo}.")
        logg("addTempo t={t} tempo={tempo}")
        self.midiFile.addTempo(0,t,tempo)
        
    def addProgramChange(self,tr,ch,t,prog):
        logg(f"addProgramChange t={t} prog={prog} route=({tr},{ch})")
        self.midiFile.addProgramChange(tr,ch,t,prog)
    
    def addVolumeChange(self,tr,ch,t,vol):
        logg(f"addVolumeChange t={t} vol={vol} route=({tr},{ch})")
        #logg(f"addControllerEvent controllerNumber=7 t={t} vol={vol} route=({tr},{ch})")
        self.midiFile.addControllerEvent(tr,ch,t,7,vol)

    def addPitchBend(self,tr,ch,t,bend):
        logg(f"addPitchBend t={t} bend={bend} route=({tr},{ch})")
        self.midiFile.addPitchWheelEvent(tr,ch,t,bend)

    def addNote(self,tr,ch,p,t,dur,vel):
        logg(f"addNote t={float(t)} dur={float(dur)} p={p} vel={vel} route=({tr},{ch})")
        self.midiFile.addNote(tr,ch,p,t,dur,vel)
        self.noteCount = self.noteCount + 1

    def writeFile(self,fileName):
        logg(f"writeFile fileName={fileName}")
        with open(fileName, "wb") as output_file:
            self.midiFile.writeFile(output_file)
