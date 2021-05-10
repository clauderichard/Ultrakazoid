from .tokenizer import TokenizerAutomaton
from .token import TkToken
from .flatparser import FlatParser
from .patternflattener import *

TKEMPTYSTATE = ""

def get1st(x,*a):
    return x
def returnArgsList(*a):
    return a

class LrProcessor:

    listTypeCounter = 1
    alreadyPrintedArgh = False

    def __init__(self):
        self.tokenizerAutomaton = TokenizerAutomaton(TKEMPTYSTATE)
        self.flatParser = FlatParser()
        self.symbolValueGenerators = {}
        self.keywordSets = {}
        self.leafRules = {}
        
    ################
    # Adding rules to tokenizer,parser,traverser

    def tokenizerRule(self,resultIndex,func,fromNodeIndex=TKEMPTYSTATE):
        self.tokenizerAutomaton.addTransition(fromNodeIndex,func,resultIndex)
            
    def keywords(self,fromTkType,words):
        self.keywordSets[fromTkType] = words

    ################
    # Symbols

    # If you want a symbol to have a value,
    # e.g. for operator symbols the value is a lambda function.
    def sym(self,tkType,symStr,value):
        self.symf(tkType,symStr,lambda: value)

    # If you want a symbol to have a meaning, but e.g.
    # each instance of the symbol should generate a distinct
    # instance of something.
    def symf(self,tkType,symStr,valueGeneratorFunc):
        self.tokenizerAutomaton.addTransitionsForSymbol(symStr,tkType)
        self.symbolValueGenerators[symStr] = valueGeneratorFunc
        self.parserLeafRule( tkType, lambda op: self.symbolValueGenerators[op]())

    # add list of symbols with no value attached to them.
    def addSimpleSymbols(self,symStrs):
        for s in symStrs:
            self.symf(s,s,lambda: None)

    ################
    # Parser rules (includes traversing)

    def parserLeafRule(self,rootType,func):
        if rootType not in self.leafRules:
            self.leafRules[rootType] = func

    def parserRule(self,resultType,\
      childrenTypes,\
      resultFunc=get1st):
        rhsList = childrenTypes if isinstance(childrenTypes,list) else [childrenTypes]
        for r in flattenedRules(resultType, rhsList, resultFunc):
            a,b,c = r
            self.flatParser.addRule(a, b, c)
        
    def parserDelimitedRule(self,\
      lsType,elType,delimType,elsToLsFunc):
        xy = f"DELIM-{lsType}-{elType}-{delimType}"
        self.parserRule( xy, [elType,delimType], lambda x,y: x)
        self.parserRule( lsType, [plus(xy),elType], lambda xs,z: elsToLsFunc(xs+[z]))
        
    ################

    def applyLeafRules(self,tokens):
        # apply leaf rules
        leafRules = self.leafRules
        deff = lambda x:x
        for tok in tokens:
            tok.value = leafRules.get(tok.type,deff)(tok.value)


    def process(self,input):
        # tokenize
        tokens = self.tokenizerAutomaton.tokenize(input)
        
        # Map symbol tokens' types
        tokens = list(tokens)
        for tok in tokens:
            ks = self.keywordSets.get(tok.type,None)
            if ks is not None and tok.value in ks:
                tok.type = tok.value # type = value for keywords


        self.applyLeafRules(tokens)

        # parse
        parseTree = self.flatParser.parse(tokens)
        if parseTree is None:
            raise Exception("Could not fully parse the code!")
        return parseTree

