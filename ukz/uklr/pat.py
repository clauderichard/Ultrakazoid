from ukz.utils import union,dedup

def fst(ls,defaul=None):
  it = iter(ls)
  try:
    x = next(it)
    return x
  except StopIteration:
    return defaul

class Pat:
  def __init__(self):
    return
  def pmLength(self,pm):
    if isinstance(pm,list):
      s = 0
      for x in pm:
        if isinstance(x,list):
          s += self.pmLength(x)
        elif isinstance(x,int):
          s += x
        else:
          raise ValueError("what!!!!")
      return s
      #return sum(lambda x: \
      # x if not isinstance(x,list) \
      # else self.pmLength(x), pm)
    else:
      return pm
  def __repr__(self):
    return str(self)
    
  def reverse(self):
    pass
  def pairs(self):
    return list(dedup(self.pairs_h()))
    
    
class PatSingle(Pat):
    
  def __init__(self,val):
    Pat.__init__(self)
    self.val = val
  def __str__(self):
    return f"{self.val}"
  def copy(self):
    return PatSingle(self.val)
  def __eq__(self,other):
    return isinstance(other,PatSingle) \
     and self.val == other.val
  
  def match(self,stack):
    if fst(stack) == self.val:
      return 1
    else:
      return None
      
  def heads(self):
    return [self.val]
  def tails(self):
    return [self.val]
  def pairs_h(self):
    return []
        
        
class PatAlt(Pat):
  
  def __init__(self,opts):
    Pat.__init__(self)
    self.opts = list(map(lambda o: \
     o.copy() if isinstance(o,Pat) \
     else PatSingle(o), opts))
  def copy(self):
    return PatAlt(map(lambda o: \
     o.copy(), self.opts))
  def __str__(self):
    s = f"({self.opts[0]}"
    for o in self.opts[1:]:
      s += f"|{o}"
    return s + ")"
  def __eq__(self,other):
    return isinstance(other,PatAlt) \
     and self.opts == other.opts

  def reverse(self):
    for o in self.opts:
      o.reverse()
    
  def match(self,stack):
    for o in self.opts:
      x = o.match(stack)
      if x is not None:
        return x
    return None
    
  def heads(self):
    xs = []
    for o in self.opts:
      xs = union(xs,o.heads())
    return list(xs)
  def tails(self):
    xs = []
    for o in self.opts:
      xs = union(xs,o.tails())
    return list(xs)
  def pairs_h(self):
    for o in self.opts:
      for p in o.pairs():
        yield p


class PatMaybe(Pat):
  
  def __init__(self,opt):
    Pat.__init__(self)
    self.opt = opt.copy() \
     if isinstance(opt,Pat) \
     else PatSingle(opt)
  def copy(self):
    return PatMaybe(self.opt.copy())
  def __str__(self):
    return f"[{self.opt}]"
  def __eq__(self,other):
    return isinstance(other,PatMaybe) \
     and self.opt == other.opt

  def reverse(self):
    self.opt.reverse()
    
  def match(self,stack):
    x = self.opt.match(stack)
    if x is not None:
      return x if x else 0
    return 0
    
  def heads(self):
    return self.opt.heads()
  def tails(self):
    return self.opt.tails()
  def pairs_h(self):
    return self.opt.pairs()
  

class PatStar(Pat):
    
  def __init__(self,pat):
    Pat.__init__(self)
    self.pat = pat.copy()
  def __str__(self):
    return f"{self.pat}*"
  def copy(self):
    return PatStar(self.pat.copy())
  def __eq__(self,other):
    return isinstance(other,PatStar) \
     and self.pat == other.pat

  def reverse(self):
    self.pat.reverse()
  
  def match(self,stack):
    ind = 0
    x = []
    while True:
      p = self.pat.match(stack[ind:])
      if p is None or not p or p==0:
        return x
      l = self.pmLength(p)
      ind += l
      x.insert(0,p)
    return x
  
  def heads(self):
    return self.pat.heads()
  def tails(self):
    return self.pat.tails()
  def pairs_h(self):
    for x in self.pat.pairs():
      yield x
    for t in self.pat.tails():
      for h in self.pat.heads():
        yield (t,h)


