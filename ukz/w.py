
from ukz.u import *
from ukz.melody import *
from fractions import *

def parseNoteString(noteDecoder, note):
    return noteDecoder[note]

def opOnMelody(op,arg,mel):
    return ukzOpMap[op](mel,arg)

def flattenHierarchicalMelody(noteDecoder,hm):
    mel = Melody()
    if isinstance(hm,MelLeaf):
        if hm.note == ".":
          mel.forward(1)
        else:
          note = parseNoteString( \
           noteDecoder, hm.note )
          mel.playNote(note)
    elif isinstance(hm,MelNode):
        if hm.type == 0:
            # sequence
            for cmel in hm.childMelodies:
                mel.playMelody(flattenHierarchicalMelody(noteDecoder,cmel))
        elif hm.type == 1:
            # parallel
            mellength = 0
            b = True
            for cmel in hm.childMelodies:
                cmelody = flattenHierarchicalMelody(noteDecoder,cmel)
                if b:
                    mellength = cmelody.curTime
                    b = False
                mel.addMelody(cmelody)
            mel.forward(mellength)
    else:
        raise ValueError('cannot flatten this thing, what the heck is this?')
    for (op,arg) in hm.operators:
        mel = opOnMelody(op,arg,mel)
    return mel
