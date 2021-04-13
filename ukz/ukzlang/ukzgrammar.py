from ukz.uklr import *
# from .states import *
from .hmel import \
  mkHmelSeq,mkHmelPar,mkHmelNote,mkHmelRest,Hmel,HmelNote
from .pitchdecoder import PitchDecoder
from ukz.util import *
from math import gcd
from ukz.util import mkFraction
from ukz.uklr.patternflattener import *
from ukz.melody.controllers import UkzControllers
from ukz.melody import \
  Fmel,Note,Gradient,Scale

################################################
# Token Types

PITCH = "PITCH"
INT = "INT"
FRAC = "FRAC"
DASH = "-"
DOUBLEDASH = "--"

FOREACHLEAF = "!"
FOREACHCHILD = ":"
FOR = "FOR"
BINOP = "BINOP"
UNOP = "UNOP"
AMBOP = "AMBOP"

MEL = "MEL"
LBRACK = "["
RBRACK = "]"
LPAREN = "("
RPAREN = ")"
# Guillemets are usually hidden,
# automatically added to ends in song.play() arg
LGUILL = "《"
RGUILL = "》"
STARTPIPE = "|"
ENDPIPE = "||"
NAME = "NAME"

################################################
# Tokenizer functions

alphaCharsUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphaCharsLower = alphaCharsUpper.lower()
alphaChars = alphaCharsLower + alphaCharsUpper
pitchChars = "ABCDEFGHJLMRSTUP"
pitchChars += pitchChars.lower()

digitChars = '0123456789'

alphaNumericChars = alphaChars + digitChars

################################################
# Make the UKZ tokenizer automaton
def fillUkzTkRules(p):
    
    # silence
    # p.tokenizerRule(DOT, ".")
      
    # pitch
    p.tokenizerRule(PITCH, pitchChars)
    p.tokenizerRule(PITCH, "^v", PITCH)
    p.tokenizerRule(PITCH, digitChars, PITCH)
    
    # integers
    p.tokenizerRule(INT, digitChars)
    p.tokenizerRule(INT, digitChars, INT)
    p.tokenizerRule(FRAC, '/', INT)
    p.tokenizerRule(FRAC, digitChars, FRAC)
    
    # operators
    p.tokenizerRule(FOREACHCHILD, ":")
    p.tokenizerRule(FOREACHCHILD, ":", FOREACHCHILD)
    p.tokenizerRule(FOREACHLEAF, "!")
    p.tokenizerRule(FOREACHLEAF, "!", FOREACHCHILD)
    
    p.tokenizerRule(STARTPIPE, "|")
    p.tokenizerRule(ENDPIPE, "|", STARTPIPE)
    
    p.tokenizerRule(NAME, "%")
    p.tokenizerRule(NAME, alphaNumericChars, NAME)
      
    # DONE!
    return p

################
# Functions for parser

def tokenIsName(s):
    return isinstance(s,str) and \
      s.startswith("%")
def getNameFromToken(x):
    return None if (x is None or x=='%') else x[1:]

# Given a list of lists (kind of a tree)
# Flatten the lists recursively.
# Result: A list where each element isn't a list.
#         Each leaf in arg is an element in result.
def flattenLists(xs):
    return list(flattenLists_h(xs))
def flattenLists_h(xs):
    for x in xs:
        if isinstance(x,list):
            yield from flattenLists(x)
        else:
            yield x
        
    
################
class UkzSymbolsConfig:

    bendWithMelody = {
      '': (UkzControllers.pitchBend,-24,24),
      'V': (UkzControllers.expression,0,12),
      'bal': (UkzControllers.balance,0,24),
      'atk': (UkzControllers.attack,0,12),
      'rev': (UkzControllers.reverb,0,12)
    }
    
