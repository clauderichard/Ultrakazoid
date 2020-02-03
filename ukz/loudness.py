from math import *
from ukz.numerize import *
from ukz.pwlinearfunction import *

################################

# Loudness and Volume
silenzioso = 0
pianississimo = 1
pianissimo = 2
piano = 3
mezzopiano = 4
mezzoforte = 5
forte = 6
fortissimo = 7
fortississimo = 8

maxLoudness = fortississimo+1
midiMaxPitch = 127
minVelocity = 0
maxVelocity = 127

################################

class LoudnessMap:
    
    def __init__(self,defaultVelocity):
        self.defaultVelocity = defaultVelocity
    
    def __getitem__(self,loudness):
        return self.defaultVelocity


class PwLinearLoudnessMap(LoudnessMap):
    
    def __init__(self,defaultVelocity):
        LoudnessMap.__init__(self,defaultVelocity)
        self.func = PwLinearFunction(0,0,9,127)
        self.func.addVertex(5,defaultVelocity)
        
    def __getitem__(self,loudness):
        return floor(self.func[loudness])

def mkLoudnessMapFromArg(arg):
    if arg is None:
        return PwLinearLoudnessMap(64)
    if isinstance(arg,int):
        return PwLinearLoudnessMap(arg)
    elif isinstance(arg,LoudnessMap):
        return arg
    elif isinstance(arg,list):
        m = PwLinearLoudnessMap(arg[5])
        for i in range(0,len(arg)):
            if i==5:
                continue
            m.func.addVertex(i,arg[i])
        return m
    else:
        raise ValueError(f'cannot make LoudnessMap from argument {arg}')

################################

class LoudnessMap2:
    
  def __init__(self):
    self.vvv = True
    self.pfs = []
    for p in range(0,128):
      f = PwLinearFunction(0,0,9,127)
      self.pfs.append(f)
    
  def setVel(self,pitch,loudness,velocity):
    self.pfs[pitch].addVertex(loudness,velocity)
  def setVelAllPitch(self,loudness,vel):
    for p in range(0,128):
      self.setVel(p,loudness,vel)
    
  def getVel(self,pitch,loudness):
    #if self.vvv:
    #  self.vvv = False
    #  for p in [66,67]:
    #    print("pfs ",p,self.pfs[p].pts)
    return floor(self.pfs[pitch][loudness])

def mkLoudnessMapFromArg2(arg):
  if arg is None:
    r = LoudnessMap2()
    return r
  elif isinstance(arg,dict):
    r = LoudnessMap2()
    for l,v in arg.items():
      if l is not None:
        r.setVelAllPitch(l,v)
    return r
  elif isinstance(arg,int):
    r = LoudnessMap2()
    r.setVelAllPitch(5,arg)
    return r
  elif isinstance(arg,LoudnessMap2):
    return arg
  elif isinstance(arg,list):
    m = LoudnessMap2()
    for i in range(0,len(arg)):
      m.setVelAllPitch(i,arg[i])
    return m
  else:
    raise ValueError(f'cannot make LoudnessMap2 from argument {arg}')
