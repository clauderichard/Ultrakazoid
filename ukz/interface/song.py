import os
from ukz.midi import MidiWriter,MidiConfig
#from .instr import *
from ukz.melody import Fmel
from ukz.ukzlang import ukz,skz
from ukz.util import intsFromTo,Tempos
from ukz.config import UkzConfig,log
from ukz.util import MultiMap,secondsToTimeString,getAbsFilePath
from .melodyresolver import MelodyResolver

class Song:

    def __init__(self,confcode):
        songConfig = skz(confcode)
        self.time = 0
        self.channelConfigs = {}
        self.nameToChannelMap = MultiMap()
        self.tempoChanges = Tempos(songConfig.tempo)

        self.songConfig = songConfig
        MidiConfig.tpb = self.songConfig.tpb

        self.numTimesPlayCalled = 0

        self.globalFmels = []
        log("  Song initialized.")
        log("  Start parsing...")
        log("  ",end='')

    ################################

    def play(self,code):
        mel = ukz(code)

        self.globalFmels.append(mel)

        self.time += mel.d

        self.numTimesPlayCalled += 1
        log(f"{self.numTimesPlayCalled} ",end='')

    def gradualTempo(self,te1,dt1,te2,dt2):
        if te1==te2:
            return
        for te in intsFromTo(te1,te2):
            dt = dt1 + (dt2-dt1)*(te-te1)/(te2-te1)
            self.setTempo(te,dt)

    def setTempo(self,tempo,dt=0):
        t = self.time + dt
        self.tempoChanges[t] = tempo
        
    ################################
        
    def write(self,name):

        log()

        midifilename = f"{UkzConfig.outputMidiFolder}/{name}.mid"
        try:
            os.makedirs(UkzConfig.outputMidiFolder)
        except:
            pass
        midiw = MidiWriter(midifilename)
        midiw.setTpb(self.songConfig.tpb)

        log(f"  Writing initial state... ")
        self.songConfig.writeInitialState(midiw)
        
        log(f"  Writing tempos... ")
        for t,te in self.tempoChanges.items():
            midiw.addTempoChange(t,te)

        log(f"  Mapping melodies to midi... ")
        self.__writeMidiNotesAndGradients(midiw)

        log(f"  Writing to file... ")
        midiw.writeFile()

        self.__printSongWritten(name,midiw,midifilename)

    ################################

    def __getResolver(self):
        resolver = MelodyResolver(self.songConfig)
        dt = 0
        for mel in self.globalFmels:
            # TODO: don't map here, map inside resolve method after resolving gradients
            # notes = self.songConfig.mapNotesFromMelody(mel.notes,dt)
            # grads = self.songConfig.mapGradientsFromMelody(mel.gradients,dt)
            resolver.addNotes(mel.notes,dt)
            resolver.addGradients(mel.gradients,dt)
            dt += mel.d
        resolver.endTime = dt
        return resolver

    def __writeMidiNotesAndGradients(self,midiw):
        resolver = self.__getResolver()
        resolver.resolve()
        midiw.addNotes(resolver.notes)
        self.songConfig.writeGradientsFromMelody(resolver.gradients,midiw)
        midiw.setEndTime(resolver.endTime)
    
    def __printSongWritten(self,name,midiw,midifilename):
        songSecs = self.tempoChanges.ticksToSeconds(midiw.endTicks)
        lengthStr = secondsToTimeString(songSecs)
        log("Song written!")
        log(f"  Title: {name}")
        log(f"  Approx Length: {lengthStr}")
        absfilename = getAbsFilePath(midifilename)
        log(f"  Location: {absfilename}")

    ################################
