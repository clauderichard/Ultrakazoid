from math import *
from ukz.numerize import *
from ukz.piecewiselinearfunction import *

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
        self.func = PiecewiseLinearFunction(0,0,9,127)
        self.func.addVertex(5,defaultVelocity)
        
    def __getitem__(self,loudness):
        return floor(self.func[loudness])

def mkLoudnessMapFromArg(arg):
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
