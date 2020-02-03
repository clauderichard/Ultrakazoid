
class BlackList:
    
  def __init__(self,ls):
    self.ls = set(ls)
    
  def isBanned(self,x):
    return x in self.ls
  
    
class WhiteList:
    
  def __init__(self,ls):
    self.ls = set(ls)
    
  def isBanned(self,x):
    return self.ls and \
     x not in self.ls


def blacklist(x):
  return BlackList(x \
   if isinstance(x,list) else [x])
def whitelist(x):
  return WhiteList(x \
   if isinstance(x,list) \
   else x if isinstance(x,set) \
   else [x])
