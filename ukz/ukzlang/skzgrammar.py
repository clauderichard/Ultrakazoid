from .midiprograms import programs,drumKits
from ukz.config import SkzConfig
from ukz.songconfig import ChannelConfig,SongConfig
from ukz.uklr.pattern import *

################################
# keywords
VELOCITY = "v"
VOLUME = "V"
OCTAVE = "o"
PROGNUMPREFIX = "i"
DRUMNUMPREFIX = "d"
BPS = "bps"
BPM = "bpm"
TPB = "tpb"
PITCHVELOCITY = "pv"
CHOIRIZE = "legato"

# Instrument setting components
LBRACK = "["
RBRACK = "]"
INT = "/INT"
WORD = "/WORD"
NAME = "/NAME"
PROGNUMSETTING = "/PROGNUMSETTING"
SONGSETTING = "/SONGSETTING"
SETTING = "/SETTING"
INSTR = "/INSTR"
CHANNEL = "/CHANNEL"

################################
# Some functions for stuff

alphaChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digitChars = '0123456789'
alphaNumericChars = alphaChars + digitChars

################################

def fillSkzTkRules(p):
        
    # numbers
    p.tokenizerRule(INT, digitChars)
    p.tokenizerRule(INT, digitChars, INT)
    p.tokenizerRule(WORD, alphaChars)
    p.tokenizerRule(WORD, alphaChars, WORD)

    p.tokenizerRule(WORD, alphaChars)

    # keywords
    p.keywords(WORD, [BPS,BPM,TPB,VELOCITY,VOLUME,\
      OCTAVE,PROGNUMPREFIX,DRUMNUMPREFIX,PITCHVELOCITY,CHOIRIZE])
    
    # names
    p.tokenizerRule(NAME, '%')
    p.tokenizerRule(NAME, alphaNumericChars, NAME)

    p.addSimpleSymbols( [LBRACK,RBRACK] )
        
    return p

################################

class TempoSetter:
    def __init__(self,t):
        self.t = t
    def apply(self,songConfig):
        songConfig.tempo = self.t

class TicksPerBeatSetter:
    def __init__(self,tpb):
        self.tpb = tpb
    def apply(self,songConfig):
        songConfig.tpb = self.tpb

class ChoirizeSetter:
    def __init__(self):
        pass
    def apply(self,channelConfig):
        channelConfig.choirize = True

class VelocitiesSetter:
    def __init__(self,velsDic):
        self.velsDic = velsDic
    def apply(self,channelConfig):
        channelConfig.setVelocities(self.velsDic)

class OctaveSetter:
    def __init__(self,o):
        self.o = o
    def apply(self,channelConfig):
        channelConfig.octave = self.o

class ProgramNumberSetter:
    def __init__(self,programNumber,isDrums=False):
        self.programNumber = programNumber
        self.isDrums = isDrums
    def apply(self,channelConfig):
        channelConfig.programNumber = self.programNumber
        channelConfig.isDrums = self.isDrums

class VolumeSetter:
    def __init__(self,o):
        self.o = o
    def apply(self,channelConfig):
        channelConfig.volume = self.o

class PitchVelocitiesSetter:
    def __init__(self,p,velsDic):
        self.p = p
        self.velsDic = velsDic
    def apply(self,channelConfig):
        channelConfig.setVelocitiesForPitch(self.p,self.velsDic)

################################

def mkVelSetting(a,nums):
    snums = sorted(nums)
    i = - snums.index(nums[0])
    dic = {}
    for sn in snums:
        dic[i] = sn
        i += 1
    return VelocitiesSetter(dic)
    
def mkPitchVelSetting(a,nums):
    pitch = nums[0]
    snums = sorted(nums[1:])
    i = - snums.index(nums[1])
    dic = {}
    for sn in snums:
        dic[i] = sn
        i += 1
    return PitchVelocitiesSetter(pitch,dic)
    #return {'pitchvelocities': {pitch:dic}}

def mkProgNum(a,num):
    return ProgramNumberSetter(num,False)
def mkDrumNum(a,num):
    return ProgramNumberSetter(num,True)
def mkProgNumWithNames(name1,nams):
    names = [name1] + nams
    try:
        prognum = programs[names]
        return ProgramNumberSetter(prognum,False)
    except ValueError:
        prognum = drumKits[names]
        return ProgramNumberSetter(prognum,True)

def mkChannel(names,progsetter,settings):
    ret = ChannelConfig( \
      names = list(map(lambda x: x[1:], names)) )
    progsetter.apply(ret)
    for s in settings:
        s.apply(ret)
    return ret

def mkSong(l,songsettings,chansettings,r):
    ret = SongConfig(SkzConfig.defaultTempo,chansettings)
    for s in songsettings:
        s.apply(ret)
    return ret

################
# Parse-traverse Rules

def fillSkzPrTrRules(p):
    
    p.parserLeafRule( INT, lambda s: int(s) )
    
    p.parserRule( SONGSETTING, [BPM, INT], lambda _,t: TempoSetter(t))
    p.parserRule( SONGSETTING, [BPS, INT], lambda _,t: TempoSetter(t*60))
    p.parserRule( SONGSETTING, [TPB, INT], lambda _,t: TicksPerBeatSetter(t))
    
    p.parserRule( PROGNUMSETTING, [PROGNUMPREFIX,INT], mkProgNum)
    p.parserRule( PROGNUMSETTING, [DRUMNUMPREFIX,INT], mkDrumNum)
    p.parserRule( PROGNUMSETTING, [WORD, star(alt(WORD,INT))], mkProgNumWithNames)

    p.parserRule( SETTING, [CHOIRIZE], lambda _: ChoirizeSetter())
    p.parserRule( SETTING, [VOLUME, INT], lambda _,num: VolumeSetter(num))
    p.parserRule( SETTING, [OCTAVE, INT], lambda _,o: OctaveSetter(o))
    p.parserRule( SETTING, [VELOCITY, plus(INT)], mkVelSetting )
    p.parserRule( SETTING, [PITCHVELOCITY, plus(INT)], mkPitchVelSetting )

    p.parserRule( CHANNEL, [plus(NAME), PROGNUMSETTING, star(SETTING)], mkChannel)

    p.parserRule( SETTING, [ LBRACK, star(SONGSETTING), star(CHANNEL), RBRACK], mkSong)

    return p
        