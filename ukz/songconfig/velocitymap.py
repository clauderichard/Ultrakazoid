# from ukz.util.pwlinfunc import PwLinFunc
from ukz.config import SkzConfig

################################################

class VelocityMap:

    def __init__(self):
        self.velocitiesByPitch = {}
        for i in range(0,128):
            self.velocitiesByPitch[i] = {0: SkzConfig.defaultVelocity}

    def __eq__(self,other):
        return self.velocitiesByPitch == other.velocitiesByPitch

    def __repr__(self):
        return f"VelocityMap(vels={self.velocitiesByPitch})"

################################################

    def __validateVelDic(self,loudToVelDic):
        for _,v in loudToVelDic.items():
            if v < 0 or v > 127:
                raise ValueError('Bad velocity value')
    def __validatePitchVelDic(self,pitchToLoudVelDic):
        for p,dic in pitchToLoudVelDic.items():
            if p < 0 or p > 127:
                raise ValueError('Bad velocity value')
            self.__validateVelDic(dic)

################################################

    def setVelocities(self,loudnessVelocityDic):
        self.__validateVelDic(loudnessVelocityDic)
        for l,v in loudnessVelocityDic.items():
            for p in range(0,128):
                self.velocitiesByPitch[p][l] = v

    def setPitchVelocities(self,pitchLoudnessVelocityDic):
        self.__validatePitchVelDic(pitchLoudnessVelocityDic)
        self.velocitiesByPitch.update(pitchLoudnessVelocityDic)

################################################
