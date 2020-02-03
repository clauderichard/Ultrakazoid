from uklr.tokenizer import TkAutomaton
from uklr.parser import PrRules,PrRunner
from uklr.traverser import Traverser

def processUklr(input,tkAutomaton,prRules,traverserules):
    # tokenize
    tokens = tkAutomaton.tokenize(input)
    
    # parse
    r = PrRunner(prRules)
    parseTree = r.parse(tokens)
    
    if isinstance(parseTree,list):
      raise Exception("Could not fully parse the code!")
    
    # traverse
    traversed = traverserules.traverse(parseTree)

    return traversed
