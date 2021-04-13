import math
from .byteutil import *
from .config import MidiConfig

################################################

# Note: There are 24 MIDI clocks per quarter-note, apparently...

################################################

class EventCategory:
    TIMESIGNATURE = 0
    TEMPOCHANGE = 1
    PROGRAMCHANGE = 2

    CONTROLCHANGE = 10

    NOTEOFF = 21 # note off BEFORE note on
    NOTEON = 22

################################################

class MidiWriter:
    
    def __init__(self,filename):
        self.file = open(filename,'wb')
        self.eventByteArray = bytearray(b'')
        # self.eventBytes = []
        self.evs = []
        self.__addTimeSignature()
        self.ch = 0
        self.endTicks = 0
        self.tempoMultiplier = 1
        self.__initForCh()

    def setTpb(self,tpb):
        MidiConfig.tpb = tpb # ukz's tpb
        self.tempoMultiplier = 1
        if tpb > 127:
            for i in range(2,1000):
                if tpb%i==0 and tpb//i <= 127:
                    self.tpb = tpb//i #header's tpb
                    self.tempoMultiplier = i
                    return
            raise Exception(f"Value tpb={tpb} is a bad one")
        else:
            self.tpb = tpb
            self.tempoMultiplier = 1
    
    def __addTimeSignature(self):
        # Time signature bytes: FF 58 04 nn dd cc bb
        # The fraction you see on a score would be nn / 2^dd
        #   (denominator always has to be power of 2)
        # cc = number of MIDI clocks in a metronome click.
        # bb = number of notated 32nd-notes in a MIDI quarter-note.
        #   bb was added in MIDI to support legacy(?)

        self.__addGenericEvent(0, EventCategory.TIMESIGNATURE, b'\xFF\x58\x04\x04\x02\x24\x08')

    # def getMaxEventBeats(self):
    #     maxTicks = max(map(lambda e: e[0], self.evs))
    #     return maxTicks / MidiConfig.tpb

    def getMaxEventTicks(self):
        return max(map(lambda e: e[0], self.evs))

    def __initForCh(self):
        chBytePos = self.ch << 16
        self.chNoteOn = 0x900000 | chBytePos
        self.chNoteOff = 0x800000 | chBytePos
        self.chPitchBend = 0xE00000 | chBytePos
    
    def switchToChannel(self,channelNumber):
        if channelNumber < 0 or channelNumber > 15:
            raise ValueError("Bad channel number")
        self.ch = channelNumber
        self.__initForCh()
    
    def __addGenericEvent(self,time,category,eventBytes):
        if isinstance(time,float):
            raise 'what!'
        timeTicks = time
        self.evs.append((timeTicks,category,eventBytes))

    # Argument tempo in beats per minute
    def addTempoChange(self,t,beatsPerMinute):
        if t < 0:
            raise ValueError("Negative time!")
        if beatsPerMinute < 1:
            raise Exception("That's a little too slow, man.")
        
        # One beat is 24 ticks.
        # bpm = 120  =>  µsecsPerBeat = 500,000
        microsecondsPerBeat = 60000000//beatsPerMinute
        # X beat/min == Y µsec/beat
        # 1 min = X beats = (X*Y) µsecs
        # 1 min = 60 million µsecs
        # 0xA120 in decimal is 500000

        self.addTempoChangeMicroseconds(t,microsecondsPerBeat)
        
    # Argument tempo in beats per minute
    def addTempoChangeMicroseconds(self,t,microsecondsPerBeat):
        if t < 0:
            raise ValueError("Negative time!")

        if self.tempoMultiplier > 1:
            microsecondsPerBeat = microsecondsPerBeat // self.tempoMultiplier

        if microsecondsPerBeat < 1:
            raise Exception("That's a little too fast, man.")
        if microsecondsPerBeat >= 2**24:
            raise Exception("That's a little too slow, man.")
        
        theBytes = bytearray(b'\xFF\x51') + intToLengthedBytes3(microsecondsPerBeat)
        self.__addGenericEvent(t, EventCategory.TEMPOCHANGE, theBytes)
        
    def addProgramChanges(self,t,channelPrograms):
        for ch,prog in channelPrograms:
            if t < 0:
                raise ValueError("Negative time!")
            if prog < 0 or prog > 127:
                raise ValueError("Bad program number")
            
            theBytes = bytearray([0xc0 | ch,prog])
            self.__addGenericEvent(0, EventCategory.PROGRAMCHANGE, theBytes)
    
    def addProgramChange(self,ch,t,prog):
        if t < 0:
            raise ValueError("Negative time!")
        if prog < 0 or prog > 127:
            raise ValueError("Bad program number")
        
        #theBytes = prog | ((0xc0 | self.ch)<<8).to_bytes(2)
        theBytes = bytearray([0xc0 | ch,prog])
        self.__addGenericEvent(0, EventCategory.PROGRAMCHANGE, theBytes)
    
