
from ukz.melody import \
 Fmel,Event,Note,History,Gradient,Scale
from ukz.hmel import \
 Hmel,HmelNote,HmelRest, \
 HmelSeq,HmelPar

def pitchBendHack(mel,a):
  mel.pitchBend = a.mapToBend(\
   Gradient.pitchBendTyp,-2,2,0,24)
  return mel
def volumeBendHack(mel,a):
  mel.volumeBend = a.mapToBend(\
   Gradient.pitchBendTyp,0,1,0,12)
  return mel

def toneExSc(tn,p):
  tn.p = p
def expandToScale(mel,a):
  ps = []
  for note in a.getFlattenedNotes():
    ps.append(note.p)
  sc = Scale(ps)
  return mel.forEachTone(lambda tn:
   toneExSc(tn,sc[tn.p]))
def filterToScale(mel,a):
  ps = [False]*12
  for note in a.getFlattenedNotes():
    ps[note.p] = True
  return mel.filterNotes(lambda n:
   ps[n.tone.p % 12])

# How to apply an operator to a Hmel.
ukzMelodyUnOpMap = {
  # Transpose is a separate special op now
	#'^': Hmel.transposeUp,
  #'v': Hmel.transposeDown,
  '¬': Hmel.durToEnd,
  '&': Hmel.lockP,
}
ukzMelodyOpMap = {
    'x': Hmel.repeat,
    'x=': Hmel.repeatUntil,
    '=': Hmel.expandTo,
    '°': Hmel.blendWithLoudness,
    '_': Hmel.setDur,
    '~': pitchBendHack,
    'o': volumeBendHack,
    # Transpose is a separate special op now
    #'^': Hmel.transposeUp,
    #'v': Hmel.transposeDown,
    '*': Hmel.expand,
    '/': Hmel.contract,
    '<$': expandToScale,
    '>$': filterToScale,
    '<<': Hmel.blowUpLeavesIntoMelody
}

# whether string op represents an operator or the start of one
def opGood(op):
  for k,_ in ukzMelodyUnOpMap.items():
    if k.startswith(op):
      return True
  for k,_ in ukzMelodyOpMap.items():
    if k.startswith(op):
      return True
  return False

# Get the function based on the op string
def opFromStr(op,argc):
  if argc==0:
    return ukzMelodyUnOpMap.get(op,None)
  elif argc==1:
    return ukzMelodyOpMap.get(op,None)
  else:
    raise ValueError('argc too high')
  return None