def addukzlangSymbols(p):
    
    # Operators for transpose
    p.sym(AMBOP, '^', (Fmel.sharp, Fmel.transposeUp))
    p.sym(AMBOP, 'v', (Fmel.flat, Fmel.transposeDown))
    p.sym(BINOP, 'o', Fmel.octavesUp)

    # unary operators
    p.sym(UNOP, '¬', Fmel.durToEnd)
    p.sym(UNOP, '<¬', lambda x: x.backwardLeaveT(x.d))

    # binary operators
    p.sym(BINOP, '<', Fmel.backwardLeaveT)
    p.sym(BINOP, 'x', Fmel.repeat)
    p.sym(BINOP, 'x=', Fmel.repeatUntil)
    p.sym(BINOP, '*', Fmel.expand)
    p.sym(BINOP, '/', Fmel.contract)
    p.sym(BINOP, '=', Fmel.expandTo)
    p.sym(BINOP, '@', Fmel.addLoudness)
    p.sym(BINOP, '_', Fmel.setNoteDurs)

    def expandToScale(mel,a):
        notes = a.notes
        sc = Scale(map(lambda n: n.p, notes))
        for n in mel.notes:
            n.p = sc[n.p]
        return mel
    p.sym(BINOP, '<$', expandToScale)
    p.sym(BINOP, '<<', Fmel.injectMelody)
    p.sym(BINOP, '¬=', lambda x,a: x.durTo(a,False))
    p.sym(BINOP, '¬==', lambda x,a: x.durTo(a,True))
    p.sym(BINOP, '<€', Fmel.parallelMapIntoScales)

    def lambdaBend(k):
        (ctrl,p1,p2) = UkzSymbolsConfig.bendWithMelody[k]
        return lambda x,a: x.applyWholeBendFromMelody(ctrl,p1,p2,a)
    def lambdaCyclicBend(k):
        (ctrl,p1,p2) = UkzSymbolsConfig.bendWithMelody[k]
        return lambda x,a: x.applyCyclicBendFromMelody(ctrl,p1,p2,a)
    def lambdaEqualBend(k):
        (ctrl,p1,p2) = UkzSymbolsConfig.bendWithMelody[k]
        return lambda x,a: x.applyEqualBendFromMelody(ctrl,p1,p2,a)
    for k,_ in UkzSymbolsConfig.bendWithMelody.items():
        p.sym(BINOP, '~'+k, lambdaBend(k))
        p.sym(BINOP, '~~'+k, lambdaCyclicBend(k))
        p.sym(BINOP, '~='+k, lambdaEqualBend(k))
    
    p.addSimpleSymbols( [DASH,DOUBLEDASH,LBRACK,RBRACK,LPAREN,RPAREN,LGUILL,RGUILL] )
    
    p.symf(MEL, ".", (lambda: mkHmelRest()))
        
################################################
# Parse-traverse Rules

