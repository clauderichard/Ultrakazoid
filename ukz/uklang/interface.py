
from .states import EMPTY
from ukz.uklr import TkAutomaton,PrRules,Traverser,LrProcessor
from .tokenrules import TkAutomaton,fillUkzTkRules
from .parserules import UkzTraverser,fillUkzPrTrRules
#from .melodyflattener import flattenMelody
from .pitchdecoder import PianoPitchDecoder,DrumPitchDecoder

class UkzProcessor:
  p = None

def buildUkParser():
  #print("build parser begin")
  # config for uklr processor
  tkRules = TkAutomaton(EMPTY)
  prRules = PrRules()
  travRules = Traverser()
  p = LrProcessor(EMPTY,tkRules,prRules,travRules)

  fillUkzTkRules(p)
  fillUkzPrTrRules(p)
  p.initialize()
  UkzProcessor.p = p
  #print("build parser done")
  
buildUkParser()

def ukzGeneric(noteDecoder,input):
    
    # process
    inp = "[" + input + "]"
    UkzTraverser.g_noteDecoder = noteDecoder
    hmel = UkzProcessor.p.process(inp)
    # flatten
    melody = hmel\
     .flatten()
    
    melody.preen()
    return melody

def ukz(input):
    return ukzGeneric(PianoPitchDecoder.getSingleton(),input)
def ukd(input):
    return ukzGeneric(DrumPitchDecoder.getSingleton(),input)
