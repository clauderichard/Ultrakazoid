from .channelconfig import ChannelConfig
from ukz.config import SkzConfig
from ukz.melody import Note,Gradient
from .drumpitch import DrumPitchUkz
from ukz.melody.controllers import UkzControllers

################################################

class SongConfig:

    def __init__(self,tempo,channelConfigs):
        self.tempo = tempo
        self.tpb = 96
        self.channelConfigs = list(channelConfigs)
        self.__initChannelMaps()
        self.__initNoteMaps()

    def __initChannelMaps(self):
        nextInstrChannel = 0
        drumsChannel = 9
        self.nameToChannels = {}
        for channelConfig in self.channelConfigs:
            if channelConfig.isDrums:
                channelConfig.channel = drumsChannel
            else:
                channelConfig.channel = nextInstrChannel
                nextInstrChannel += 1
                if nextInstrChannel==drumsChannel:
                    nextInstrChannel += 1
            for name in channelConfig.names:
                self.nameToChannels.setdefault(name,[]).append(channelConfig.channel)
    
    def __initNoteMaps(self):
        drumsChannel = 9
        self.pitchmap = {}
        self.velmap = {}
        for chanConf in self.channelConfigs:
            c = chanConf.channel
            if c==drumsChannel:
                for ukzp,midip in DrumPitchUkz.pitchMap.items():
                    self.pitchmap[(c,ukzp)] = midip
                for midip in range(0,127):
                    ukzp = 10000 + midip
                    self.pitchmap[(c,ukzp)] = midip
            else:
                octaveShift = 12 * chanConf.octave
                for midip in range(0,127):
                    ukzp = midip - octaveShift
                    self.pitchmap[(c,ukzp)] = midip
            for p,lvs in chanConf.velocityMap.velocitiesByPitch.items():
                for l,v in lvs.items():
                    self.velmap[(c,p,l)] = v
    
    def __eq__(self,other):
        return self.tempo == other.tempo and \
          self.channelConfigs == other.channelConfigs
    
    def __repr__(self):
        return f"SongConfig(tempo={self.tempo},channelConfigs={self.channelConfigs})"

    def getChoirizedChannels(self):
        ret = set()
        for conf in self.channelConfigs:
            if conf.choirize:
                ret.add(conf.channel)
        return ret

################################################

    def mapNotesFromMelody(self,notes):
        nameToChannels = self.nameToChannels
        pitchmap = self.pitchmap
        velmap = self.velmap
        ret = []
        for note in notes:
            chs = nameToChannels[note.c]
            for c in chs:
                p = pitchmap[(c,note.p)]
                vel = velmap[(c,p,note.l)]
                ret.append(Note(p,note.t,note.d,vel,c))
        return ret

    def mapNotesFromMelody_old(self,notes,dt):
        nameToChannels = self.nameToChannels
        pitchmap = self.pitchmap
        velmap = self.velmap
        ret = []
        for note in notes:
            chs = nameToChannels[note.c]
            for c in chs:
                p = pitchmap[(c,note.p)]
                vel = velmap[(c,p,note.l)]
                ret.append(Note(p,note.t+dt,note.d,vel,c))
        return ret

    def mapGradientsFromMelody(self,gradients,dt):
        nameToChannels = self.nameToChannels
        ret = []
        for grad in gradients:
            chs = nameToChannels[grad.c]
            for c in chs:
                ret.append(Gradient(grad.typ,grad.t+dt,grad.d,grad.bend,c))
        return ret

    def writeGradientsFromMelody(self,gradients,midiw):
        nameToChannels = self.nameToChannels
        ret = []
        lastValues = UkzControllers.controllerDefaultValues.copy()
        for gradient in gradients:
            # chs = [gradient.c]
            chs = nameToChannels[gradient.c]
            lastValue = lastValues[gradient.typ]
            intPts = gradient.getIntPoints(lastValue)
            channelTimeVals = []
            for ch in chs:
                for gt,gv in intPts:
                    channelTimeVals.append((ch,gt,gv))
            UkzControllers.addControllerEventStream( \
                midiw, gradient.typ, channelTimeVals)
            lastValues[gradient.typ] = gradient.getLastValue()
        return ret

    def writeInitialState(self,midiw):
        cvs = []
        cprogs = []
        for chanConf in self.channelConfigs:
            cvs.append((chanConf.channel,chanConf.volume))
            cprogs.append((chanConf.channel,chanConf.programNumber))
        midiw.addInitialVolumes(0,cvs)
        midiw.addProgramChanges(0,cprogs)

################################################
