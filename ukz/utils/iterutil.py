
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
