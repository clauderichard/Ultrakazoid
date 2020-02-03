from math import floor
from ukz.midi import Limits
from ukz.utils.pwlinfunc import *

################################

class Amp:
    
  minLoudness = 0
  maxLoudness = 9
    
  def __init__(self,vels={}):
    self.volume = Limits.defaultVolume
    self.pfs = []
    for _ in range(\
     Limits.minPitch,\
     Limits.maxPitch+1):
      f = PwLinFunc(\
       Amp.minLoudness,\
       Limits.minVelocity,\
       Amp.maxLoudness,\
       Limits.maxVelocity)
      self.pfs.append(f)
    if isinstance(vels,dict):
      for k,v in vels.items():
        self[k] = v
    elif isinstance(vels,int):
      self[None] = vels
    
    	
  def __setitem__(self,index,value):
    if index is None:
      self.volume = value
      return
    Limits.checkVelocity(value)
    if isinstance(index,int):
      for p in range(\
       Limits.minPitch,\
       Limits.maxPitch+1):
        self.pfs[p].addVertex(\
        	index,value)
    else:
      (p,l) = index
      self.pfs[p].addVertex(l,value)
      
  def __getitem__(self,index):
    if index is None:
      return self.volume
    if isinstance(index,int):
      raise ValueError('Why get velocity at loudness alone? Pass the pitch, man!')
    else:
      (p,l) = index
      return floor(self.pfs[p][l])