class PatPlus(Pat):
    
  def __init__(self,pat):
    Pat.__init__(self)
    self.pat = pat.copy()
  def __str__(self):
    return f"{self.pat}+"
  def copy(self):
    return PatPlus(self.pat.copy())
  def __eq__(self,other):
    return isinstance(other,PatPlus) \
     and self.pat == other.pat

  def reverse(self):
    self.pat.reverse()
  
  def match(self,stack):
    p = self.pat.match(stack)
    if p is None or not p or p==0:
      #print (f"rudg{stack}")
      return None
    l = self.pmLength(p)
    x = self.match(stack[l:])
    if x is None:
      return [p]
    x.insert(0,p)
    return x
    
  def heads(self):
    return self.pat.heads()
  def tails(self):
    return self.pat.tails()
  def pairs_h(self):
    for x in self.pat.pairs():
      yield x
    for t in self.pat.tails():
      for h in self.pat.heads():
        yield (t,h)

    
class PatSeq(Pat):

  def __init__(self,seq):
    Pat.__init__(self)
    self.seq = list(map(lambda x: \
     x.copy() if isinstance(x,Pat) \
     else PatSingle(x), seq))
  def __str__(self):
    return f"{self.seq}"
  def copy(self):
    return PatSeq(map(lambda x: \
     x.copy(), self.seq))
  def __eq__(self,other):
    return isinstance(other,PatSeq) \
     and self.seq == other.seq

  def reverse(self):
    for x in self.seq:
      x.reverse()
    self.seq.reverse()
     
  def match(self,stack):
    return self.match_h(stack,0)
     
  def match_h(self,stack,ind):
    if ind==len(self.seq):
      return []
    x = self.seq[ind].match(stack)
    if x is None:
      return None
    if isinstance(x,int) or isinstance(x,list):
      xl = self.pmLength(x)
      y = self.match_h(stack[xl:],ind+1)
      if y is None:
        return None
      return [x] + y
    else:
      raise "eee"
      
  def heads(self):
    return self.seq[0].heads()
  def tails(self):
    return self.seq[len(self.seq)-1].tails()
  def pairs_h(self):
    for x in self.seq:
      for y in x.pairs():
        yield y
    for i in range(1,len(self.seq)):
      x = self.seq[i-1]
      y = self.seq[i]
      for tx in x.tails():
        for hy in y.heads():
          yield (tx,hy)
    return []
    
        
class PatFlatSeq(Pat):

  def __init__(self,seq):
    Pat.__init__(self)
    self.seq = list(seq)
    self.n = len(self.seq)
  def __str__(self):
    return f"{self.seq}"
  def copy(self):
    return PatFlatSeq(map(lambda x:x, self.seq))
  def reverse(self):
    self.seq.reverse()
  def __eq__(self,other):
    return isinstance(other,PatFlatSeq) \
     and self.seq == other.seq \
     and self.n == other.n
     
  def match(self,stack):
    if len(stack) < self.n:
      return None
    for (x,y) in zip(stack,self.seq):
      if x != y:
        return None
    return [1]*self.n
    
  def heads(self):
    return [self.seq[0]]
  def tails(self):
    return [self.seq[len(self.seq)-1]]
  def pairs_h(self):
    for i in range(1,len(self.seq)):
      yield (self.seq[i-1],self.seq[i])


def maybe(opt):
  return PatMaybe(opt)
def alt(*opts):
  if isinstance(opts[0],list):
    return PatAlt(opts[0])
  return PatAlt(opts)
def star(x):
  return PatStar(x \
   if isinstance(x,Pat) else PatSingle(x))
def plus(x):
  return PatPlus(x \
   if isinstance(x,Pat) else PatSingle(x))
def seq(*xs):
  for x in xs:
    if isinstance(x,Pat):
      return PatSeq(xs)
  return PatFlatSeq(xs)
