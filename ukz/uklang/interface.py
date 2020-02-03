
from .tokenrules import mkUkzTkAutomaton
from .parserules import mkUkzPrRules
from .traverserules import mkUkzTraverser
from ..uklr.processor import LrProcessor
#from .melodyflattener import flattenMelody
from .pianopitchdecoder import PianoPitchDecoder
from .drumpitchdecoder import DrumPitchDecoder
from .tkpostprocessor import processToken

################

# def tk(input):
#     t = mkUkzTkAutomaton()
#     if len(input)==0:
#         input = "[C# DE *2 h^] @x4"
#     tks = list(t.tokenize(input))
#     print(input)
#     print(tks)
    
################

# def ukzParse(input):
#     t = mkUkzTkAutomaton()
#     tokens = t.tokenize(input)
#     prRules = mkUkzPrRules()
#     r = PrRunner(prRules)
#     return r.parse(tokens)

################

def ukzGeneric(noteDecoder,input):
    # config for uklr processor
    inp = "[" + input + "]"
    tkRules = mkUkzTkAutomaton()
    prRules = mkUkzPrRules()
    travRules = mkUkzTraverser()

    # process
    p = LrProcessor(tkRules,prRules,travRules)
    p.tkPostProcessor = processToken
    hierarchicalMelody = p.process(inp)
    # flatten
    melody = hierarchicalMelody\
     .flatten(noteDecoder)
    
    melody.preen()
    return melody

def ukz(input):
    return ukzGeneric(PianoPitchDecoder.getSingleton(),input)
def ukd(input):
    return ukzGeneric(DrumPitchDecoder.getSingleton(),input)
