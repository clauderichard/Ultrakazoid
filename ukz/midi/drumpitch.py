
class DrumPitch:
    
  bassPedal = 1
  snare = 2
  
  hiHatOpen = 5
  hiHatClosed = 4
  hiHatClosed2 = 3
  
  splashCymbal = 7
  gong = 6
  cymbal1 = 8
  cymbal2 = 9
  
  rideCymbal1 = 10
  rideCymbal2 = 11
  rideBell = 12
  cowbell = 13
  
  floorTom1 = 14
  floorTom2 = 15
  tom1 = 16
  tom2 = 17
  tom3 = 18
  tom4 = 19
        
  metronomeClosed = 20
  metronomeOpen = 21
    
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
    metronomeOpen: 34
  }

  @classmethod
  def mapToMidi(cls,p):
    pp = cls.pitchMap.get(p,None)
    if pp is None:
      return p
    else:
      return pp
