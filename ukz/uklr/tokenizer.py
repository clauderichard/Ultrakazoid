
class TkToken:
  def __init__(self,type,value):
    self.type = type
    self.value = value
  def __str__(self):
    return f"(type={self.type},value={self.value})"
  def __repr__(self):
    return str(self)

# Node in a tokenizer's automaton
class TkNode:
    def __init__(self,defaultResult):
        self.transitions = []
        self.defaultResult = defaultResult
    def addTransition(self,func,result):
        f = func
        if isinstance(func,str):
            f = lambda x,y : y in func
        self.transitions.append((f,result))
    def getNext(self,acc,input):
        for (f,r) in self.transitions:
            if f(acc,input):
                return r
        return self.defaultResult
        
# Automaton for tokenizing
# Going to the empty node means your token is done,
# if there's a token built up in the first place.
class TkAutomaton:
    def __init__(self,emptyNodeIndex):
        self.emptyNodeIndex = emptyNodeIndex
        self.nodes = {emptyNodeIndex: TkNode(self.emptyNodeIndex)}
        self.ws = set([' ','\n','\r','\t'])
    def nodeExists(self,index):
        return self.nodes.get(index,None) is not None
    def getNode(self,index):
        if not self.nodeExists(index):
            self.nodes[index] = TkNode(self.emptyNodeIndex)
        return self.nodes[index]
    def addTransition(self,fromNodeIndex,func,resultIndex):
        self.getNode(fromNodeIndex).addTransition(func,resultIndex)
    def getNext(self,fromNodeIndex,acc,input):
        return self.getNode(fromNodeIndex).getNext(acc,input)
    def tokenize(self,string):
        nodeIndex = self.emptyNodeIndex
        acc = ""
        for input in string:
            nx = self.getNext(nodeIndex,acc,input)
            if nx == self.emptyNodeIndex:
                if nodeIndex != self.emptyNodeIndex:
                  yield TkToken(nodeIndex,acc)
                elif input not in self.ws:
                  raise Exception("Unexpected character")
                acc = ""
                nodeIndex = self.emptyNodeIndex
                nx = self.getNext(nodeIndex,acc,input)
                if nx == self.emptyNodeIndex and input not in self.ws:
                  raise Exception("Unexpected character")
            if nx != self.emptyNodeIndex:
                acc = acc + input
            nodeIndex = nx
        if len(acc) > 0 and nodeIndex != self.emptyNodeIndex:
            yield TkToken(nodeIndex,acc)
        