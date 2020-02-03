from ukz.uklr import *
from .states import *
from .melodyopmap import *

def opTrans(acc,input):
  i = 0
  while i<len(acc) and \
   (acc[i]=='@' or acc[i]=='!'):
    i += 1
  return opGood(acc[i:]+input)

# Make the UKZ tokenizer automaton
def mkUkzTkAutomaton():
  a = TkAutomaton(EMPTY)
    
  # silence
  a.addTransition(EMPTY, ".", DOT)
    
  a.addTransition(EMPTY, "&", LOCK)
  a.addTransition(EMPTY, "-", DASH)
  
  # notes
  a.addTransition(EMPTY, pitchChars, NOTE)
  
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
  a.addTransition(EMPTY, "|", PIPE)
  
  # operators
  a.addTransition(EMPTY, "@", AT)
  a.addTransition(AT, "@", AT)
  a.addTransition(EMPTY, "!", EXCL)
  a.addTransition(AT, "!", EXCL)
    
  for state in [EMPTY,EXCL,AT,OP]:
    a.addTransition(\
     state, opTrans, OP)
    
  # property setting
  #a.addTransition(EXCL, isAlphaNumeric, PROPNAME)
  #a.addTransition(PROPNAME, isAlphaNumeric, PROPNAME)
  #a.addTransition(PROPNAME, '=', OP)
    
  # DONE!
  return a
