
class StringMatcher:
    
  def __init__(self):
    self.vals = {}
    
  def __getitem__(self,index):
    terms = index.split(' ')
    for name,num in \
     self.vals.items():
      good = True
      for term in terms:
        if term not in name.lower():
          good = False
          break
      if good:
        return num
    raise ValueError(f'Could not find key matching {index}')
