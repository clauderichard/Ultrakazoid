class Tone:
  
  def __init__(self,p=0,l=5,\
   pl=False,ll=False):
    self.p = p
    self.l = l
    self.pl = pl
    self.ll = ll
  def copy(self):
    return Tone(self.p,self.l,\
     self.pl,self.ll)
  def __str__(self):
    return f"({self.p},{self.l})"

  def transposeUp(self,dp):
    if self.pl:
      return
    self.p += dp
  def transposeDown(self,dp):
    if self.ll:
      return
    self.transposeUp(-dp)
  def blendWithLoudness(self,l=5):
    if self.ll:
      return
    self.l += (l-5)
    
  def lockP(self):
    self.pl = True
  def lockL(self):
    self.ll = True
