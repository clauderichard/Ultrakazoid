from ukz.ukmelody import Melody,Event,Note,History

class MelOp:
  def __init__(self,func,argc):
    self.func = func
    self.argc = argc

# How to apply an operator to a (flat, not hierarchical) melody.
ukzMelodyUnOpMap = {
	 '¬': Melody.durationUntilEnd,
	 '^': Melody.transposeUp,
  'v': Melody.transposeDown
}
ukzMelodyOpMap = {
    '=': Melody.expandToEndTime,
    'x': History.repeat,
    'x=': History.repeatUntilEndTime,
    '~': Melody.pitchBendWithMelody,
    'o': Melody.volumeBendWithMelody,
    '<<': Melody.injectMelody,
    '<_': Melody.zipNoteDurations,
    '&': Melody.lock,
    #'¬': Melody.durationUntilEnd,
    '>': History.forward,
    '<': History.backward,
    '^': Melody.transposeUp,
    'v': Melody.transposeDown,
    '/': History.contract,
    '<^': Melody.chromUp
}

ukzMelodyForAllOpMap = {
  Melody.forAllTime: {
    '*': Event.expand,
    #'/': Event.contract,
  },
  Melody.forAllNotes: {
    '°': Note.setL,
    '_': Event.setD,
    '_*': Event.durExpand,
    '_/': Event.durContract,
    '_+': Event.durExtend,
    '_-': Event.durShorten,
    '+': Note.translateUp,
    '-': Note.translateDown,
    '$': Note.atScale1,
    '$$': Note.atScale2
  }
}

def opExists(op):
  if ukzMelodyUnOpMap.get(op,None) is not None:
    return True
  if ukzMelodyOpMap.get(op,None) is not None:
    return True
  for k,v in ukzMelodyForAllOpMap.items():
    if v.get(op,None) is not None:
      return True
  return False
def opGood(op):
  for k,_ in ukzMelodyUnOpMap.items():
    if k.startswith(op):
      return True
  for k,_ in ukzMelodyOpMap.items():
    if k.startswith(op):
      return True
  if ukzMelodyOpMap.get(op,None) is not None:
    return True
  for _,v in ukzMelodyForAllOpMap.items():
    for k,_ in v.items():
      if k.startswith(op):
        return True
  return False

def opFromStr(op,argc):
  if argc==0:
    f = ukzMelodyUnOpMap.get(op,None)
    if f is not None:
      return MelOp(f,0)
  elif argc==1:
    f = ukzMelodyOpMap.get(op,None)
    if f is not None:
      return MelOp(f,1)
    for g,evFuncs in \
     ukzMelodyForAllOpMap.items():
      f = evFuncs.get(op,None)
      if f is not None:
        return MelOp(lambda m,a: \
         g(m,f,a),argc)
    else:
      raise ValueError('argc too high')
    return None
