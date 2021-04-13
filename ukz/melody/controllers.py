
class UkzControllers:

    pitchBend = 0
    volume = 1
    balance = 2
    expression = 3
    attack = 4
    reverb = 5
    numControllers = 6

    midiControllerMap = {
        volume: 7,
        balance: [8,10],
        expression: 11,
        attack: 73,
        reverb: 91
    }

    controllerDefaultValues = {
        pitchBend: 64,
        volume: 127,
        balance: 64,
        expression: 127,
        attack: 64,
        reverb: 96
    }

################################

    @classmethod
    def mapControllerToMidi(cls,ctrl):
        x = cls.midiControllerMap.get(ctrl,None)
        if x is not None:
            if isinstance(x,list):
                yield from x
            elif isinstance(x,int):
                yield x
            else:
                raise ValueError("midiControllerMap is badly structured")
        else:
            yield ctrl

    @classmethod
    def addControllerEventStream(cls,midiw,ctrl,channelTimeVals):
        if ctrl == cls.pitchBend:
            for ch,time,val in channelTimeVals:
                midiw.addPitchBend(ch,time,val)
            return
        else:
            cs = cls.mapControllerToMidi(ctrl)
            for c in cs:
                midiw.addControllerEventStream(c,channelTimeVals)
    
################################
