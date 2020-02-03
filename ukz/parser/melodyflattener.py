
from ukz.parser.traverserules import *
from ukz.melody import *
from ukz.parser.melodyopmap import *
from ukz.parser.states import *
from fractions import *

def opOnMelody(op,arg,mel):
    return ukzOpMap[op](mel,arg)

def flattenMelody(noteDecoder,hm):
  mel = Melody()
  if isinstance(hm,MelLeaf):
    if hm.note == ".":
      mel.forward(1)
    else:
      note = noteDecoder[hm.note]
      mel.appendNote(note)
  elif isinstance(hm,MelNode):
    if hm.type == 0:
      # sequence
      for cmel in hm.childMelodies:
        cmelFlat = flattenMelody(noteDecoder,cmel)
        mel.appendMelody(cmelFlat)
    elif hm.type == 1:
      # parallel
      mellength = 0
      b = True
      for cmel in hm.childMelodies:
        cmelody = flattenMelody(noteDecoder,cmel)
        if b:
          mellength = cmelody.time
          b = False
        mel.addMelody(cmelody)
      mel.forward(mellength)
    else:
      raise ValueError('cannot flatten this thing, what the heck is this?')
  for (op,arg) in hm.operators:
    a = flattenMelody(noteDecoder,arg) \
     if isinstance(arg,Mel) else arg
    f = ukzOpMap.get(op,None)
    if f is None:
      mel.setProp(op[0:len(op)-1],a)
    else:
      ukzOpMap[op](mel,a)
  return mel
