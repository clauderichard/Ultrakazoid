
# State numbers in the UKZ tokenizer automaton
EMPTY = 0
NOTE = 1
INT = 2
FRAC = 3
DOT = 4
EXCL = 5
AT = 6
OP = 7
VAR = 8
LBRACK = 9
RBRACK = 10
LPAREN = 11
RPAREN = 12
PROPNAME = 13
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

def isSmallAlpha(s):
    c = ord(s)
    return c >= ord('a') and c <= ord('z') and c != ord('x')
def isBigAlpha(s):
    c = ord(s)
    return c >= ord('A') and c <= ord('Z') and c != ord('X')
def isAlpha(s):
    return isSmallAlpha(s) or isBigAlpha(s)
def isDigit(s):
    c = ord(s)
    return c >= ord('0') and c <= ord('9')
def isAlphaNumeric(s):
    return isAlpha(s) or isDigit(s)
def isPitchModifier(s):
    return isDigit(s) or s == "#"

