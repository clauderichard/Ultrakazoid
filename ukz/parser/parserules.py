from uklr import PrRules,EOF
from ukz.parser.states import *

def mkUkzPrRules():
  rs = PrRules()
    
  # simplest melodies
  rs.addRule( MEL, [NOTE] )
  rs.addRule( MEL, [DOT] )
    
  # melody operators
  rs.addRule( MEL, [MEL, OP, INT] )
  rs.addRule( MEL, [MEL, OP, FRAC] )
  rs.addRule( MEL, [MEL, OP, MEL] )
    
  # melody sequencing
  rs.addAdoptionRule( MELS, [MELS, MEL], [OP] )
  rs.addRule( MELS, MEL, [OP, EOF] )
    
  # brackets and parentheses
  rs.addRule( MEL, [LBRACK, MELS, RBRACK] )
  rs.addRule( MEL, [LPAREN, MELS, RPAREN] )
     
  return rs
    