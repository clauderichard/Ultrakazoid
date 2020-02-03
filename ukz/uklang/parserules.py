from ukz.uklr import *
from .states import *
from ukz.melody import Tone
from ukz.hmel import HmelSeq,HmelPar,HmelNote,HmelRest
from .melodyopmap import opFromStr
from ukz.utils.iterutil import intsFromTo
from math import gcd
from fractions import Fraction

################

class UkzTraverser:
  g_noteDecoder = []
  
################
# Functions

def octaveTransposeMel(mel,octave):
  mel.transposeUp(12*octave)
  return mel
  
def applyOpToMel(mel,op,arg):
  return op(mel,arg)
def applyUnOpToMel(mel,op):
  return op(mel)
  
def concatListsEtc(xs):
  for x in xs:
    if isinstance(x,list):
      for y in x:
        yield y
    else:
      yield x
    
def sequenceMels(l,mels,r):
  pres = []
  mids = []
  curs = []
  atpost = False
  for m in concatListsEtc(mels):
    if m=='|':
      pres = curs
      curs = []
    elif m=='||':
      mids = curs
      curs = []
      atpost = True
    else:
      curs.append(m)
  if not atpost:
    mids = curs
    curs = []
  return HmelSeq(mids,pres,curs)

def parallelMels(l,mels,r):
  pres = []
  curs = []
  last = None
  for m in concatListsEtc(mels):
    if m=='|':
      pres = curs
      curs = []
    elif m=='||':
      last = curs[len(curs)-1]
      del curs[len(curs)-1]
    else:
      curs.append(m)
  if last is not None:
    curs.append(last)
  return HmelPar(curs,pres)

def get2nd(a,b,c=None):
  return b
  
def mkNoteWithPitch(p):
  if isinstance(p,list):
    return HmelPar(map(lambda pp: \
     HmelNote(1,Tone(pp,5)), p))
  tn = Tone(p,5)
  return HmelNote(1,tn)

def pitchesToPitch(ps,tp):
  ip = ps[0:len(ps)-1]
  lp = ps[len(ps)-1]
  return ip + pitchToPitch(lp,tp)
def pitchToPitch(p,q):
  ps = []
  if p<q:
    ps = list(range(p,q+1))
  else:
    ps = list(range(p,q-1,-1))
  return ps
def pitchesToLots(ps):
  x = ps[0]
  xs = [x]
  for p in ps[1:]:
    qs = pitchToPitch(x,p)[1:]
    x = p
    xs.extend(qs)
  return list(map(\
   mkNoteWithPitch,xs))
  #return mkMelWithPitches(xs)
  
def mkMelWithPitches(ps):
  return list(map(mkNoteWithPitch, ps))

def transposeMel(hmel,code):
  n = 1 if code[0]=='^' else -1
  if len(code) > 1:
    multiplier = int(code[1:])
    n = n*multiplier
  return hmel.transposeUp(n)
  
def zipDescs(m1,d1,op,d2,m2):
  xs = list(m1.getDescendants(d1))
  ys = list(m2.getDescendants(d2))
  m = len(xs)
  n = len(ys)
  mn = m*n // gcd(m,n)
  xys = zip(xs*(mn//m),ys*(mn//n))
  zs = list(map(lambda z: \
   op(z[0].copy(),z[1].copy()), xys))
  if isinstance(m1,HmelSeq):
    return HmelSeq(zs)
  if isinstance(m1,HmelPar):
    return HmelPar(zs)
  if isinstance(m2,HmelSeq):
    return HmelSeq(zs)
  if isinstance(m2,HmelPar):
    return HmelPar(zs)
  return HmelSeq(zs)
  

################
# Parse-traverse Rules

def fillUkzPrTrRules(p):
    
  # Traverse leaf nodes
  p.prtrLeafRule( PITCH, lambda code: \
   UkzTraverser.g_noteDecoder[code] )
  p.prtrLeafRule( DOT, lambda dot: HmelRest(1) )
  p.prtrLeafRule( INT, lambda v: int(v) )
  p.prtrLeafRule( FRAC, Fraction )
  p.prtrLeafRule( OP, lambda op: \
   opFromStr(op,1))
  p.prtrLeafRule( UNOP, lambda op: \
   opFromStr(op,0))
  p.prtrLeafRule( AT, lambda x: len(x))
  p.prtrLeafRule( EXCL, lambda x: -1)
   
  p.prtrRule( FOR, alt(EXCL,AT) )
  
  # Pitch range e.g. "c-g-d^-G"
  p.prtrDelimRule( MEL, PITCH, DASH, \
   pitchesToLots)

  # primitive rest melody
  p.prtrRule( MEL, DOT )
  # primitive note melody
  #p.prtrRule( MEL, PITCH, mkNoteWithPitch, [DASH] )
  p.prtrRule( MEL, PITCH, mkNoteWithPitch )
  
  # Transpose mel up by octaves
  p.prtrRule( MEL, \
   [MEL, INT], \
   octaveTransposeMel ) 

  # Transpose mel by semitones
  p.prtrRule( MEL, \
   [MEL, TRANSPOSE], \
   transposeMel )

  # Binary operator on mel
  p.prtrRule( MEL, \
   seq(MEL, OP, alt(INT,FRAC,MEL,INTARRAY)), \
   applyOpToMel )
   
  p.prtrRule( MEL, \
  	seq(MEL, FOR, OP, alt(\
  	INT,FRAC,MEL,INTARRAY)), \
   lambda m,d,op,a: \
   m.replaceDescendants(d,lambda x: op(x,a)) )
   
  p.prtrRule( MEL, \
  	seq(MEL, OP, FOR, MEL), \
   lambda m,op,d,a: \
   a.replaceDescendants(d, \
   lambda x: op(m.copy(),x)) )
   
  p.prtrRule( MEL, \
  	seq(MEL, FOR, OP, FOR, MEL), \
   zipDescs )

  # Unary operator on mel
  p.prtrRule( MEL, [MEL, FOR, UNOP], \
   lambda m,d,op: m.replaceDescendants(d,op) )
  
  p.prtrRule( MEL, [MEL, UNOP], applyUnOpToMel )
  
  # Sequence with []
  p.prtrRule( MEL, \
   [LBRACK, star(alt(MEL,PIPE)), RBRACK], \
   sequenceMels )
  # Parallel with ()
  p.prtrRule( MEL, \
   [LPAREN, star(alt(MEL,PIPE)), RPAREN], \
   parallelMels )
  
  return p
    