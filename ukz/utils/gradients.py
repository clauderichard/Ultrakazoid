
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
