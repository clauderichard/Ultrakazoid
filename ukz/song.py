from midiutil import *
from ukz.scheme import *
from ukz.melody import *
from ukz.numerize import *

class TrackRoute:
    def __init__(self,trackI,channelI):
        self.trackI = trackI
        self.channelI = channelI

class Track:

  def __init__(self,song,track,channel,program):
    if isinstance(song,list):
        self.tracks = song
        self.tracks = False
    else:
        self.tracks = False
    self.midiRoutes = []
    self.track = track
    self.channel = channel
    self.curVolume = 100
    self.curTime = 0
    self.program = program
    self.curPitchShift = 0
    self.notes = []
    
  def setProgram(self):
    self.midifile.addProgramChange(self.track,self.channel,self.curTime,self.program)
  
  def switchProgram(self,prog):
    self.program = prog
    self.midifile.addProgramChange(self.track,self.channel,self.curTime,self.program)
  
  def setPitchShift(self,pitchShift):
    self.curPitchShift = pitchShift
  
  def addPitchWheelEvent(self,bendTime,val):
      self.midifile.addPitchWheelEvent(self.track,self.channel,bendTime*self.curTimeFactor,val)
  
  def addNote(self,pitch,duration=1,mustMove=True):
    if self.tracks:
        for t in self.tracks:
            t.addNote(pitch,duration,mustMove)
        return
    tr = self.track
    ch = self.channel
    pit = self.curPitchShift + value(pitch)
    tim = self.curTime
    dur = numerize(duration)
    vol = self.curVolume
    self.notes.append((tim,pit,dur,vol))
    self.midifile.addNote(tr,ch,pit,tim,dur,vol)
    if mustMove:
      if False:
          self.curTime = self.curTime + mustMove
      else:
          self.curTime = self.curTime + dur

  def addChord(self,chord,duration=1,mustMove=True):
      for p in value(chord):
          self.addNote(p,duration,False)
      if mustMove:
          self.forward(duration)

  def play(self,pitch,duration=1,mustMove=True):
      if isinstance(pitch,Melody):
          return self.addMelody(pitch,mustMove)
      return self.addNote(pitch,duration,mustMove)

  def addMelody(self,melody,mustMove=True):
    meltime = 0
    origtime = self.curTime
    for (time,pitch,duration) in melody.notes:
      self.forward(time-meltime)
      self.addNote(pitch,duration,False)
      meltime = time
    self.curTime = origtime + \
     melody.curTime
     

  def forward(self,duration):
    self.curTime = \
     self.curTime + \
     numerize(value(duration))
     
  def timeFlag(self):
    self.curFlag = self.curTime
  def goToFlag(self):
    self.curTime = self.curFlag

	
class Song:
    
    def __init__(self,name,initTempo):
        self.name = name
        self.initTempo = initTempo
        self.tracks = []

    # you can't call this after calling init
    def addTrack(self,program):
        if isinstance(program,list):
            ts = []
            for p in program:
                ts.append(self.addTrack(p))
            return Track(ts,0,0,0)
        tn = len(self.tracks)
        cn = tn
        if program<0:
            cn = 9
        elif cn>=9:
            cn = cn+1
        pr = max(0,program)
        tr = Track(self,tn,cn,pr)
        self.tracks.append(tr)
        return tr
        
    # most call this after adding tracks
    # and before writing
    def init(self):
        self.midifile = MIDIFile(len(self.tracks))
        self.midifile.addTempo(0,0,self.initTempo)
        for track in self.tracks:
            track.midifile = self.midifile
            track.setProgram()

    def syncTracksToTime(self,time):
        for track in self.tracks:
            track.curTime = time

    def syncToTrackTime(self,track):
        self.syncTracksToTime(track.curTime)

    def superWrite(self):
        print('no')

    # must call this after calling init
    def write(self):
        with open(self.name + ".mid", "wb") as output_file:
            self.midifile.writeFile(output_file)
