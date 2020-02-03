from ukz.uklr import PrRules,EOF
from .states import *

def mkUkzPrRules():
  rs = PrRules()
    
  # simplest melodies
  rs.addRule( MEL, [NOTE] )
  rs.addRule( MEL, [DOT] )
  rs.addRule( MEL, [PIPE] )
    
  rs.addRule( MEL, [LOCK,MEL] )
  rs.addRule( MEL, [MEL,UNTILEND] )
    
  # melody operators
  rs.addRule( MEL, [MEL, INT] ) # octave transpose
  rs.addRule( MEL, [MEL, SHARP], [INT] ) # transpose up by 1
  rs.addRule( MEL, [MEL, SHARP, INT] ) # transpose by different amount
  rs.addRule( MEL, [MEL, OP, INT] )
  rs.addRule( MEL, [MEL, OP, FRAC] )
  rs.addRule( MEL, [MEL, OP, MEL] )
    
  # melody sequencing
  rs.addAdoptionRule( MELS, \
   [MELS, MEL], \
   [OP,SHARP,INT,UNTILEND] )
  rs.addRule( MELS, MEL, \
   [OP,SHARP,INT,UNTILEND,EOF] )
    
  # brackets and parentheses
  rs.addRule( MEL, [LBRACK, MELS, RBRACK] )
  rs.addRule( MEL, [LPAREN, MELS, RPAREN] )
     
  return rs
    