from .velocitymap import VelocityMap
from ukz.config import SkzConfig

class ChannelConfig:

    def __init__(self,**args):
        self.names = set()
        for n in args.get('names',[]):
            self.names.add(n)
        self.isDrums = args.get('isDrums', False)
        self.octave = args.get('octave', 0)
        self.volume = args.get('volume', SkzConfig.defaultVolume)
        self.programNumber = args.get('programNumber', SkzConfig.defaultProgramNumber)
        vels = args.get('velocities', {})
        pvels = args.get('pitchVelocities', {})
        self.velocityMap = VelocityMap()
        self.velocityMap.setVelocities(vels)
        self.velocityMap.setPitchVelocities(pvels)
        self.choirize = args.get('choirize', False)
        self.channel = -1
    
    def __eq__(self,other):
        return self.names == other.names and \
          self.octave == other.octave and \
          self.volume == other.volume and \
          self.programNumber == other.programNumber and \
          self.isDrums == other.isDrums and \
          self.velocityMap == other.velocityMap and \
          self.choirize == other.choirize
    
    def __repr__(self):
        return f"ChannelConfig(names={self.names},o={self.octave},vol={self.volume},prog={self.programNumber}{',isDrums' if self.isDrums else ''},velmap={self.velocityMap})"
    
    def setVelocities(self,dic):
        self.velocityMap.setVelocities(dic)
    
    def setVelocitiesForPitch(self,pitch,dic):
        self.velocityMap.setPitchVelocities({pitch: dic})
