from .tokenizer import TkAutomaton
from .parser import PrRules,PrRunner
from .traverser import Traverser
from .pat import seq,alt,star,plus

def get1st(x,*a):
  return x
def evenPositionedElmts(ls):
  b = True
  for x in ls:
    if b:
      yield x
    b = not b
def oddPositionedElmts(ls):
  b = False
  for x in ls:
    if b:
      yield x
    b = not b
def idlist(*a):
  return a

class LrProcessor:

  listTypeCounter = 1

  def __init__(self,emp,tk=None,pr=None,tr=None):
    self.tkAutomaton = tk if tk is not None else TkAutomaton(emp)
    self.tkPostProcessor = None
    self.prRules = pr if pr is not None else PrRules()
    self.traverseRules = tr if tr is not None else Traverser()
    
  def initialize(self):
    self.prRules.initialize()
    
  ################
  # Adding rules to tokenizer,parser,traverser

  def tkRule(self,fromNodeIndex,func,resultIndex):
      self.tkAutomaton.addTransition(fromNodeIndex,func,resultIndex)
      
  def prRule(self,\
   resultType,childrenTypes,\
   travFunc):
    self.prRules.addRule(resultType,\
     childrenTypes,travFunc)

  #def trRule(self,rootType,childrenTypes,func):
  #  self.traverseRules.addRule(rootType,childrenTypes,func)

  #def trLeafRule(self,rootType,func):
  #  self.traverseRules.addLeafRule(rootType,func)

  #def trPowerRule(self,rootType,allChildrenType,func):
  #  self.traverseRules.addPowerRule(rootType,allChildrenType,func)
    
  ################
  # Add parser and traverser rules at same time
  # (because they must match anyway)

  def prtrLeafRule(self,rootType,func):
    self.prRules.addLeafFunc(rootType,func)
    #self.traverseRules.addLeafRule(rootType,func)

  def prtrRule(self,resultType,\
   childrenTypes,\
   traverseFromChildrenFunc=get1st):
    self.prRule(resultType,childrenTypes,\
     traverseFromChildrenFunc)
    #self.trRule(resultType,childrenTypes,traverseFromChildrenFunc)

  def prtrDelimRule(self,\
   listType,elmtType,delimType,\
   elmtsToListFunc):
    travFunc = lambda a,bs: elmtsToListFunc( \
     [a] + list(map(lambda x: x[1], bs)))
    self.prtrRule(listType,\
     seq(elmtType,plus(seq(delimType,elmtType))), \
     travFunc)

  ################

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
    return parseTree.value
    # traverse
    traversed = self.traverseRules.traverse(parseTree)

    return traversed
