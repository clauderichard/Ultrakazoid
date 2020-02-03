from ukz.ukmelody import \
 Melody,Event,Note
from .melodyopmap import *

class Mel:
  def __init__(self):
    self.operators = []
  def flatten(self,noteDecoder):
    mel = self.flattenWoOps(noteDecoder)
    for (op,arg) in self.operators:
      a = arg.flatten(noteDecoder) \
       if isinstance(arg,Mel) else arg
      if arg is None:
        mop = opFromStr(op,0)
        if mop is not None:
          mop.func(mel)
          continue
      mop = opFromStr(op,1)
      mop.func(mel,a)
    return mel
    
class MelLeaf(Mel):
  def __init__(self,note):
    Mel.__init__(self)
    self.note = note
  def applyOperator(self,opSymbol,opArg):
    if opSymbol[0] == '@':
      # too many @'s in the operator, but whatever.
      # Just ignore the @'s and move along.
      self.applyOperator(opSymbol[1:],opArg)
    elif opSymbol[0] == '!':
      self.operators.append((opSymbol[1:],opArg))
    else:
      self.operators.append((opSymbol,opArg))
  # partially copied from melodyflattener.py
  def flattenWoOps(self,noteDecoder):
    mel = Melody()
    if self.note == ".":
      mel.d += 1
    elif self.note != "|":
      note = noteDecoder[self.note]
      if isinstance(note,list):
        mel.insertNote(Note(note[0],mel.getEndTime()))
        for i in range(1,len(note)):
          newnote = Note(note[i],mel.getEndTime())
          newnote.locked = True
          mel.insertNote(newnote)
        mel.d += 1
      else:
        mel.appendNote(note)
    return mel

# You shouldn't have both childMelodies and leafNote.
class MelNode(Mel):
  def __init__(self,type,childMelodies):
    self.type = type
    self.childMelodies = childMelodies
    Mel.__init__(self)
  def applyOperator(self,opSymbol,opArg):
    if opSymbol[0] == '@':
      for c in self.childMelodies:
        c.applyOperator(opSymbol[1:],opArg)
    elif opSymbol[0] == '!':
      for c in self.childMelodies:
        c.applyOperator(opSymbol,opArg)
    else:
      self.operators.append((opSymbol,opArg))
  def flattenWoOps(self,noteDecoder):
    mel = Melody()
    if self.type == 0:
      # sequence
      startTime = 0
      b = True
      for cmel in self.childMelodies:
        cmelFlat = cmel.flatten(noteDecoder)
        if b:
          startTime = cmelFlat.t
          b = False
        mel.appendMelody(cmelFlat)
      dd = mel.t - startTime
      mel.t = startTime
      mel.d += dd
    elif self.type == 1:
      # parallel
      mellength = 0
      for cmel in self.childMelodies:
        cmelFlat = cmel.flatten(noteDecoder)
        mellength = cmelFlat.getEndTime()
        mel.insertMelody(cmelFlat)
      mel.d += mellength
    else:
      raise ValueError('cannot flatten this thing, what the heck is this?')
    return mel
    
################

class MelNodePiped(Mel):
  def __init__(self,type,melsL,melsR):
    self.type = type
    self.melsL = melsL
    self.melsR = melsR
    Mel.__init__(self)
  def applyOperator(self,opSymbol,opArg):
    if opSymbol[0] == '@':
      for c in self.melsL + self.melsR:
        c.applyOperator(opSymbol[1:],opArg)
    elif opSymbol[0] == '!':
      for c in self.melsL + self.melsR:
        c.applyOperator(opSymbol,opArg)
    else:
      self.operators.append((opSymbol,opArg))
  def flattenWoOps(self,noteDecoder):
    mel = Melody()
    if self.type == 0:
      # sequence
      startTime = 0
      backBy = 0
      b = True
      for cmel in self.melsL:
        cmelFlat = cmel.flatten(noteDecoder)
        if b:
          startTime = cmelFlat.t
          b = False
        mel.appendMelody(cmelFlat)
      backBy = mel.getEndTime()
      dd = mel.t - startTime
      mel.t = startTime
      mel.d += dd
      for cmel in self.melsR:
        cmelFlat = cmel.flatten(noteDecoder)
        mel.appendMelody(cmelFlat)
      mel.backward(backBy)
    elif self.type == 1:
      # parallel
      mellength = 0
      mellength2 = 0
      for cmel in self.melsL:
        cmelFlat = cmel.flatten(noteDecoder)
        mellength = cmelFlat.d
        cmelFlat.backward(\
         cmelFlat.getEndTime())
        mel.insertMelody(cmelFlat)
      for cmel in self.melsR:
        cmelFlat = cmel.flatten(noteDecoder)
        mellength2 = cmelFlat.getEndTime()
        mel.insertMelody(cmelFlat)
      mel.t = -mellength
      mel.d = mellength+mellength2
    else:
      raise ValueError('cannot flatten this thing, what the heck is this?')
    return mel
  
################
