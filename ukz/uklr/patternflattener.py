from .pattern import *

################################################
# Examples:
################################
# a <- bc
################################
# a <- b c+          lambda b,cs: f(b,cs)
#   b_cs <- b c      lambda b,c: [b,[c]]
#   b_cs <- b_cs c   lambda b_cs,c: b_cs[1].append(c); return b_cs
#   a <- b_cs        lambda b_cs: f(*b_cs)
################################
# a <- b c*          lambda b,cs: f(b,cs)
#   b_cs <- b        lambda b: [b,[]]
#   b_cs <- b_cs c   lambda b_cs,c: b_cs[1].append(c); return b_cs
#   a <- b_cs        lambda b_cs: f(*b_cs)
################################
# a <- b c* d        lambda b,cs: f(b,cs)
#   b_cs <- b        lambda b: [b,[]]
#   b_cs <- b_cs c   lambda b_cs,c: b_cs[1].append(c); return b_cs
#   a <- b_cs d      lambda b_cs,d: f(*b_cs,d)
################################
# a <- b c d* e
#   b_c_ds <- b c        lambda b,c: [b,c,[]]
#   b_c_ds <- b_c_ds d   lambda b_c_ds,d: b_cs[2].append(d); return b_c_ds
#   a <- b_c_ds e        lambda b_c_ds,e: f(*b_c_ds,e)
################################
# a <- b (c|d)* e
#   b_cds <- b          lambda b: [b,[]]
#   b_cds <- b_cds c    lambda b_cds,c: b_cs[1].append(c); return b_cds
#   b_cds <- b_cds d    lambda b_cds,d: b_cs[1].append(d); return b_cds
#   a <- b_c_ds e       lambda b_cds,e: f(*b_cds,e)
################################
# a <- b (c|d)* e* f      lambda b,cds,es,f: g(b,cds,es,f)
#   b_cds <- b            lambda b: [b,[]]
#   b_cds <- b_cds c      lambda b_cds,c: b_cs[1].append(c); return b_cds
#   b_cds <- b_cds d      lambda b_cds,d: b_cs[1].append(d); return b_cds
#   b_cds_es <- b_cds     lambda b_cds: [b_cds[0],b_cds[1],[]]
#   b_cds_es <- b_cd_es     lambda b_cds: [b_cds[0],b_cds[1],[]]
#   a <- b_cds_es f       lambda b_cds_es,f: g(*b_cds_es,f)
################################
# a <- b c d*             lambda b,c,ds: f(b,c,ds)
#   b_c_ds <- b c         lambda b,c: [b,c,[]]      
#                              star rule: lambda args: args in a list followed by []
#   b_c_ds <- b_c_ds d    lambda b_c_ds,d: b_c_ds[2].append(d); return b_c_ds
#                              star rule: lambda ls,el: ls[lastofls].append(el); return ls
#   a <- b_c_ds           lambda b_c_ds: f(*b_c_ds)
#                              final rule: lambda args,rest...: f(*args,*rest)
################################
# a <- b (c|d) e*         lambda b,cd,es: f(b,cd,es)
#   a <- b c e*           lambda b,c,es: f(b,c,es)   == f
#     b_cd_es <- b c        lambda b,c: [b,c,[]]
#     b_c_es <- b_c_es e  lambda b_c_es,e: b_c_es[2].append(e); return b_c_es
#   a <- b d e*           lambda b,d,es: f(b,d,es)   == f
#     b_cd_es <- b d        lambda b,d: [b,d,[]]
#     b_d_es <- b_d_es e  lambda b_d_es,e: b_d_es[2].append(e); return b_d_es
#   a <- b_cd_es          lambda b_cd_es: f(*b_cd_es)
################################
        
################################################

class PatAccumulator:
    acc = [""]

    @classmethod
    def newacc(cls,x):
        na = cls.acc[len(cls.acc)-1] + x
        cls.acc.append(na)
        return na
    @classmethod
    def delacc(cls):
        del cls.acc[len(cls.acc)-1]

def starListRule1(*args):
    return (*args,[])
def plusListRule1(*args):
    a = args[0:len(args)-1]
    x = args[len(args)-1]
    return (*a,[x])
def appendToLastList(arglist,el):
    arglist[len(arglist)-1].append(el)
    return arglist

def flattenedRules(resultType,patternPieces,resultFunc):
    return list(flattenedRules_h(resultType,patternPieces,resultFunc,0))

def flattenedRules_h(resultType,patternPieces,resultFunc,index):
    if index >= len(patternPieces):
        yield (resultType,patternPieces,resultFunc)
        return
    p = patternPieces[index]
    if isinstance(p,PatOr):
        for o in p.options:
            newPatternPieces = patternPieces[0:index] + [o] + patternPieces[index+1:]
            yield from flattenedRules_h(resultType,newPatternPieces,resultFunc,index)
    elif isinstance(p,PatStar):
        o = p.elmt
        lsType = PatAccumulator.newacc(f"_{o}s")
        yield from flattenedRules_h(lsType,[lsType,o],appendToLastList,1)
        yield from flattenedRules_h(lsType, patternPieces[0:index], starListRule1,index)
        newPatternPieces = [lsType] + patternPieces[index+1:]
        newResFun = lambda ls,*args: resultFunc(*ls,*args)
        yield from flattenedRules_h(resultType,newPatternPieces,newResFun,1)
        PatAccumulator.delacc()
    elif isinstance(p,PatPlus):
        o = p.elmt
        lsType = PatAccumulator.newacc(f"_{o}s")
        yield from flattenedRules_h(lsType,[lsType,o],appendToLastList,1)
        yield from flattenedRules_h(lsType,patternPieces[0:index]+[o], plusListRule1,index)
        newPatternPieces = [lsType] + patternPieces[index+1:]
        newResFun = lambda ls,*args: resultFunc(*ls,*args)
        yield from flattenedRules_h(resultType,newPatternPieces,newResFun,1)
        PatAccumulator.delacc()
    else:
        lsType = PatAccumulator.newacc(f"_{patternPieces[index]}")
        yield from flattenedRules_h(resultType,patternPieces,resultFunc,index+1)
        PatAccumulator.delacc()

################################################



