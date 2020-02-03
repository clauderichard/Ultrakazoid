from .tokenizer import TkToken
from .pat import *
from .restriction import *

# Parser node types (only generic ones included here)
BOF = -2
EOF = -1

class PrRule:
    
  def __init__(self,resultType,\
   pattern,\
   travFunc):
    self.l = resultType
    self.travFunc = travFunc
    self.bwl = blacklist([])
    self.pat = seq(*pattern) \
     if isinstance(pattern,list) \
     else pattern.copy() \
     if isinstance(pattern,Pat) \
     else PatSingle(pattern)
    self.pat.reverse()
    
  def applyPatMatch(self,pm,stack,restyp):
    newCs = []
    pmm = pm if isinstance(pm,list) else [pm]
    for n in pmm:
      if isinstance(n,int) and n==1:
        nnn = stack[0:n]
        del stack[0:n]
        newCs.insert(0,nnn[0].value)
      elif isinstance(n,list):
        x = self.applyPatMatch(n,stack,None)
        newCs.insert(0,x.value)
      else:
        raise Exception("bad pattern match format?!")
    if restyp is None:
      return TkToken(restyp,newCs)
    else:
      #print(f"newCs {newCs} restyp {restyp}")
      return TkToken(restyp,\
       self.travFunc(*newCs))
    
  def tryReduce(self,stack,nex,st):
    if nex is not None and \
     self.bwl is not None and \
     self.bwl.isBanned(nex.type):
      return False
    pm = self.pat.match(st)
    if pm is None:
      return False
    x = self.applyPatMatch(pm,stack,self.l)
    stack.insert(0,x)
    return True


class PrRules:

  def __init__(self):
    self.leafFuncs = {}
    self.rules = []
    # from stack top to rule list
    # for performance
    self.ruleMap = {}
    
  # func from string to value
  def addLeafFunc(self,typ,func):
    self.leafFuncs[typ] = func

  def addRule(self,\
   resultType,childrenTypes,\
   travFunc):
    # rightR = childrenTypes
    # if not isinstance(childrenTypes,list):
    #   rightR = [childrenTypes]
    # rightR = list(rightR)
    newRule = PrRule(\
     resultType,childrenTypes,\
     travFunc)
    self.rules.append(newRule)

  def mapLeaf(self,tok):
    f = self.leafFuncs.get(tok.type,None)
    if f is None:
      return tok
    else:
      return TkToken(\
       tok.type,f(tok.value))

  def tryReduce(self,stack,nex):
    st = list(map(lambda x:x.type,\
     stack))
    if not st:
      return False
    h = st[0]
    for r in self.ruleMap.get(h,[]):
      if r.tryReduce(stack,nex,st):
        st = list(map(lambda x: x.type,stack))
        #print(f"reduced to {st}")
        return True
    return False
    
  def setTrans(self,t,a,b):
    x = t.get(a,None)
    if x is None:
      t[a] = set()
      t[a].add(b)
      return True
    if b in x:
      return False
    x.add(b)
    return True
  def transHas(self,t,a,b):
    x = t.get(a,None)
    if x is None:
      return False
    return b in x
  def transAdd(self,aa,bb):
    ch = False
    for (a,xs) in aa.items():
      xsx = set()
      for b in xs:
        ys = bb.get(b,None)
        if ys is None:
          bb[b] = set()
          ys = bb[b]
        for y in ys:
          if y not in xs:
            ch = True
            xsx.add(y)
      for x in xsx:
        xs.add(x)
    for (b,ys) in bb.items():
      if b not in aa:
        aa[b] = ys.copy()
        aa[b].add(b)
        ch = True
    return ch
  def transPow(self,aa):
    while True:
      aac = {}
      for (a,xs) in aa.items():
        aac[a] = xs.copy()
      ch = self.transAdd(aa,aac)
      if not ch:
        return
    
  def wlGen(self):
    lx = {}
    xy = {}
    yn = {}
    for rule in self.rules:
      for h in rule.pat.heads():
        self.setTrans(lx,h,rule.l)
      for t in rule.pat.tails():
        self.setTrans(yn,rule.l,t)
      for (f,b) in rule.pat.pairs():
        self.setTrans(xy,b,f)
    self.transPow(lx)
    self.transPow(yn)
    self.transAdd(lx,xy)
    self.transAdd(lx,yn)
    # work with lx now.
    # lx is whitelists
    for rule in self.rules:
      t = lx.get(rule.l,set())
      t.add(EOF)
      rule.bwl = whitelist(t)
    
    
  def initialize(self):
    for r in self.rules:
      for h in r.pat.heads():
        rs = self.ruleMap.get(h,None)
        if rs is None:
          rs = []
          self.ruleMap[h] = rs
        rs.append(r)
    self.wlGen()
    return


class PrRunner:

  def __init__(self,prRules):
    self.prRules = prRules
    self.stack = []
    self.inputs = iter([None])
    self.nextInput = next(self.inputs)

  def initialize(self,tokens):
    self.stack = []
    self.inputs = iter(tokens)
    self.nextInput = next(self.inputs)

  def tryShift(self):
    if self.nextInput is None:
      return False
    newLeaf= self.prRules.mapLeaf(\
     self.nextInput)
    self.stack.insert(0,newLeaf)
    try:
      self.nextInput = next(self.inputs)
    except StopIteration:
      self.nextInput = None
    st = list(map(lambda x: x.type,self.stack))
    #print(f"shifted to {st}")
    return True

  def tryReduce(self):
    return self.prRules.tryReduce(\
    	self.stack,self.nextInput)

  def tokensWithEnds(self,tokens):
    yield TkToken(BOF,None)
    for t in tokens:
        yield t
    yield TkToken(EOF,None)

  def parse(self,tokens):
    self.initialize(self.tokensWithEnds(tokens))
    while True:
      if not self.tryReduce():
        if not self.tryShift():
          break
    if len(self.stack) == 3:
      return self.stack[1]
    else:
      print('not fully parsed! Uh oh... Stack looks like this:')
      print(self.stack)
      return self.stack
      