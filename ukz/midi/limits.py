
class Limits:
    
  minTempo = 1
  # todo find the real maxTempo
  maxTempo = None
    
  minPitch = 0
  maxPitch = 127
  minVelocity = 0
  maxVelocity = 127
  minProgram = 0
  maxProgram = 127
  
  minVolume = 0
  maxVolume = 127
  defaultVolume = 96
  
  minPitchBend = -8192
  neutralPitchBend = 0
  maxPitchBend = 8191
  minPitchBend1 = -64
  neutralPitchBend1 = 0
  maxPitchBend1 = 64
  
  minChannel = 0
  maxChannel = 15
  minTrack = 0
  maxTrack = 15
  drumsChannel = 9
  
  minTime = 0
  maxTime = None
  minDuration = 0.000001
  maxDuration = None
  
  @classmethod
  def mapPitchBend1(cls,b):
    return min(b*128,8191)
  
  @classmethod
  def __checkRange(self,\
   name,minVal,maxVal,val):
    if minVal is not None\
     and val < minVal:
      raise ValueError(f'The {name} is below the belt.')
    if maxVal is not None\
     and val > maxVal:
      raise ValueError(f'The {name}... is TOO DAMN HIGH!')
  
  @classmethod
  def checkPitch(cls,val):
    cls.__checkRange('pitch number',\
     cls.minPitch,cls.maxPitch,val)
    
  @classmethod
  def checkVelocity(cls,val):
    cls.__checkRange('velocity number',\
     cls.minVelocity,cls.maxVelocity,\
     val)
  
  @classmethod
  def checkProgram(cls,val):
    cls.__checkRange('program number',\
     cls.minProgram,cls.maxProgram,val)
  
  @classmethod
  def checkTempo(cls,val):
    cls.__checkRange('tempo',\
     cls.minTempo,cls.maxTempo,val)
  
  @classmethod
  def checkVolume(cls,val):
    cls.__checkRange('volume',\
     cls.minVolume,cls.maxVolume,val)
  
  @classmethod
  def checkPitchBend(cls,val):
    cls.__checkRange('pitch bend number',\
     cls.minPitchBend,cls.maxPitchBend,val)
  
  @classmethod
  def checkChannel(cls,val):
    cls.__checkRange('channel number',\
     cls.minChannel,cls.maxChannel,val)
  
  @classmethod
  def checkTrack(cls,val):
    cls.__checkRange('track number',\
     cls.minTrack,cls.maxTrack,val)
  
  @classmethod
  def checkTime(cls,val):
    cls.__checkRange('time value',\
     cls.minTime,cls.maxTime,val)
  
  @classmethod
  def checkDuration(cls,val):
    cls.__checkRange('duration value',\
     cls.minDuration,cls.maxDuration,val)
  