################################################

    def addInitialVolumes(self,time,channelVolumes):
        for ch,vol in channelVolumes:
            self.addControllerEvent(ch,7,time,vol)
            self.addControllerEvent(ch,11,time,127)

    def addInitialVolume(self,ch,time,vol):
        self.addControllerEvent(ch,7,time,vol)
        self.addControllerEvent(ch,11,time,127)

    def addControllerEvent(self,ch,ctrl,time,val):
        if val < 0 or val > 127:
            raise Exception("Bend out of range!")
        if time < 0:
            raise Exception("Time negative!")
        
        theBytes = bytearray([0xB0 | ch, ctrl, val])
        self.__addGenericEvent(time, EventCategory.CONTROLCHANGE, theBytes)

    def addControllerEventStream(self,ctrl,channelTimeVals):
        evs = self.evs
        category = EventCategory.CONTROLCHANGE
        for ch,time,val in channelTimeVals:
            if val < 0 or val > 127:
                raise Exception("Bend out of range!")
            if time < 0:
                raise Exception("Time negative!")
        
            theBytes = bytearray([0xB0 | ch, ctrl, val])
            
            # self.__addGenericEvent(time, EventCategory.CONTROLCHANGE, theBytes)
            timeTicks = time
            evs.append((timeTicks,category,theBytes))

################################################

    # Assume this works like any other controller.
    # But here we map bend value to the range
    #   that MIDI's pitch-bend event expects.
    def addPitchBend(self,ch,time,bend):
        if bend < 0 or bend > 127:
            raise Exception("Bend out of range!")
        if time < 0:
            raise Exception("Time negative!")

        #theBytes = (self.chPitchBend | (bend<<8) | bend).to_bytes(3,'big')
        theBytes = bytearray([0xE0 | ch, bend, bend])
        self.__addGenericEvent(time, EventCategory.CONTROLCHANGE, theBytes)

    def addNotes(self,notes):
        for note in notes:
            
            if note.p < 0 or note.p > 127:
                raise Exception("Pitch out of range!")
            if note.t < 0:
                raise Exception("Time negative!")
            if note.d < 0:
                raise Exception("Duration negative!")
            if note.l < 0 or note.l > 127:
                raise Exception("Velocity out of range!")

            # 0x90 is status byte for noteOn
            # 0x80 is status byte for noteOff
            # theBytesOn = (self.chNoteOn | (pitch<<8) | vel).to_bytes(3,'big')
            theBytesOn = bytearray([0x90 | note.c, note.p, note.l])
            # theBytesOff = (self.chNoteOff | (pitch<<8) | vel).to_bytes(3,'big')
            theBytesOff = bytearray([0x80 | note.c, note.p, note.l])
            
            timeTicksOn = note.t
            timeTicksOff = note.t+note.d
            if isinstance(timeTicksOn,float) or isinstance(timeTicksOff,float):
                raise 'what!'
            self.evs.append((timeTicksOn, EventCategory.NOTEON, theBytesOn))
            self.evs.append((timeTicksOff, EventCategory.NOTEOFF, theBytesOff))
            

    def setEndTime(self,t):
        self.endTicks = t

    def __setEventBytes(self):
        self.evs.sort()
        curtimeTicks = 0
        self.eventByteArray = bytearray(b'')
        
        bs = bytearray()

        for timeTicks,_,ebytes in self.evs:
            deltaTicks = timeTicks-curtimeTicks
            
            # self.eventByteArray.extend(intToVarLengthBytes(deltaTicks))
            if deltaTicks==0:
                self.eventByteArray += b'\x00'
            else:
                bs.clear()
                bs.insert(0, deltaTicks % 128) # rightmost byte, bit 7 NOT set
                m = deltaTicks >> 7
                while m > 0:
                    bs.insert(0, (m % 128) | 0x80) # NOT rightmost byte, bit 7 IS set
                    m >>= 7
                self.eventByteArray += bs

            self.eventByteArray.extend(ebytes)
            curtimeTicks = timeTicks

        deltaTicks = self.endTicks - curtimeTicks
        self.eventByteArray.extend(intToVarLengthBytes(deltaTicks))
        self.eventByteArray.extend(b'\xFF\x2F\x00')
        # self.eventByteArray.extend(b'\x00\xFF\x2F\x00') # track end
    
    def writeFile(self):
        self.__writeHeaderChunk()
        self.__setEventBytes()
        self.__writeChunk(b'MTrk',self.eventByteArray)
        self.file.close()

    def __writeChunk(self,typenameBytes,chunkBytesArray):
        self.__writeBytes(typenameBytes)
        self.__writeBytes(intToBytes(len(chunkBytesArray), 4))
        self.__writeBytes(chunkBytesArray)

    def __writeHeaderChunk(self):
        headerBytes = bytearray(b'\x00\x00\x00\x01\x00')
        headerBytes += bytes([self.tpb])
        self.__writeChunk(b'MThd',headerBytes)
    
    def __writeBytes(self,theBytes):
        self.file.write(theBytes)
    