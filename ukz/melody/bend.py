class BendVertex:

  def __init__(self,time,val):
    self.t = time
    self.v = val
  def copy(self):
    return BendVertex(self.t,self.v)
  def __eq__(self,other):
    return self.t == other.t \
     and self.v == other.v

class Bend:
    
  def __init__(self,vertices=[]):
    self.vs = list(vertices)
  def copy(self):
    return Bend( \
     map(lambda v: v.copy(),\
     self.vs))
  def __eq__(self,other):
    return self.vs == other.vs
