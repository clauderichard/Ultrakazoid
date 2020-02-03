
from uklr import *
from ukz.parser.hiermelody import *
from ukz.parser.states import *
from fractions import *

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
    t.addRule( MEL, [MEL, OP, MEL], applyOpToMel )
    
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
