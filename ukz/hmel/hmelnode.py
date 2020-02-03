from abc import abstractmethod
from .hmel import Hmel

################################

class HmelNode(Hmel):
  
  def __init__(self):
    Hmel.__init__(self)
  def copyFrom(self,other):
    Hmel.copyFrom(self,other)

################################
# Abstract methods

  @abstractmethod
  def allChildren(self):
    pass

  @abstractmethod
  def mapChildren(self,f):
    pass

  @abstractmethod
  def filterChildren(self,f):
    pass

################################

  def getDescendants(self,d):
    if d==0:
      yield self
    else:
      for c in self.allChildren():
        for x in c.getDescendants(d-1):
          yield x
  
  def allLeaves(self):
    for c in self.allChildren():
      for x in c.allLeaves():
        yield x
  def allNotes(self):
    for c in self.allChildren():
      for x in c.allNotes():
        yield x
        
  def mapLeaves(self,f):
    return self.mapChildren(lambda c: c.mapLeaves(f))
  def mapNotes(self,f):
    return self.mapLeaves(lambda x: \
     f(x) if x.isHmelNote() else x)
    
  def replaceDescendants(self,d,f):
    if d==0:
      return f(self)
    else:
      return self.mapChildren(lambda c: \
       c.replaceDescendants(d-1,f))
      
  def filterDescendants(self,d,f):
    if d==0:
      return self if f(self) \
       else None
    else:
      self.mapChildren(lambda c: c.filterDescendants(d-1,f))
      self.filterChildren(lambda x: x is not None)
      for _ in self.allChildren():
        return self
      return None
      
################################
