
def cubGradPts(t1,t2,v1,v2):
  a = 4*(t2-t1)/(v2-v1)**3
  mv = (v1+v2)/2
  mt = (t1+t2)/2
  vs = range(v1,v2+1) if v2>v1 \
   else reversed(list(\
   range(v2,v1+1)))
  for v in vs:
    t = a * (v-mv)**3 + mt
    yield (t,v)
def polGradPts(e,t1,t2,v1,v2):
  dt2 = (t2-t1)/2
  dv2 = (v2-v1)/2
  mv = (v1+v2)/2
  mt = (t1+t2)/2
  a = dt2/dv2**e
  vs = range(v1,v2+1) if v2>v1 \
   else reversed(list(\
   range(v2,v1+1)))
  for v in vs:
    t = a * (v-mv)**e
    if (v<mv) == (v2>v1):
      t = -abs(t)
    t = t + mt
    yield (t,v)
    
    
  if v2>v1:
    return CubicGradient(\
    	t1,t2,v1,v2).points()
  return CubicGradient(\
   t1,t2,v2,v1).points()

class CubicGradient:

  def __init__(self,\
  	 mint,maxt,minv,maxv):
    self.mint = mint
    self.maxt = maxt
    self.minv = minv
    self.maxv = maxv

  def points(self):
    t1 = self.mint
    t2 = self.maxt
    v1 = self.minv
    v2 = self.maxv
    a = 4*(v2-v1)/(t2-t1)**3
    mt = (t1+t2)/2
    for t in range(t1,t2+1):
      v = a * (t-mt)**3 + (v2+v1)/2
      yield (t,v)