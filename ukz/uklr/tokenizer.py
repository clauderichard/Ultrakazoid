from .token import TkToken

################################################

# Node in a tokenizer's automaton
class TokenizerAutomatonNode:

    def __init__(self,defaultResult):
        self.transitions = {}
        self.defaultResult = defaultResult

    def addTransition(self,charset,result):
        if not isinstance(charset,str):
            raise Exception("Expecting a string here")
        for c in charset:
            if self.transitions.get(c,None) is None:
                self.transitions[c] = result

    def getNext(self,inputChar):
        return self.transitions.get(inputChar,self.defaultResult)

################################################

class TokenizerAutomaton:

    def __init__(self,emptyNodeIndex):
        self.emptyNodeIndex = emptyNodeIndex
        self.symbolTypeMap = {}
        self.nodes = {emptyNodeIndex: TokenizerAutomatonNode(self.emptyNodeIndex)}
        #self.whitespaceCharset = set(bytearray(' \n\r\t','utf-8'))
        self.whitespaceCharset = set(' \n\r\t')
        # Want to be in node this[acc] whenever
        #   accumulated string is acc
        self.__accToNodeIndex = {}
        # should never conflict with other node indices
        self.__accToNodeCounter = 1000000
        
    def __getNodeIndexForAcc(self,acc):
        accstr = acc
        if accstr=="":
            return self.__getNode(self.emptyNodeIndex)
        if self.__accToNodeIndex.get(accstr,None) is None:
            self.__accToNodeIndex[accstr] = self.__accToNodeCounter
            self.__accToNodeCounter += 1
        return self.__accToNodeIndex[accstr]

    def addTransitionsForSymbol(self,symString,tkType):
        #symBytes = bytearray(symString,'utf-8')
        symFirstChar = symString[0]
        nodeIndexFirstChar = self.__getNodeIndexForAcc(symFirstChar)
        self.__getNode(self.emptyNodeIndex).addTransition( \
          symFirstChar, nodeIndexFirstChar)
        for l in range(1,len(symString)+1):
            acc1 = symString[0:(l-1)]
            acc2Last = symString[l-1]
            acc2 = acc1 + acc2Last
            node1 = self.__getNode(self.__getNodeIndexForAcc(acc1))
            node2Index = self.__getNodeIndexForAcc(acc2)
            node1.addTransition(acc2Last,node2Index)
        finalNodeIndex = self.__getNodeIndexForAcc(symString)
        self.symbolTypeMap[finalNodeIndex] = tkType

    # If node doesn't exist yet, then
    #   creates it automatically before returning.
    def __getNode(self,index):
        return self.nodes.setdefault(index,TokenizerAutomatonNode(self.emptyNodeIndex))
    
    def addTransition(self,fromNodeIndex,charset,resultIndex):
        self.__getNode(fromNodeIndex).addTransition(charset,resultIndex)
    
    def tokenize(self,inputString):
        ret = []
        curNodeIndex = self.emptyNodeIndex
        acc = ""

        # inputCharIndex = 0
        # accBegin = 0
        inputCharsIter = iter(inputString)
        nextInputChar = next(inputCharsIter)
        while True:
            mustReadNextInput = False
            
            nextNodeIndex = self.emptyNodeIndex
            if curNodeIndex in self.nodes:
                nxnode = self.nodes[curNodeIndex]
                nextNodeIndex = nxnode.transitions.get(nextInputChar,nxnode.defaultResult)
            
            # if cannot accumulate string
            if nextNodeIndex == self.emptyNodeIndex:
                # if had acculated stuff
                if curNodeIndex != self.emptyNodeIndex:
                    # accumulation done
                    # accReturn = inputString[accBegin:inputCharIndex]
                    # ret.append(TkToken(self.symbolTypeMap.get(curNodeIndex,curNodeIndex),accReturn))
                    ret.append(TkToken(self.symbolTypeMap.get(curNodeIndex,curNodeIndex),acc))
                    acc = ""
                    curNodeIndex = self.emptyNodeIndex
                    # accBegin = inputCharIndex
                elif nextInputChar in self.whitespaceCharset:
                    # acc empty, found yet more whitespace
                    mustReadNextInput = True
                    # accBegin += 1
                else:
                    # acc empty, found alien stuff
                    raise Exception("Unexpected character")
            else:
                curNodeIndex = nextNodeIndex
                acc += nextInputChar
                mustReadNextInput = True
            if mustReadNextInput:
                # inputCharIndex += 1
                # if inputCharIndex >= capInputCharIndex:
                #     break
                # nextInputChar = inputString[inputCharIndex]
                try:
                    # inputCharIndex += 1
                    nextInputChar = next(inputCharsIter)
                except StopIteration:
                    break
        if curNodeIndex != self.emptyNodeIndex:
            # accReturn = inputString[accBegin:inputCharIndex]
            # ret.append(TkToken(self.symbolTypeMap.get(curNodeIndex,curNodeIndex),accReturn))
            ret.append(TkToken(self.symbolTypeMap.get(curNodeIndex,curNodeIndex),acc))
        return ret

################################################
