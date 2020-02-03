from math import *
from ukz.numerize import *

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

maxLoudness = fortississimo

################################

class Velocities:
    def __init__(self,velocities):
        self.vels = velocities
    def __getitem__(self,loudness):
        l = numerize(loudness)
        if isinstance(l,int):
            return self.vels[l]
        l1 = floor(l)
        l2 = l1+1
        beta = l-l1
        alpha = l2-l
        v1 = self.vels[l1]
        v2 = self.vels[l2]
        return floor(v1*alpha + v2*beta)

minVelocity = 0
maxVelocity = 127
defaultVelocities = \
 [0,16,32,48,64,80,96,112,127]
 
def mkVelocities(\
	theVelocity=100,\
	loudness=mezzoforte):
    theVel = numerize(theVelocity)
    if theVel<0:
        raise ValueError(f"cannot mkVelocities with negative velocity {theVelocity}")
    if theVel>maxVelocity:
        raise ValueError(f"cannot mkVelocities with velocity greater than {maxVelocity}, but was {theVolume}")
    vels = [0]
    for i in range(1,loudness):
        v =	theVel*i/loudness
        vels.append(floor(v))
    vels.append(floor(theVel))
    for i in range(loudness+1,\
    	fortississimo+1):
        t = (i-loudness) / \
         (fortississimo-loudness)
        v = theVel*(1-t) + \
         maxVelocity*t
        v = floor(v)
        vels.append(v)
    return Velocities(vels)
    
################################
