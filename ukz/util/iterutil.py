
def cartProd(*lists):
    if not lists:
        yield ()
        return
    # Must cache list so you do not try
    # to iterate this twice
    yss = list(cartProd(*lists[1:]))
    for x in lists[0]:
        for yt in yss:
            zt = (x,) + yt
            yield zt

def intsFromTo(a,b):
        if a<=b:
                return range(a,b+1)
        else:
                return range(a,b-1,-1)

def groupWithStateModifier( \
  isModifierFunc, stateFunc, ls):
    acc = []
    st = None
    for x in ls:
        if isModifierFunc(x):
            if acc:
                yield (st,acc)
                acc = []
            st = stateFunc(x)
        else:
            acc.append(x)
    if acc:
        yield (st,acc)
