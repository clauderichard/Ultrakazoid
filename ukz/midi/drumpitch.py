
class DrumPitch:
    
  ################################
  # Overlaps with piano letters

  cymbal1 = 0 # c
  cymbal2 = 1 # c^
  floorTom1 = 5 # f
  floorTom2 = 6 # f^
  gong = 7 # g
  splashCymbal = 8 # g^
  bassPedal = 11 # b

  ################################

  snare = 24
  
  hiHatClosed2 = 26
  hiHatClosed = 27
  hiHatOpen = 28
  
  rideCymbal1 = 41
  rideCymbal2 = 42
  rideBell = 43
  cowbell = 44
  
  tom1 = 45
  tom2 = 46
  tom3 = 47
  tom4 = 48
        
  metronomeClosed = 61
  metronomeOpen = 62
  
  jingleBell = 63
  bellTree = 64
    
  pitchMap = {
    bassPedal: 36,
    snare: 38,
    hiHatOpen: 46,
    hiHatClosed: 42,
    hiHatClosed2: 44,
    splashCymbal: 55,
    gong: 52,
    cymbal1: 49,
    cymbal2: 57,
    rideCymbal1: 59,
    rideCymbal2: 51,
    rideBell: 53,
    cowbell: 56,
    floorTom1: 41,
    floorTom2: 43,
    tom1: 45,
    tom2: 47,
    tom3: 48,
    tom4: 50,
    metronomeClosed: 33,
    metronomeOpen: 34,
    jingleBell: 83,
    bellTree: 84
  }

  @classmethod
  def mapToMidi(cls,p):
    pp = cls.pitchMap.get(p,None)
    if pp is None:
      pp = cls.pitchMap.get(p-12,None)
      if pp is None:
        return p
      else:
        return [36,pp]
    else:
      return pp
