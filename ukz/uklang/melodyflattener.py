
#from .traverserules import *
from .hiermelody import Mel,MelLeaf,MelNode
from ukz.ukmelody import Melody,Event,Note
from .melodyopmap import \
 ukzMelodyOpMap,\
 ukzMelodyForAllOpMap
#from .states import *
#from fractions import *

def flattenMelody(noteDecoder,hm):
  mel = Melody()
  if isinstance(hm,MelLeaf):
    if hm.note == ".":
      mel.time += 1
    elif hm.note != "|":
      note = noteDecoder[hm.note]
      if isinstance(note,list):
        mel.insertNote(Note(note[0],mel.time))
        for i in range(1,len(note)):
          newnote = Note(note[i],mel.time)
          newnote.locked = True
          mel.insertNote(newnote)
        mel.time += 1
      else:
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
        cmelFlat = flattenMelody(noteDecoder,cmel)
        if b:
          mellength = cmelFlat.time
          b = False
        mel.insertMelody(cmelFlat)
      mel.time += mellength
    else:
      raise ValueError('cannot flatten this thing, what the heck is this?')
  for (op,arg) in hm.operators:
    a = flattenMelody(noteDecoder,arg) \
     if isinstance(arg,Mel) else arg
    f = ukzMelodyOpMap.get(op,None)
    if f is not None:
      f(mel,a)
      continue
    b = False
    for melForFunc,evFuncs in \
     ukzMelodyForAllOpMap.items():
      f = evFuncs.get(op,None)
      if f is not None:
        melForFunc(mel,f,a)
        b = True
        break
    if b:
      continue
    if op[len(op)-1] != '=':
      raise ValueError('unsupported operator')
    mel.forAllEvents(Event.setProp,op[0:len(op)-1],a)
  return mel
