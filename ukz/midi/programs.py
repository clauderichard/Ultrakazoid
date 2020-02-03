
from ..utils import StringMatcher

class Programs(StringMatcher):
    
  def __init__(self):
    StringMatcher.__init__(self)
    # todo complete the list
    # of 127 programs
    self.vals = {
     'acoustic grand piano': 0,
     'bright acoustic piano': 1,
     'electric grand piano': 2,
     'honkyT tonk piano': 3,
     'electric piano 1': 4,
     'electric piano 2': 5,
     'harpsichord': 6,
     'clavinet': 7,
     
     'celesta': 8,
     'glockenspiel': 9,
     'music box': 10,
     'vibraphone': 11,
     'marimba': 12,
     'xylophone': 13,
     'tubular bells': 14,
     'dulcimer': 15,

     'drawbar organ': 16,
     'percussive organ': 17,
     'rock organ': 18,
     'church organ': 19,
     'reed organ': 20,
     'accordion': 21,
     'harmonica': 22,
     'tango accordion': 23,
     
     'acoustic guitar nylon': 24,
     'acoustic guitar steel': 25,
     'electric guitar jazz': 26,
     'electric guitar clean': 27,
     'electric guitar muted': 28,
     'overdriven guitar': 29,
     'distortion guitar': 30,
     'guitar harmonics': 31,
     
     'acoustic bass': 32,
     'electric bass finger': 33,
     'electric bass pick': 34,
     'fretless bass': 35,
     'slap bass 1': 36,
     'slap bass 2': 37,
     'synth bass 1': 38,
     'synth bass 2': 39,

     'violin': 40,
     'viola': 41,
     'cello': 42,
     'contrabass': 43,
     'tremolo strings': 44,
     'pizzicato strings': 45,
     'orchestral harp': 46,
     'timpani': 47,
     
     'string ensemble 1': 48,
     'string ensemble 2': 49,
     'synth strings 1': 50,
     'synth strings 2': 51,
     'choir aahs': 52,
     'voice oohs': 53,
     'synth choir': 54,
     'orchestra hit': 55,
     
     'trumpet': 56,
     'trombone': 57,
     'tuba': 58,
     'muted trumpet': 59,
     'french horn': 60,
     'brass section': 61,
     'synth brass 1': 62,
     'synth brass 2': 63,
     
     'soprano sax': 64,
     'alto sax': 65,
     'tenor sax': 66,
     'baritone sax': 67,
     'oboe': 68,
     'englishHorn': 69,
     'bassoon': 70,
     'clarinet': 71,

     'piccolo': 72,
     'flute': 73,
     'recorder': 74,
     'pan flute': 75,
     'blown bottle': 76,
     'shakuhachi': 77,
     'whistle': 78,
     'ocarina': 79,

     'lead 1 square': 80,
     'lead 2 sawtooth': 81,
     'lead 3 calliope': 82,
     'lead 4 chiff': 83,
     'lead 5 charang': 84,
     'lead 6 voice': 85,
     'lead 7 fifths': 86,
     'lead 8 bass lead': 87,

     'pad 1 new age': 88,
     'pad 2 warm': 89,
     'pad 3 polysynth': 90,
     'pad 4 choir': 91,
     'pad 5 bowed': 92,
     'pad 6 metallic': 93,
     'pad 7 halo': 94,
     'pad 8 sweep': 95,

     'fx 1 rain': 96,
     'fx 2 soundtrack': 97,
     'fx 3 crystal': 98,
     'fx 4 atmosphere': 99,
     'fx 5 brightness': 100,
     'fx 6 goblins': 101,
     'fx 7 echoes': 102,
     'fx 8 scifi': 103,

     'sitar': 104,
     'banjo': 105,
     'shamisen': 106,
     'koto': 107,
     'kalimba': 108,
     'bagpipe': 109,
     'fiddle': 110,
     'shanai': 111,

     'tinkle bell': 112,
     'agogo': 113,
     'steel drums': 114,
     'wood block': 115,
     'taiko drum': 116,
     'melodic tom': 117,
     'synth drum': 118,
     'reverse cymbal': 119,
     
     'guitar fret noise': 120,
     'breath noise': 121,
     'seashore': 122,
     'bird tweet': 123,
     'telephone ring': 124,
     'helicopter': 125,
     'applause': 126,
     'gunshot': 127

    }

class DrumKits(StringMatcher):

  def __init__(self):
    StringMatcher.__init__(self)
    self.vals = {
      'standard': 0,
      'room': 8,
      'power': 16,
      'electric': 24,
      'rap': 25,
      'jazz': 32,
      'brush': 40
    }

programs = Programs()
drumKits = DrumKits()
