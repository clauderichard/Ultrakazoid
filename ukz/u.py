
from ukz.tk import *
from ukz.hm import *
from fractions import *

def isSmallAlpha(s):
    c = ord(s)
    return c >= ord('a') and c <= ord('z') and c != ord('x')
def isBigAlpha(s):
    c = ord(s)
    return c >= ord('A') and c <= ord('Z') and c != ord('X')
def isAlpha(s):
    return isSmallAlpha(s) or isBigAlpha(s)
def isDigit(s):
    c = ord(s)
    return c >= ord('0') and c <= ord('9')
def isAlphaNumeric(s):
    return isAlpha(s) or isDigit(s)
def isPitchModifier(s):
    return isDigit(s) or s == "#"

# State numbers in the UKZ tokenizer automaton
EMPTY = 0
NOTE = 1
INT = 2
FRAC = 3
DOT = 4
EXCL = 5
AT = 6
OP = 7
VAR = 8
LBRACK = 9
RBRACK = 10
LPAREN = 11
RPAREN = 12
# This is for the parser only
# (not for leaves in the parse tree, only for other nodes)
MEL = 100
MELS = 101

class UkzStates:
    stateStrings = {
        EMPTY: "EMPTY",
        NOTE: "NOTE",
        INT: "INT",
        FRAC: "FRAC",
        DOT: "DOT",
        EXCL: "EXCL",
        AT: "AT",
        OP: "OP",
        VAR: "VAR",
        LBRACK: "LBRACK",
        RBRACK: "RBRACK",
        LPAREN: "LPAREN",
        RPAREN: "RPAREN",
        MEL: "MEL",
        MELS: "MELS"
    }
    
# Make the UKZ tokenizer automaton
def mkUkzTkAutomaton():
    a = TkAutomaton(EMPTY)
    
    # silence
    a.addTransition(EMPTY, ".", DOT)
    
    # notes
    noteModifiers = "#°"
    a.addTransition(EMPTY, isAlpha, NOTE)
    a.addTransition(NOTE, isDigit, NOTE)
    a.addTransition(NOTE, noteModifiers, NOTE)
    
    # integers
    a.addTransition(EMPTY, isDigit, INT)
    a.addTransition(INT, isDigit, INT)
    a.addTransition(INT, '/', FRAC)
    a.addTransition(FRAC, isDigit, FRAC)
    
    # symbols like brackets etc
    a.addTransition(EMPTY, '[', LBRACK)
    a.addTransition(EMPTY, ']', RBRACK)
    a.addTransition(EMPTY, '(', LPAREN)
    a.addTransition(EMPTY, ')', RPAREN)
    #for (sym,symC) in zip(UkzStates.symbols,UkzStates.symbolChars):
    #    a.addTransition(EMPTY, symC, sym)
    
    # operators
    opChars = "+-*/%=^xX:"
    a.addTransition(EMPTY, "@", AT)
    a.addTransition(AT, "@", AT)
    a.addTransition(EMPTY, "!", EXCL)
    a.addTransition(AT, "!", EXCL)
    for state in [EMPTY,EXCL,AT]:
        a.addTransition(state, opChars, OP)
    # multi-char operators dealt with here!
    a.addTransition(OP, opChars, OP)
    
    # variables
    a.addTransition(EMPTY, "$", VAR)
    a.addTransition(VAR, isAlphaNumeric, VAR)

    # DONE!
    return a

################

def mkUkzPrRules():
    rs = PrRules()
    
    # simplest melodies
    rs.addRule( MEL, [NOTE] )
    rs.addRule( MEL, [DOT] )
    
    # melody operators
    rs.addRule( MEL, [MEL, OP, INT] )
    rs.addRule( MEL, [MEL, OP, FRAC] )
    
    # melody sequencing
    rs.addAdoptionRule( MELS, [MELS, MEL], [OP] )
    rs.addRule( MELS, MEL, [OP, EOF] )
    #rs.addRule( MELS, [MEL, MEL], [OP] )
    
    # brackets and parentheses
    rs.addRule( MEL, [LBRACK, MELS, RBRACK] )
    rs.addRule( MEL, [LPAREN, MELS, RPAREN] )
     
    return rs
    
################

def applyOpToMel(mel,op,arg):
    mel.applyOperator(op, arg)
    return mel
def sequenceMels(mels):
    return MelNode(0,mels)
def parallelMels(mels):
    return MelNode(1,mels)
def sequenceMels1(l,mels,r):
    return sequenceMels(mels)
def parallelMels1(l,mels,r):
    return parallelMels(mels)
def identityFunction(x):
    return x
def makeFraction(fracString):
    fs = fracString.replace('%','/')
    return Fraction(fs)

def mkUkzTraverser():
    t = Traverser()
    
    # leaf nodes
    t.addLeafRule( NOTE, lambda v: MelLeaf(v) )
    t.addLeafRule( DOT, lambda v: MelLeaf(v) )
    t.addLeafRule( OP, identityFunction )
    t.addLeafRule( INT, lambda v: int(v) )
    t.addLeafRule( FRAC, makeFraction )
    
    # building melodies simply
    t.addRule( MEL, [NOTE], identityFunction )
    t.addRule( MEL, [DOT], identityFunction )
    t.addRule( MEL, [MEL, OP, INT], applyOpToMel )
    t.addRule( MEL, [MEL, OP, FRAC], applyOpToMel )
    
    # melody arrays
    t.addPowerRule( MELS, MEL, identityFunction )
    t.addRule( MEL, [LBRACK, MELS, RBRACK], sequenceMels1 )
    t.addRule( MEL, [LPAREN, MELS, RPAREN], parallelMels1 )
    #t.addPowerRule2( MEL, [LBRACK, MELS, RBRACK], 1, MEL, sequenceMels )
    #t.addPowerRule2( MEL, [LPAREN, MELS, RPAREN], 1, MEL, parallelMels )
    
    return t

def traverseUkzTree(node):
    traverser = mkUkzTraverser()
    return traverser.traverse(node)

################
