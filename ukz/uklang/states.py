
# State numbers in the UKZ tokenizer automaton
class StateCount:
  stateCount = 0

def st():
  StateCount.stateCount += 1
  return StateCount.stateCount

# empty state
EMPTY = st()

# primitives
PITCH = st()
INT = st()
FRAC = st()
DOT = st()

# operators
EXCL = st()
AT = st()
FOR = st()
OP = st()
UNOP = st()
TRANSPOSE = st()

# brackets
LBRACK = st()
RBRACK = st()
LPAREN = st()
RPAREN = st()
PIPE = st()

# melody components
MEL = st()
#MELS = st()

# ranges
DASH = st()
#TOPITCH = st()
PITCHES = st()

# int ranges
#INTRANGE = st()
#INTRANGES = st()
INTARRAY = st()
#DASHINT = st()
#INTS = st()

# Unused right now...
#PROPNAME = st()
#LOCK = st()
#VAR = st()

