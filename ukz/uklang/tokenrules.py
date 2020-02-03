from ukz.uklr import *
from .states import *
from .melodyopmap import *
#from .charsets import *

################
# Some functions for stuff

pitchChars = "ABCDEFGHJLMRSTU"
pitchChars += pitchChars.lower()

def isSmallAlpha(acc,s):
    c = ord(s)
    return c >= ord('a') and c <= ord('z')
def isBigAlpha(acc,s):
    c = ord(s)
    return c >= ord('A') and c <= ord('Z')
def isAlpha(acc,s):
    return isSmallAlpha(acc,s) \
     or isBigAlpha(acc,s)
def isDigit(acc,s):
    c = ord(s)
    return c >= ord('0') and c <= ord('9')
def isAlphaNumeric(acc,s):
    return isAlpha(acc,s) \
     or isDigit(acc,s)

def opTrans(acc,input):
  i = 0
  while i<len(acc) and \
   (acc[i]==':' or acc[i]=='!'):
    i += 1
  return opGood(acc[i:]+input)

def trimOp(op):
  i = 0
  while i < len(op) and op[i]==':':
    i += 1
  return op[i:]

def processToken(t):
  if t.type == OP:
    if ukzMelodyUnOpMap.get(\
     trimOp(t.value),None) \
     is not None:
      t.type = UNOP
  return t

################
# Make the UKZ tokenizer automaton
def fillUkzTkRules(p):
    
  # silence
  p.tkRule(EMPTY, ".", DOT)
    
  #p.tkRule(EMPTY, "&", LOCK)
  p.tkRule(EMPTY, "-", DASH)
  
  # pitch
  p.tkRule(EMPTY, pitchChars, PITCH)
  p.tkRule(PITCH, "^v", PITCH)
  p.tkRule(PITCH, isDigit, PITCH)
  
  # integers
  p.tkRule(EMPTY, isDigit, INT)
  p.tkRule(INT, isDigit, INT)
  p.tkRule(INT, '/', FRAC)
  p.tkRule(FRAC, isDigit, FRAC)
    
  # symbols like brackets etc
  p.tkRule(EMPTY, '[', LBRACK)
  p.tkRule(EMPTY, ']', RBRACK)
  p.tkRule(EMPTY, '(', LPAREN)
  p.tkRule(EMPTY, ')', RPAREN)
  p.tkRule(EMPTY, "|", PIPE)
  p.tkRule(PIPE, "|", PIPE)

  # transpose: special operator
  p.tkRule(EMPTY, "^v", TRANSPOSE)
  p.tkRule(TRANSPOSE, isDigit, TRANSPOSE)
  
  # operators
  p.tkRule(EMPTY, ":", AT)
  p.tkRule(AT, ":", AT)
  p.tkRule(EMPTY, "!", EXCL)
  p.tkRule(AT, "!", EXCL)
    
  for state in [EMPTY,OP]:
    p.tkRule(state, opTrans, OP)
    
  # property setting
  #a.addTransition(EXCL, isAlphaNumeric, PROPNAME)
  #a.addTransition(PROPNAME, isAlphaNumeric, PROPNAME)
  #a.addTransition(PROPNAME, '=', OP)

  p.tkPostProcessor = processToken
    
  # DONE!
  return p
