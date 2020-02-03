from .tokenizer import TkAutomaton
from .parser import PrRules,PrRunner
from .traverser import Traverser

class LrProcessor:
  def __init__(self,tk,pr,tr):
    self.tkAutomaton = tk
    self.tkPostProcessor = None
    self.prRules = pr
    self.traverseRules = tr
  def process(self,input):
    # tokenize
    tokens = self.tkAutomaton\
     .tokenize(input)
    # process tokens
    if self.tkPostProcessor is not None:
      tokens = map(self.tkPostProcessor,\
       tokens)
    # parse
    r = PrRunner(self.prRules)
    parseTree = r.parse(tokens)
    
    if isinstance(parseTree,list):
      raise Exception("Could not fully parse the code!")
    # traverse
    traversed = self.traverseRules.traverse(parseTree)

    return traversed
