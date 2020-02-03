from .tokenizer import TkToken

# Parser node types (only generic ones included here)
BOF = -2
EOF = -1

def tokensWithEnds(tokens):
    yield TkToken(BOF,None)
    for t in tokens:
        yield t
    yield TkToken(EOF,None)

class PrRuleType:
  REDUCE = 0
  ADOPT = 1
  GEN = 2

class PrRule:
    def __init__(self,resultType,\
    	childrenTypes,\
    	blacklistForNext=[],\
    	whitelistForNext=[],\
    	typ=0):
        self.left = resultType
        self.right = childrenTypes
        self.blacklistForNext = blacklistForNext
        self.whitelistForNext = whitelistForNext
        self.typ = typ

class PrRules:
  def __init__(self):
    self.rules = []
  def addRule(self,\
   resultType,childrenTypes,\
   blacklistForNext=[],\
   whitelistForNext=[]):
    rightR = childrenTypes
    if not isinstance(childrenTypes,list):
      rightR = [childrenTypes]
    rightR = list(rightR)
    newRule = PrRule(\
    	resultType,rightR,\
    	blacklistForNext,\
    	whitelistForNext,\
    	PrRuleType.REDUCE)
    self.rules.append(newRule)
  def addGenRule(self,\
   newType,stackTypes,\
   blacklistForNext=[],\
   whitelistForNext=[]):
    rightR = stackTypes
    if not isinstance(stackTypes,list):
      rightR = [stackTypes]
    rightR = list(rightR)
    newRule = PrRule(\
    	newType,rightR,\
    	blacklistForNext,\
    	whitelistForNext,\
    	PrRuleType.GEN)
    self.rules.append(newRule)
  def addAdoptionRule(self,resultType,childrenTypes,blacklistForNext=[],whitelistForNext=[]):
    if len(childrenTypes) != 2:
      raise ValueError('adoption rule must have 2 items on the right')
    rightR = childrenTypes
    if not isinstance(childrenTypes,list):
      rightR = [childrenTypes]
    rightR = list(rightR)
    newRule = PrRule(\
    	resultType,rightR,\
    	blacklistForNext,\
    	whitelistForNext,\
    	PrRuleType.ADOPT)
    self.rules.append(newRule)
  def ruleMatchesStack(self,stack,rule,nextInput):
    if len(stack) < len(rule.right):
      return False
    # If lookahead makes the rule not apply just yet
    if len(rule.whitelistForNext) > 0 \
     and nextInput is not None \
     and nextInput.type not in rule.whitelistForNext:
      return False
    if nextInput is not None and nextInput.type in rule.blacklistForNext:
      return False
    for (t,r) in zip(stack,reversed(rule.right)):
      if t.root.type != r:
        return False
    return True
  def findRuleForStack(self,stack,nextInput):
    for r in self.rules:
      if self.ruleMatchesStack(stack,r,nextInput):
        return r
    return None

class PrNode:
    def __init__(self,root,children=[]):
        self.root = root
        self.children = children
        if not isinstance(self.children,list):
            self.children = [self.children]
    def printTree(self,stateStrings,tabN=0):
        if self.root.value is None:
            print(' '*tabN,stateStrings.get(self.root.type,'|'),sep='')
        else:
            #print(' '*tabN,self.root)
            print(' '*tabN,stateStrings.get(self.root.type,''),' ',self.root.value,sep='')
        for c in self.children:
            c.printTree(stateStrings,tabN+4)
def mkPrLeaf(token):
    return PrNode(token)

class PrRunner:
    def __init__(self,prRules):
        self.prRules = prRules
        self.stack = []
        self.inputs = iter([None])
        self.nextInput = next(self.inputs)
    def initialize(self,tokens):
        self.stack = []
        self.inputs = iter(tokens)
        self.nextInput = next(self.inputs)
    def tryShift(self):
        if self.nextInput is None:
            return False
        newLeaf = PrNode(self.nextInput)
        self.stack.insert(0,newLeaf)
        try:
            self.nextInput = next(self.inputs)
        except StopIteration:
            self.nextInput = None
        return True
    def canReduce(self):
        r = self.prRules.findRuleForStack(self.stack,self.nextInput)
        return r is not None
    def doReduce(self,r):
        n = len(r.right)
        newNode = None
        if r.typ == PrRuleType.ADOPT:
            oldChildren = self.stack[1].children
            newChildren = oldChildren + self.stack[0:1]
            newNode = PrNode(TkToken(r.left,None),newChildren)
            del self.stack[0:n]
            self.stack.insert(0,newNode)
        elif r.typ == PrRuleType.GEN:
            newNode = PrNode(TkToken(r.left,None),[])
            self.stack.insert(0,newNode)
        else:
            newChildren = list(reversed(self.stack[0:n]))
            newNode = PrNode(TkToken(r.left,None),newChildren)
            del self.stack[0:n]
            self.stack.insert(0,newNode)
    def tryReduce(self):
        r = self.prRules.findRuleForStack(self.stack,self.nextInput)
        if r is None:
            return False
        else:
            self.doReduce(r)
            return True
    def parse(self,tokens):
        self.initialize(tokensWithEnds(tokens))
        while True:
            if not self.tryReduce():
                if not self.tryShift():
                    break
        if len(self.stack) == 3:
            return self.stack[1]
        else:
            print('not fully parsed! Uh oh...')
            return self.stack
