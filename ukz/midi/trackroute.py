from .limits import *

class TrackRoute:
  
  def __init__(self,\
   trackNumber,channelNumber):
    self.track = trackNumber
    self.channel = channelNumber

class TrackRouteGenerator:
    
  def __init__(self):
    self.tn = -1
    self.cn = -1
    self.dr = 0
    
  def gen(self,prog):
    if prog.isDrums:
      return self.genDrums()
    else:
      return self.genNonDrums()
    
  def genDrums(self):
    self.dr += 1
    if self.dr > 1:
      raise ValueError("Too many drum tracks!")
    self.tn += 1
    Limits.checkTrack(self.tn)
    return TrackRoute(\
    	self.tn,Limits.drumsChannel)
  
  def genNonDrums(self):
    self.tn += 1
    Limits.checkTrack(self.tn)
    self.cn += 1
    if self.cn == Limits.drumsChannel:
      self.cn += 1
    Limits.checkChannel(self.cn)
    return TrackRoute(\
    	self.tn,self.cn)