def fillUkzPrTrRules(p):
    
    # arg = alt(INT,FRAC,MEL)
    ambarg = INT

    # Traverse leaf nodes
    p.parserLeafRule( PITCH, lambda s: PitchDecoder.decode(s) )
    # p.parserLeafRule( DOT, lambda dot: mkHmelRest(1) )
    p.parserLeafRule( INT, lambda s: int(s) )
    p.parserLeafRule( FRAC, lambda s: mkFraction(s) )
    # Foreach descendant
    p.parserLeafRule( FOREACHCHILD, lambda x: len(x))
    p.parserLeafRule( FOREACHLEAF, lambda x: -1)
    
    #p.parserRule( FOR, alt(FOREACHLEAF,FOREACHCHILD) )
    p.parserRule( FOR, FOREACHCHILD )
    p.parserRule( FOR, FOREACHLEAF )
    
    p.parserRule( INT, [DASH, INT], (lambda d,i: -i))
    p.parserRule( PITCH, [PITCH, INT], (lambda p,i: p + 12*i))
    
    ################################################
    # primitive melodies

    p.parserRule( MEL, PITCH, mkHmelNote )
    
    ################################################
    # Chromatic shredding e.g. "c--g--d^--G"
    def pitchesToLots(ps):
        x = ps[0]
        xs = [x]
        for p in ps[1:]:
            qs = list(intsFromTo(x,p))[1:]
            x = p
            xs.extend(qs)
        return list(map(\
        mkHmelNote,xs))
    p.parserDelimitedRule( MEL, PITCH, DOUBLEDASH, pitchesToLots)

    ################################################
    # Unary operators
    def applyUnOp(mel,op):
        mel.applyOp(op)
        return mel
    def applyAmbOpToMel1(mel,ambop):
        return applyUnOp(mel,ambop[0])

    p.parserRule( MEL, [MEL, UNOP], applyUnOp )

    def forUnop(mel,deg,uop):
        for c in mel.getDescendants(deg):
            c.applyOp(uop)
        return mel
    p.parserRule( MEL, [MEL, FOR, UNOP], forUnop )

    ################################################
    # Binary operators
    def applyBinOp(mel,op,arg):
        a = arg.flatten() if isinstance(arg,Hmel) else arg
        mel.applyOp(op,a)
        return mel

    def leftForBinop(mel,deg,bop,arg):
        for c in mel.getDescendants(deg):
            a = arg.flatten() if isinstance(arg,Hmel) else arg
            c.applyOp(bop,a)
        return mel

    for argg in [INT,FRAC,MEL]:
        p.parserRule( MEL, [MEL, BINOP, argg], applyBinOp )
        p.parserRule( MEL, [MEL, FOR, BINOP, argg], leftForBinop )

    ################################################
    # Ambiguous operators
    def applyAmbOpToMel2(mel,ambop,arg):
        return applyBinOp(mel,ambop[1],arg)
    p.parserRule( MEL, [MEL, AMBOP], applyAmbOpToMel1 )
    p.parserRule( MEL, [MEL, AMBOP, ambarg], applyAmbOpToMel2 )

    def leftForAmbop1(mel,deg,ambop):
        return forUnop(mel,deg,ambop[0])
    p.parserRule( MEL, [MEL, FOR, AMBOP], leftForAmbop1 )

    def leftForAmbop2(mel,deg,ambop,arg):
        return leftForBinop(mel,deg,ambop[1],arg)
    p.parserRule( MEL, [MEL, FOR, AMBOP, ambarg], leftForAmbop2 )

    ################################################
    # Composite melodies

    # mels includes names because alt(NAME,MEL,PIPE) or something
    def separateMelList(mels):
        xs = flattenLists(mels)
        curname = None
        startseen = False
        endseen = False
        prexs = []
        midxs = []
        acc = []
        for x in xs:
            if x == STARTPIPE:
                if startseen:
                    raise "Duplicate start pipes in same melody"
                if endseen:
                    raise "Start pipe after end pipe in same melody"
                startseen = True
                prexs = acc
                acc = []
            elif x == ENDPIPE:
                if endseen:
                    raise "Duplicate end pipe in same melody"
                endseen = True
                midxs = acc
                acc = []
            elif tokenIsName(x):
                curname = getNameFromToken(x)
            else:
                if curname is not None:
                    x.c = curname
                acc.append(x)
        if not endseen:
            midxs = acc
            acc = []
        return (prexs,midxs,acc)
        
    def sequenceMels(l,mels,r):
        (a,b,c) = separateMelList(mels)
        return mkHmelSeq(a,b,c)
    def parallelMels(l,mels,r):
        (a,b,c) = separateMelList(mels)
        return mkHmelPar(a,b,c)

    def indexOfGroupWithEndPipe(gs):
        i = 0
        for st,ms in gs:
            if ENDPIPE in ms:
                return i
            i += 1
        return -1
    def moveEndPipeLast(gs):
        i = indexOfGroupWithEndPipe(gs)
        if i<0:
            return
        x = gs[i]
        del gs[i]
        gs.append(x)
    def guillMels(l,mels,r):
        gs = groupWithStateModifier(tokenIsName,lambda x:x,mels)
        gs = list(gs)
        moveEndPipeLast(gs)
        sms = []
        for st,ms in gs:
            sm = sequenceMels(l,ms,r)
            nam = getNameFromToken(st)
            if nam is not None:
                sm.c = nam
            sms.append(sm)
        return mkHmelPar([],sms,[])
        

    elPat = star(alt(MEL,STARTPIPE,ENDPIPE,NAME))
    p.parserRule(MEL, [LBRACK, elPat, RBRACK], sequenceMels)
    p.parserRule(MEL, [LPAREN, elPat, RPAREN], parallelMels)
    p.parserRule(MEL, [LGUILL, elPat, RGUILL], guillMels)
    
    ################################################

    return p
        