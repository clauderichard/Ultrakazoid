from ukz.melody.controllers import UkzControllers

def log(string='',**args):
    if UkzConfig.logEnabled:
        print(string,flush=True,**args)

class UkzConfig:

################################

    # ukz writes to this directory
    #outputMidiFolder = "../../foobar2000/Music/AMidi" # Desktop
    outputMidiFolder = "../AMidi" # Android

    logEnabled = True

################################

class SkzConfig:

    defaultOctave = 0
    defaultVolume = 105
    defaultVelocity = 96
    defaultProgramNumber = 0
    defaultTempo = 120
