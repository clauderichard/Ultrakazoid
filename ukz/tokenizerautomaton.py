
class TokenizerAutomaton:
    
    def __init__(self):
        self.nodes = [{}]
    
    def tryGetNext(self,node,c):
        return node.get(c,None)
    
    def hasNext(self,node,c):
        return self.tryGetNext(\
        	node,c) is not None 
    
    def symbolMayExist(self,w):
        #print('mayexist ',w)
        node = self.nodes[0]
        for s in w:
            c = ord(s)
            nn = node.get(c,None)
            if nn is not None:
                node = nn
            else:
                return False
        return True
    
    def addWord(self,w):
        node = self.nodes[0]
        for s in w:
            c = ord(s)
            nn = node.get(c,None)
            if nn is not None:
                node = nn
            else:
                nn = {}
                self.nodes.append(nn)
                node[c] = nn
