
from ukz.uklr import Traverser
from .hiermelody import Mel,MelLeaf,MelNode
from .states import *
from fractions import Fraction

def untilEndMel(mel,ue):
    mel.applyOperator(ue,0)
    return mel
def lockMel(l,mel):
    mel.applyOperator(l,0)
    return mel
def sharpMel(mel,sharp):
    if sharp=="v":
        mel.applyOperator('-', 1)
    else:
        mel.applyOperator('+', 1)
    return mel
def sharpMelInt(mel,sharp,arg):
    if sharp=="v":
        mel.applyOperator('-', arg)
    else:
        mel.applyOperator('+', arg)
    return mel
def octaveTransposeMel(mel,octave):
    mel.applyOperator('+', 12*octave)
    return mel
def applyOpToMel(mel,op,arg):
    mel.applyOperator(op, arg)
    return mel
def sequenceMels(l,mels,r):
    return MelNode(0,mels)
def parallelMels(l,mels,r):
    return MelNode(1,mels)
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
    t.addLeafRule( PIPE, lambda v: MelLeaf(v) )
    t.addLeafRule( OP, identityFunction )
    t.addLeafRule( SHARP, identityFunction )
    t.addLeafRule( UNTILEND, identityFunction )
    t.addLeafRule( INT, lambda v: int(v) )
    t.addLeafRule( FRAC, makeFraction )
    t.addLeafRule( LOCK, identityFunction )
   
    # building melodies simply
    t.addRule( MEL, [NOTE], identityFunction )
    t.addRule( MEL, [DOT], identityFunction )
    t.addRule( MEL, [PIPE], identityFunction )
    t.addRule( MEL, [LOCK,MEL], lockMel )
    t.addRule( MEL, [MEL,UNTILEND], untilEndMel )
    t.addRule( MEL, [MEL, INT], octaveTransposeMel )
    t.addRule( MEL, [MEL, SHARP], sharpMel )
    t.addRule( MEL, [MEL, SHARP, INT], sharpMelInt )
    t.addRule( MEL, [MEL, OP, INT], applyOpToMel )
    t.addRule( MEL, [MEL, OP, FRAC], applyOpToMel )
    t.addRule( MEL, [MEL, OP, MEL], applyOpToMel )
    
    # melody arrays
    t.addPowerRule( MELS, MEL, identityFunction )
    t.addRule( MEL, [LBRACK, MELS, RBRACK], sequenceMels )
    t.addRule( MEL, [LPAREN, MELS, RPAREN], parallelMels )
    #t.addPowerRule2( MEL, [LBRACK, MELS, RBRACK], 1, MEL, sequenceMels )
    #t.addPowerRule2( MEL, [LPAREN, MELS, RPAREN], 1, MEL, parallelMels )
    
    return t

def traverseUkzTree(node):
    traverser = mkUkzTraverser()
    return traverser.traverse(node)

################
