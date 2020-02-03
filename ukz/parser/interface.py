
from ukz.parser.tokenrules import mkUkzTkAutomaton
from ukz.parser.parserules import mkUkzPrRules
from ukz.parser.traverserules import mkUkzTraverser
from uklr.processor import processUklr
from ukz.parser.melodyflattener import flattenMelody
from ukz.parser.pianopitchdecoder import PianoPitchDecoder
from ukz.parser.drumpitchdecoder import DrumPitchDecoder

################

# def tk(input):
#     t = mkUkzTkAutomaton()
#     if len(input)==0:
#         input = "[C# DE *2 H°] @x4"
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
    hierarchicalMelody = processUklr(inp,tkRules,prRules,travRules)
    # flatten
    melody = flattenMelody(noteDecoder,hierarchicalMelody)
    
    return melody

def ukz(input):
    return ukzGeneric(PianoPitchDecoder.getSingleton(),input)
def ukd(input):
    return ukzGeneric(DrumPitchDecoder.getSingleton(),input)
