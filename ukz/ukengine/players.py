from math import floor
from ukz.midi import MidiWriter
#from .instr import *
from ukz.melody import Fmel
from .player import PlayerBase,Player,Drummer
from ukz.utils import intsFromTo

class Players:
    
  def __init__(self,players=[]):
    self.players = list(players)
    self.hasDrummer = False
    self.hasPlayer = False
    for p in self.players:
      if isinstance(p,Drummer):
        self.hasDrummer = True
      if isinstance(p,Player):
        self.hasPlayer = True

  def reset(self):
    for t in self.players:
      t.reset()

  def newPlayer(self,*args):
    x = Player(*args)
    self.players.append(x)
    self.hasPlayer = True
    return x
        
  def newPlayers(self,n,*args):
    ls = []
    for i in range(0,n):
      ls.append(self.newPlayer(args))
    return ls
        
  def newDrummer(self,*args):
    if self.hasDrummer:
      raise ValueError("Cannot add more than one drummer")
    x = Drummer(*args)
    self.players.append(x)
    self.hasDrummer = True
    return x
    
  def play(self,ukzstr):
    if self.hasPlayer and \
     self.hasDrummer:
      raise Exception('drummer and player cannot play the same string')
    for p in self.players:
      p.play(ukzstr)
      
  def choirize(self):
    for p in self.players:
      p.choirize()
    
  def __addi__(self,player):
    if isinstance(player,Drummer):
      self.hasDrummer = True
    else:
      self.hasPlayer = True
    self.players.append(player)
        
  # make all tracks go to the
  # specified time. 
  def goto(self,to):
    t = to.fmel.d \
     if isinstance(to,PlayerBase) \
     else to.d if isinstance(to,Fmel) \
     else to
    for player in self.players:
      player.goto(t)

  # Make all players go to the
  # latest time of all the players
  def sync(self):
    t = self.maxTime()
    self.goto(t)

  def maxTime(self):
    return max(map(lambda p: p.fmel.d, \
     self.players))

  def countInstrs(self):
    return sum(map(lambda p: \
     len(p.getInstrs()), \
     self.players))

  def getTimeString(self,secs):
    m = floor(secs)//60
    s = floor(secs) - 60*m
    s1 = s//10
    s0 = s%10
    return f"{m}:{s1}{s0}"


  
class Song(Players):

  def __init__(self,*args):
    Players.__init__(self,*args)
    self.tempoChanges = {}
    
  def gradualTempo(self,te1,dt1,te2,dt2):
    if te1==te2:
      return
    for te in intsFromTo(te1,te2):
      dt = dt1 + (dt2-dt1)*(te-te1)/(te2-te1)
      self.setTempo(te,dt)
    
  def setTempo(self,tempo,dt=0):
    t = self.maxTime() + dt
    self.tempoChanges[t] = tempo
    
  def write(self,initTempo,name):
    self.tempoChanges[0] = initTempo
    numTr = self.countInstrs()
    midi = MidiWriter(numTr)
    for t,te in self.tempoChanges.items():
      midi.addTempo(t,te)
    for player in self.players:
      player.write(midi)
    midifilename = f"../AMidi/{name}.mid"
    midi.writeFile(midifilename)
    self.printSongWritten(\
     initTempo,name,midi)

  def toSeconds(self,beats):
    secs = 0
    time = 0
    tempo = 120
    for t,te in sorted(self.tempoChanges.items()):
      secs += (t-time) * 60 / tempo
      tempo = te
      time = t
    secs += (beats-time) * 60 / tempo
    return secs
  def printSongWritten(self,\
   initTempo,name,midiw):
    #songLength = self.maxTime()
    songLength = midiw.maxTime
    songSecs = self.toSeconds(songLength)
    lengthStr = self.getTimeString(songSecs)
    print('Song written!')
    print('  Title:', name)
    print(f"  Approx Length: {lengthStr}")
