from ukz.uklr import PrRules,EOF
from .states import *

def mkUkzPrRules():
  rs = PrRules()
    
  # simplest melodies
  rs.addRule( MEL, [NOTE] )
  rs.addRule( MEL, [DOT] )
  #rs.addRule( MEL, [PIPE] )
    
  rs.addRule( MEL, [LOCK,MEL] )
  #rs.addRule( MEL, [MEL,UNTILEND] )
    
  # melody operators
  rs.addRule( MEL, [MEL, INT] ) # octave transpose
  #rs.addRule( MEL, [MEL, SHARP], [INT] ) # transpose up by 1
  #rs.addRule( MEL, [MEL, SHARP, INT] ) # transpose by different amount
  rs.addRule( MEL, [MEL, OP, INT] )
  rs.addRule( MEL, [MEL, OP, FRAC] )
  rs.addRule( MEL, [MEL, OP, MEL] )
  rs.addRule( MEL, [MEL, OP, INTARRAY] )
  rs.addRule( MEL, [MEL, UNOP], [INT] )
  rs.addRule( MEL, [MEL, UNOP, INT] )
  #rs.addRule( MEL, [MEL, UNOP, INTRANGE] )
  
  # melody sequencing
  rs.addAdoptionRule( MELS, \
   [MELS, MEL], \
   [OP,UNOP,INT] )
  rs.addRule( MELS, MEL, \
   [OP,UNOP,INT,EOF] )
    
  # brackets and parentheses
  rs.addGenRule( INTS, LBRACK, [], [INT] )
  rs.addGenRule( INTS, LPAREN, [], [INT] )
  rs.addGenRule( MELS, LBRACK )
  rs.addGenRule( MELS, LPAREN )
  rs.addGenRule( MELS, PIPE )
  
  rs.addRule( MEL, [LBRACK, MELS, RBRACK] )
  rs.addRule( MEL, [LPAREN, MELS, RPAREN] )
 
  rs.addRule( MEL, [LBRACK, MELS, PIPE, MELS, RBRACK] )
  rs.addRule( MEL, [LPAREN, MELS, PIPE, MELS, RPAREN] )
  
  rs.addRule( INTARRAY, \
   [LBRACK,INTS,RBRACK] )
  rs.addRule( INTARRAY, \
   [LPAREN,INTS,RPAREN] )
   
  #rs.addRule( DASHINT, \
  # [DASH,INT] )
  #rs.addRule( INTRANGE, \
  # [INT,DASHINT] )
  #rs.addAdoptionRule( INTRANGE, \
  # [INTRANGE, DASHINT] )
  rs.addAdoptionRule( INTS, \
   [INTS, INT] )
  rs.addAdoptionRule( INTS, \
   [INTS, DASH] )
  
  return rs
    