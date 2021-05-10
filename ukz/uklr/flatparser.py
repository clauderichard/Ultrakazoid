from .transmatrix import TransMatrix
from .tokenizer import TkToken

BOF = "__BOF"
EOF = "__EOF"

class ParserFlatRule:
    
    def __init__(self,resultType,stackTypes,resultFunc):
        self.resultType = resultType
        self.stackTypes = stackTypes
        self.resultFunc = resultFunc

class ParserFlatRuleMaybe:

    def __init__(self,rule,dic):
        self.rule = rule
        self.dic = dic

class ParserFlatRuleset:

    def __init__(self):
        self.rulesList = []
        self.rulesMap = {}

    def addRule(self,resultType,stackTypes,resultFunc):
        self.rulesList.append(ParserFlatRule( \
          resultType,stackTypes,resultFunc))
    
    # Call this after all rules have been added.
    def initialize(self):
        trans = self.__topToNextTrans()
        for rule in self.rulesList:
            for nx in trans[rule.resultType]:
                self.__initRule( rule, nx )
            self.__initRule( rule, EOF )
    
    # Resulting transmatrix:
    # From top of stack T, to next input type I
    # has arrow iff
    # prod rules with that top of stack
    # can be applied when next input is N.
    def __topToNextTrans(self):
        transDownR = TransMatrix.eye() # maybe apply
        transSibR = TransMatrix() # must be applied
        transUpL = TransMatrix.eye() # maybe apply
        for rule in self.rulesList:
            transDownR.addArrow( rule.resultType, rule.stackTypes[0] )
            transUpL.addArrow( rule.stackTypes[len(rule.stackTypes)-1], rule.resultType )
            for i in range(0,len(rule.stackTypes)-1):
                transSibR.addArrow( rule.stackTypes[i], rule.stackTypes[i+1] )
        # transDownR **= None
        # transUpL **= None
        transDownR.ipowInf()
        transUpL.ipowInf()
        return transUpL * transSibR * transDownR
    
    def __initRule(self,rule,nextInput):
        x = self.rulesMap.setdefault(nextInput,{})
        y = None
        for tok in reversed(rule.stackTypes[1:]):
            # if not isinstance(x,dict):
            #     raise Exception('redundant rule found?')
            if isinstance(x,ParserFlatRule):
                raise Exception('redundant rule found?')
            y = x
            x = x.setdefault(tok,{})
        
        # x[rule.stackTypes[0]] = rule

        if isinstance(x,ParserFlatRuleMaybe):
            raise Exception("Rule already has a subset of it initialized. Bad ordering!")
        elif isinstance(x,ParserFlatRule):
            z = {}
            y[rule.stackTypes[1]] = ParserFlatRuleMaybe(x, z)
            z[rule.stackTypes[0]] = rule
        elif rule.stackTypes[0] in x and isinstance(x[rule.stackTypes[0]],dict):
            x[rule.stackTypes[0]] = ParserFlatRuleMaybe(rule,x[rule.stackTypes[0]])
        else:
            x[rule.stackTypes[0]] = rule
    
    def matchStackTokens(self,stackTokens,nextInputTok):
        try:
            x = self.rulesMap[nextInputTok.type]
            foundRule = None
            for tok in reversed(stackTokens):
                try:
                    x = x[tok.type]
                    if isinstance(x,ParserFlatRuleMaybe):
                        foundRule = x.rule
                        x = x.dic
                    if not isinstance(x,dict):
                        return x
                except KeyError:
                    return foundRule
        except KeyError:
            return None
        
    def matchStackTypes(self,stackLength,stackTypes,nextInputType):
        try:
            x = self.rulesMap[nextInputType]
            foundRule = None
            # for typ in reversed(stackTypes):
            for i in range(stackLength-1,-1,-1):
                typ = stackTypes[i]
                try:
                    x = x[typ]
                    if isinstance(x,ParserFlatRuleMaybe):
                        foundRule = x.rule
                        x = x.dic
                    if not isinstance(x,dict):
                        return x
                except KeyError:
                    return foundRule
        except KeyError:
            return None
        
                
class FlatParser:

    def __init__(self):
        self.ruleset = ParserFlatRuleset()
        self.rulesetInitialized = False
        
    def addRule(self,resultType,stackTypes,resultFunc):
        self.ruleset.addRule(resultType,stackTypes,resultFunc)

    def parse(self,tokens):
        if not self.rulesetInitialized:
            self.ruleset.initialize()
            self.rulesetInitialized = True
        

        # Hacking: will modify tokens list in place.
        # within stack, tokens[i] will only be type.
        # stackValues has the values.
        tokens.append(TkToken(EOF,None))
        capInputIndex = len(tokens)
        stackValues = [0] * (capInputIndex+1)
        stackLength = 0
        inputIndex = 0
        nextInputType = tokens[0].type
        nextInputValue = tokens[0].value

        rulesmap = self.ruleset.rulesMap

        while True:

            mat = None
            try:
                x = rulesmap[nextInputType]
                for i in range(stackLength-1,-1,-1):
                    typ = tokens[i]
                    try:
                        x = x[typ]
                        if isinstance(x,ParserFlatRuleMaybe):
                            mat = x.rule
                            x = x.dic
                        elif not isinstance(x,dict):
                            mat = x
                            break
                    except KeyError:
                        # mat = foundRule
                        break
            except KeyError:
                pass

            if mat is None:
                stackValues[stackLength] = nextInputValue
                tokens[stackLength] = nextInputType
                stackLength += 1
                inputIndex += 1
                if inputIndex >= capInputIndex:
                    break
                tok = tokens[inputIndex]
                # nextInputType,nextInputValue = tok.type,tok.value
                nextInputType = tok.type
                nextInputValue = tok.value
            else:
                stackI1 = stackLength - len(mat.stackTypes)
                resultArgs = stackValues[stackI1:stackLength]
                tokens[stackI1] = mat.resultType
                stackValues[stackI1] = mat.resultFunc(*resultArgs)
                stackLength = stackI1 + 1

        # expect [finalvalue,EOF]
        if stackLength == 2:
            return stackValues[0]
        else:
            return None
