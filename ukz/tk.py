
################

# Tokenizer

class TkToken:
    def __init__(self,type,value):
        self.type = type
        self.value = value

# Node in a tokenizer's automaton
class TkNode:
    def __init__(self,defaultResult):
        self.transitions = []
        self.defaultResult = defaultResult
    def addTransition(self,func,result):
        f = func
        if isinstance(func,str):
            f = lambda x : x in func
        self.transitions.append((f,result))
    def getNext(self,input):
        for (f,r) in self.transitions:
            if f(input):
                return r
        return self.defaultResult
        
# Automaton for tokenizing
# Going to the empty node means your token is done,
# if there's a token built up in the first place.
class TkAutomaton:
    def __init__(self,emptyNodeIndex):
        self.emptyNodeIndex = emptyNodeIndex
        self.nodes = {emptyNodeIndex: TkNode(self.emptyNodeIndex)}
    def nodeExists(self,index):
        return self.nodes.get(index,None) is not None
    def getNode(self,index):
        if not self.nodeExists(index):
            self.nodes[index] = TkNode(self.emptyNodeIndex)
        return self.nodes[index]
    def addTransition(self,fromNodeIndex,func,resultIndex):
        self.getNode(fromNodeIndex).addTransition(func,resultIndex)
    def getNext(self,fromNodeIndex,input):
        return self.getNode(fromNodeIndex).getNext(input)
    def tokenize(self,string):
        nodeIndex = self.emptyNodeIndex
        acc = ""
        for input in string:
            nx = self.getNext(nodeIndex,input)
            if nx == self.emptyNodeIndex:
                if nodeIndex != self.emptyNodeIndex:
                  yield TkToken(nodeIndex,acc)
                acc = ""
                nodeIndex = self.emptyNodeIndex
                nx = self.getNext(nodeIndex,input)
            if nx != self.emptyNodeIndex:
                acc = acc + input
            nodeIndex = nx
        if len(acc) > 0 and nodeIndex != self.emptyNodeIndex:
            yield TkToken(nodeIndex,acc)
        
################

# Parser node types (only generic ones included here)
BOF = -2
EOF = -1

def tokensWithEnds(tokens):
    yield TkToken(BOF,None)
    for t in tokens:
        yield t
    yield TkToken(EOF,None)

class PrRule:
    def __init__(self,resultType,childrenTypes,blacklistForNext=[],whitelistForNext=[],isAdoption=False):
        self.left = resultType
        self.right = childrenTypes
        self.blacklistForNext = blacklistForNext
        self.whitelistForNext = whitelistForNext
        self.isAdoption = isAdoption

class PrRules:
    def __init__(self):
        self.rules = []
    def addRule(self,resultType,childrenTypes,blacklistForNext=[],whitelistForNext=[],isAdoption=False):
        rightR = childrenTypes
        if not isinstance(childrenTypes,list):
            rightR = [childrenTypes]
        rightR = list(rightR)
        newRule = PrRule(resultType,rightR,blacklistForNext,whitelistForNext,isAdoption)
        self.rules.append(newRule)
    def addAdoptionRule(self,resultType,childrenTypes,blacklistForNext=[],whitelistForNext=[]):
        if len(childrenTypes) != 2:
            raise ValueError('adoption rule must have 2 items on the right')
        self.addRule(resultType,childrenTypes,blacklistForNext,whitelistForNext,True)
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
        if r.isAdoption:
            oldChildren = self.stack[1].children
            newChildren = oldChildren + self.stack[0:1]
            newNode = PrNode(TkToken(r.left,None),newChildren)
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

################

# Traverser
# Used to traverse a parse tree to build an object out of it

# A simple rule for a traverser.
# If a parse tree looks like (rootType in root, childrenTypes for child types),
# then you must traverse the children first to get an array C of child traversed objects, 
# then apply this rule's func with C as argument, to get the parent node's traversed object.
class TraverserRule:
    def __init__(self,rootType,childrenTypes,func):
        self.rootType = rootType
        self.childrenTypes = childrenTypes
        self.func = func
    def nodeMatches(self,node):
        if self.rootType != node.root.type:
            return False
        if len(self.childrenTypes) != len(node.children):
            return False
        for (ruleT,cNode) in zip(self.childrenTypes,node.children):
            if ruleT != cNode.root.type:
                return False
        return True

# Like a rule, but the children are just an array of uncertain length
# but the children must be all the same type.
class TraverserPowerRule:
    def __init__(self,rootType,allChildrenType,func):
        self.rootType = rootType
        self.allChildrenType = allChildrenType
        self.func = func
    def nodeMatches(self,node):
        if self.rootType != node.root.type:
            return False
        for cNode in node.children:
            if self.allChildrenType != cNode.root.type:
                return False
        return True

# Not really necessary I think...
# You can get this by combining a Rule with a PowerRule, I think. Maybe not always.
class TraverserPowerRule2:
    def __init__(self,rootType,childrenTypes,childIndex,allGrandChildrenType,func):
        self.rootType = rootType
        self.childrenTypes = childrenTypes
        self.childIndex = childIndex
        self.allGrandChildrenType = allGrandChildrenType
        self.func = func
    def nodeMatches(self,node):
        if self.rootType != node.root.type:
            return False
        if len(self.childrenTypes) != len(node.children):
            return False
        for (ruleT,cNode) in zip(self.childrenTypes,node.children):
            if ruleT != cNode.root.type:
                return False
        cNode = node.children[self.childIndex]
        for gcNode in cNode.children:
            if self.allGrandChildrenType != gcNode.root.type:
                return False
        return True

# Construct this object, add rules to it,
# and then you can traverse with a parse tree as an argument, and get an object!
class Traverser:
    def __init__(self):
        self.leafRules = []
        self.rules = []
        self.powerRules = []
        self.powerRules2 = []
    def addRule(self,rootType,childrenTypes,func):
        rule = TraverserRule(rootType,childrenTypes,func)
        self.rules.append(rule)
    def addLeafRule(self,rootType,func):
        rule = TraverserRule(rootType,[],func)
        self.leafRules.append(rule)
    def addPowerRule(self,rootType,allChildrenType,func):
        rule = TraverserPowerRule(rootType,allChildrenType,func)
        self.powerRules.append(rule)
    def addPowerRule2(self,rootType,childrenTypes,childIndex,allGrandChildrenType,func):
        rule = TraverserPowerRule2(rootType,childrenTypes,childIndex,allGrandChildrenType,func)
        self.powerRules2.append(rule)
    def traverse(self,node):
        if len(node.children) == 0:
            for rule in self.leafRules:
                if rule.nodeMatches(node):
                    mappedNode = rule.func(node.root.value)
                    return mappedNode
        for rule in self.rules:
            if rule.nodeMatches(node):
                mappedChildren = list(map(lambda c: self.traverse(c), node.children))
                mappedParent = rule.func( *mappedChildren )
                return mappedParent
        for powerRule in self.powerRules:
            if powerRule.nodeMatches(node):
                mappedChildren = list(map(lambda c: self.traverse(c), node.children))
                mappedParent = powerRule.func( mappedChildren )
                return mappedParent
        for powerRule2 in self.powerRules2:
            if powerRule2.nodeMatches(node):
                childNode = node.children[powerRule2.childIndex]
                mappedGrandChildren = list(map(lambda c: self.traverse(c), childNode.children))
                mappedChild = rule.func( mappedGrandChildren )
                return mappedChild
        # no rule found. This is reached for brackets and stupid things.
        return None
