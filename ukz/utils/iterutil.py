
def cartProd(*lists):
  if not lists:
    yield ()
    return
  for x in lists[0]:
    for yt in cartProd(*lists[1:]):
      zt = (x,) + yt
      yield zt

def intsFromTo(a,b):
    if a<=b:
        return range(a,b+1)
    else:
        return range(a,b-1,-1)

def cycle(ls):
  xs = []
  # build list on first iteration
  for x in ls:
    xs.append(x)
    yield x
  # use previously-built list
  while True:
    for x in xs:
      yield x
      
def union(xs,ys):
  x = sorted(list(xs))
  m = len(x)
  y = sorted(list(ys))
  n = len(y)
  i = 0
  j = 0
  while i<m and j<n:
    if x[i] < y[j]:
      yield x[i]
      i += 1
    elif x[i] > y[j]:
      yield y[j]
      j += 1
    else:
      yield x[i]
      i += 1
      j += 1
  while i<m:
    yield x[i]
    i += 1
  while j<n:
    yield y[j]
    j += 1
    
def dedup(xs):
  ls = sorted(xs)
  x = None
  for y in ls:
    if y != x:
      yield y
      x = y
    
