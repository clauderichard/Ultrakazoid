
from ukz.uklr import Traverser
from .hiermelody import \
 Mel,MelLeaf,MelNode,MelNodePiped
from .states import *
from fractions import Fraction
from ukz.utils.iterutil \
 import intsFromTo

def lockMel(l,mel):
  mel.applyOperator(l,0)
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
def applyUnOpToMel(mel,op):
  mel.applyOperator(op, None)
  return mel
def emptyMel(l,r):
  return MelNode(0,[])
def sequenceMels(l,mels,r):
  return MelNode(0,mels)
def parallelMels(l,mels,r):
  return MelNode(1,mels)
def sequenceMelsWithPipe(\
	l,ms1,p,ms2,r):
  return MelNodePiped(0,ms1,ms2)
def parallelMelsWithPipe(\
	l,ms1,p,ms2,r):
  return MelNodePiped(1,ms1,ms2)
def identityFunction(x):
  return x
def makeFraction(fracString):
  fs = fracString.replace('%','/')
  return Fraction(fs)
def mkIntRange(dis):
  print(f"mkIntRange {dis}")
  if len(dis)==0:
    return []
  i = dis[0]
  ls = [i]
  for j in dis[1:]:
    ls.extend( \
     list(intsFromTo(i,j))[0:] )
    i = j
  return ls
def mkIntRanges(rs):
  print(f"mkIntRanges {rs}")
  ls = []
  for r in rs:
    if isinstance(r,list):
      ls.extend(r)
    elif isinstance(r,int):
      ls.append(r)
    else:
      raise ValueError('unsuported type')
  return ls
def get2nd(a,b,c=None):
  return b
def mkInts(xs):
  ls = []
  i = 0
  dash = False
  for x in xs:
    if isinstance(x,int):
      if dash:
        ls.extend(list( \
        	intsFromTo(i,x))[1:] )
      else:
        ls.append(x)
      i = x
      dash = False
    else:
      dash = True
  return ls

def mkUkzTraverser():
    t = Traverser()
    
    # leaf nodes
    t.addLeafRule( NOTE, lambda v: MelLeaf(v) )
    t.addLeafRule( DOT, lambda v: MelLeaf(v) )
    t.addLeafRule( INT, lambda v: int(v) )
    t.addLeafRule( FRAC, makeFraction )
    
    # building melodies simply
    t.addRule( MEL, [NOTE], identityFunction )
    t.addRule( MEL, [DOT], identityFunction )
    #t.addRule( MEL, [PIPE], identityFunction )
    t.addRule( MEL, [LOCK,MEL], lockMel )
    #t.addRule( MEL, [MEL,UNTILEND], untilEndMel )
    t.addRule( MEL, [MEL, INT], octaveTransposeMel )
    #t.addRule( MEL, [MEL, SHARP], sharpMel )
    #t.addRule( MEL, [MEL, SHARP, INT], sharpMelInt )
    t.addRule( MEL, [MEL, OP, INT], applyOpToMel )
    t.addRule( MEL, [MEL, OP, FRAC], applyOpToMel )
    t.addRule( MEL, [MEL, OP, MEL], applyOpToMel )
    t.addRule( MEL, [MEL, OP, INTARRAY], applyOpToMel )
    t.addRule( MEL, [MEL, UNOP], applyUnOpToMel )
    t.addRule( MEL, [MEL, UNOP, INT], applyOpToMel )
    t.addRule( MEL, [MEL, UNOP, INTARRAY], applyOpToMel )
    
    # melody arrays
    t.addPowerRule( MELS, MEL, identityFunction )
    t.addRule( MEL, [LBRACK, MELS, RBRACK], sequenceMels )
    t.addRule( MEL, [LPAREN, MELS, RPAREN], parallelMels )
    t.addRule( MEL, [LBRACK, RBRACK], emptyMel )
    t.addRule( MEL, [LPAREN, RPAREN], emptyMel )
    t.addRule( MEL, [LBRACK, MELS, PIPE, MELS, RBRACK], sequenceMelsWithPipe )
    t.addRule( MEL, [LPAREN, MELS, PIPE, MELS, RPAREN], parallelMelsWithPipe )
    
    t.addRule( INTARRAY, \
     [LBRACK,INTS,RBRACK], \
     get2nd )
    t.addRule( INTARRAY, \
     [LPAREN,INTS,RPAREN], \
     get2nd )
     
    t.addPowerRule( INTS, \
     [INT,DASH], \
     mkInts )
    #t.addRule( INTRANGE, \
    # [INT,DASH,INT], \
    # makeIntRange )
    #t.addRule( DASHINT, [DASH,INT], \
    # get2nd )
    
    return t

def traverseUkzTree(node):
    traverser = mkUkzTraverser()
    return traverser.traverse(node)

################
