
# the kind of trans used in parser's
# auto bwl generator.
# This file is not used yet,
class Trans:
    
  def __init__(self):
    self.t = {}
  def copy(self):
    t = Trans()
    for (a,b) in self.t.items():
      t.t[a] = b.copy()
    return t
    
  def add(self,a,b):
    x = self.t.get(a,None)
    if x is None:
      self.t[a] = set([b])
      return True
    if b in x:
      return False
    x.add(b)
    return True
    
  def extend(self,o):
    ch = False
    for (a,xs) in self.t.items():
      xsx = set()
      for b in xs:
        ys = o.t.get(b,None)
        if ys is None:
          o.t[b] = set()
          ys = o.t[b]
        for y in ys:
          if y not in xs:
            ch = True
            xsx.add(y)
      for x in xsx:
        xs.add(x)
    for (b,ys) in o.t.items():
      if b not in aa:
        self.t[b] = ys.copy()
        self.t[b].add(b)
        ch = True
    return ch
    
  def extendInf(self):
    chInf = False
    while True:
      t = {}
      for (a,xs) in self.t.items():
        t[a] = xs.copy()
      ch = self.transAdd(self.t,t)
      if not ch:
        return chInf
      chInf = True
    
