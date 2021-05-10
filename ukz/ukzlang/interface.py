
from ukz.uklr import LrProcessor
# from .tokenrules import fillUkzTkRules
from .ukzgrammar import fillUkzPrTrRules,fillUkzTkRules,addukzlangSymbols
from .pitchdecoder import PitchDecoder
# from .ukzlangsymbols import addukzlangSymbols
from .skzgrammar import fillSkzPrTrRules,fillSkzTkRules

class SkzProcessor:
    p = None
class UkzProcessor:
    p = None

def buildUkzParser():
    # config for uklr processor
    PitchDecoder.init() # must be called before parsing.
    UkzProcessor.p = LrProcessor()
    addukzlangSymbols(UkzProcessor.p)
    fillUkzTkRules(UkzProcessor.p)
    fillUkzPrTrRules(UkzProcessor.p)
    
def buildSkzParser():
    # config for uklr processor
    SkzProcessor.p = LrProcessor()
    fillSkzTkRules(SkzProcessor.p)
    fillSkzPrTrRules(SkzProcessor.p)
    
################################

buildSkzParser()
buildUkzParser()

################################
def ukz(code):
    hmel = UkzProcessor.p.process(f"《{code}》")
    melody = hmel.flatten()
    melody.sortNotes()
    return melody

def skz(code):
    x = SkzProcessor.p.process(f"[{code}]")
    return x
################################
