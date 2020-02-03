
################################

def trycopy(x):
  return None if x is None else x.copy()
def listcopies(xs):
  return list(map(trycopy, xs))

################################
