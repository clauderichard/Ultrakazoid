
from ukz.uklr import *
from .states import *
from .melodyopmap import \
 ukzMelodyUnOpMap

def trimOp(op):
  i = 0
  while i < len(op) and op[i]=='@':
    i += 1
  return op[i:]

def processToken(t):
  if t.type == OP:
    if ukzMelodyUnOpMap.get(\
     trimOp(t.value),None) \
     is not None:
      t.type = UNOP
  return t
