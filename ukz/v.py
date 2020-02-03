
from ukz.u import *
from ukz.w import *
from ukz.pianopitchdecoder import *
from ukz.drumpitchdecoder import *

################

def tk(input):
    t = mkUkzTkAutomaton()
    if len(input)==0:
        input = "[C# DE *2 H°] @x4"
    tks = list(t.tokenize(input))
    print(input)
    print(tks)
    
################

def ukzParse(input):
    t = mkUkzTkAutomaton()
    tokens = t.tokenize(input)
    prRules = mkUkzPrRules()
    r = PrRunner(prRules)
    return r.parse(tokens)

################

def ukzGeneric(noteDecoder,input):
    inp = "[" + input + "]"

    # tokenize
    t = mkUkzTkAutomaton()
    tokens = t.tokenize(inp)
    
    # parse
    prRules = mkUkzPrRules()
    r = PrRunner(prRules)
    parseTree = r.parse(tokens)
    
    if isinstance(parseTree,list):
      for p in parseTree:
        print("another node...")
        p.printTree(UkzStates.stateStrings,2)
      raise "oops"
    
    # traverse
    hierarchicalMelody = traverseUkzTree(parseTree)
    
    # flatten
    melody = flattenHierarchicalMelody(noteDecoder,hierarchicalMelody)
    
    return melody

def ukz(input):
    return ukzGeneric(PianoPitchDecoder.getSingleton(),input)
def ukd(input):
    return ukzGeneric(DrumPitchDecoder.getSingleton(),input)

################

def pr(input=None):
    if input is None:
        input = "([CD*7]*8)"
    print('input = ',input,sep='')
    #stack = ukzParse(input)
    
    t = mkUkzTkAutomaton()
    tokens = t.tokenize(input)
    
    prRules = mkUkzPrRules()
    r = PrRunner(prRules)
    stack = r.parse(tokens)
    
    mel = None
    if isinstance(stack,list):
        print('Parsed result list:')
        for node in stack:
            node.printTree(UkzStates.stateStrings,4)
    else:
        print('Parsed result:')
        stack.printTree(UkzStates.stateStrings,4)
        mel = traverseUkzTree(stack)
    
    if mel is not None:
        print('Traversed result:')
        mel.printTree(0)
    else:
        print('Traversing returned nothing. Womp womp. Here is the parse tree before traversing.')
        stack.printTree(UkzStates.stateStrings,4)
        
    if mel is None:
        return
    
    melody = flattenHierarchicalMelody(DrumPitchDecoder.getSingleton(),mel)
    print(melody)
    for n in melody.notes:
        print(n)

################

#pr("[ (bs)*5 [bc]*2 C ] @@x3 ")
