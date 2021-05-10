
class StringMatcher:
        
    def __init__(self,vals):
        self.vals = vals
        
    def __matchTerms(self,terms):
        for name,num in self.vals.items():
            good = True
            for term in terms:
                if f"{term}" not in name.lower():
                    good = False
                    break
            if good:
                return num
        raise ValueError(f'Could not find key matching terms {terms}')
        
    def __getitem__(self,index):
        if isinstance(index,str):
            terms = index.split(' ')
            return self.__matchTerms(terms)
        elif isinstance(index,list):
            return self.__matchTerms(index)
