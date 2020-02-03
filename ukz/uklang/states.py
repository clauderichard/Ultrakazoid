
# State numbers in the UKZ tokenizer automaton
EMPTY = 0
NOTE = 1
INT = 2
FRAC = 3
DOT = 4
EXCL = 5
AT = 6
OP = 7
UNOP = 23
#SHARP = 16
VAR = 8
LBRACK = 9
RBRACK = 10
LPAREN = 11
RPAREN = 12
PROPNAME = 13
PIPE = 14
LOCK = 15
INTRANGE = 24
DASH = 25
INTRANGES = 26
INTARRAY = 27
DASHINT = 28
INTS = 29
#UNTILEND = 17
# This is for the parser only
# (not for leaves in the parse tree, only for other nodes)
MEL = 100
MELS = 101

class UkzStates:
    stateStrings = {
        EMPTY: "EMPTY",
        NOTE: "NOTE",
        INT: "INT",
        FRAC: "FRAC",
        DOT: "DOT",
        EXCL: "EXCL",
        AT: "AT",
        OP: "OP",
        VAR: "VAR",
        LBRACK: "LBRACK",
        RBRACK: "RBRACK",
        LPAREN: "LPAREN",
        RPAREN: "RPAREN",
        MEL: "MEL",
        MELS: "MELS"
    }

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
#def isPitchModifier(s):
#    return isDigit(s) or s == "#"

