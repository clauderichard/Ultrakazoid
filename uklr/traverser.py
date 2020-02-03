from uklr.tokenizer import TkToken,TkNode,TkAutomaton
from uklr.parser import PrRules

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
