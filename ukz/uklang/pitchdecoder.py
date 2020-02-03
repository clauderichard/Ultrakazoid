from ukz.midi import DrumPitch
  
class PitchDecoder:

  def __init__(self):
    self.pitchmap = {}
    
  def isCaps(self,s):
    return ord('A') <= ord(s) \
      and ord('Z') >= ord(s)
  def isDigit(self,s):
    return ord('0') <= ord(s) \
      and ord('9') >= ord(s)

  def applyCap(self,p):
    return p+12

  def pitchTrans_h(self,p,trans,i):
    if trans=='' and i=='':
      return p
    ud = 1 if trans=='^' else -1 if trans=='v' else 12
    n = 1 if i=='' else int(i)
    return p + ud*n

  def pitchTransposes(self,p,code):
    trans = ''
    i = ''
    for o in code[1:] + '.':
      tra = o=='^' or o=='v'
      dig = self.isDigit(o)
      if dig:
        i += o
      elif tra and trans=='' and i=='':
        trans += o
      else:
        p = self.pitchTrans_h(p,trans,i)
        trans = o if tra else ''
        i = o if dig else ''
    return p

  def __getitem__(self,code):
    c = code[0]
    p = self.pitchmap.get(c.lower(),None)
    if p is None:
      raise ValueError(f"Char '{c}' is not supported in non-drum notes")
    p = self.pitchTransposes(p,code)
    if self.isCaps(c):
      p = self.applyCap(p)
    return p


class PianoPitchDecoder(PitchDecoder):
  instance = None
  @classmethod
  def getSingleton(cls):
    if cls.instance is None:
      cls.instance = cls()
    return cls.instance

  def __init__(self):
    self.pitchmap = {
      "c": 0,
      "d": 2,
      "e": 4,
      "f": 5,
      "g": 7,
      "a": 9,
      "b": 11,
    }

        
class DrumPitchDecoder(PitchDecoder):
  instance = None
  @classmethod
  def getSingleton(cls):
    if cls.instance is None:
      cls.instance = cls()
    return cls.instance

  def __init__(self):
    self.pitchmap = {
      "c": DrumPitch.cymbal1,
      "d": 2,
      "e": 4,
      "f": DrumPitch.floorTom1,
      "g": DrumPitch.gong,
      "a": 9,
      "b": DrumPitch.bassPedal,
      "s": DrumPitch.snare,
      "h": DrumPitch.hiHatClosed,
      "r": DrumPitch.rideCymbal1,
      "l": DrumPitch.rideBell,
      "t": DrumPitch.tom1,
      "u": DrumPitch.tom3,
      "m": DrumPitch.metronomeClosed,
      "j": DrumPitch.jingleBell,
    }
