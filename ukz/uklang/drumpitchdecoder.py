from ukz.midi import DrumPitch

class DrumPitchDecoder:
  capsExtraPitch = DrumPitch.bassPedal
    
  instance = None

  def __init__(self):
    self.pitchmap = {}
        
    self.mapchar("b",DrumPitch.bassPedal)
    self.mapchar("s",DrumPitch.snare)
    self.mapchar("h",DrumPitch.hiHatClosed)
    self.mapchar("c",DrumPitch.cymbal1)
    self.mapchar("r",DrumPitch.rideCymbal1)
    self.mapchar("g",DrumPitch.gong)
    self.mapchar("l",DrumPitch.rideBell)
        
    self.mapchar("f",DrumPitch.floorTom1)
    self.mapchar("t",DrumPitch.tom1)
    self.mapchar("u",DrumPitch.tom3)
        
    self.mapchar("m",33)
    self.mapchar("j",DrumPitch.jingleBell)
        
  @classmethod
  def getSingleton(cls):
    if cls.instance is None:
      cls.instance = cls()
    return cls.instance
        
  def mapchar(self,string,pitch):
    self.pitchmap[string] = pitch
        
  # Returns an array of pitch numbers, because
  # there might be an extra bass pedal with it.
  def __getitem__(self,string):
    c = ord(string[0])
    iscaps = c >= ord('A') and c <= ord('Z')
    s = string.lower()
    # if iscaps then we'll add the extra pitch.
    p = self.pitchmap[s]
    return [p,DrumPitchDecoder.capsExtraPitch] if iscaps else [p]
        