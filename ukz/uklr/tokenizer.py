
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
        