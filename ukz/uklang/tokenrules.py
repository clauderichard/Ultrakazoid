from ukz.uklr import *
from ukz.uklang.states import *

# Make the UKZ tokenizer automaton
def mkUkzTkAutomaton():
    a = TkAutomaton(EMPTY)
    
    # silence
    a.addTransition(EMPTY, ".", DOT)
    
    # empty melody
    a.addTransition(EMPTY, "|", PIPE)
    
    a.addTransition(EMPTY, "&", LOCK)
    a.addTransition(EMPTY, "¬", UNTILEND)
    
    # notes
    #noteModifiers = "#°"
    a.addTransition(EMPTY, pitchChars, NOTE)
    #a.addTransition(NOTE, isDigit, NOTE)
    #a.addTransition(NOTE, noteModifiers, NOTE)
    
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
    a.addTransition(EMPTY, "#^v", SHARP)
    opChars = "+-*/%=°xX<>$_~o"
    a.addTransition(EMPTY, "@", AT)
    a.addTransition(AT, "@", AT)
    a.addTransition(EMPTY, "!", EXCL)
    a.addTransition(AT, "!", EXCL)
    for state in [EMPTY,EXCL,AT]:
        a.addTransition(state, opChars, OP)
    # multi-char operators dealt with here!
    a.addTransition(OP, opChars, OP)
    
    # property setting
    a.addTransition(EXCL, isAlphaNumeric, PROPNAME)
    a.addTransition(PROPNAME, isAlphaNumeric, PROPNAME)
    a.addTransition(PROPNAME, opChars, OP)
    
    ## variables
    #a.addTransition(EMPTY, "$", VAR)
    #a.addTransition(VAR, isAlphaNumeric, VAR)

    # DONE!
    return a
