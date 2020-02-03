from random import *

class Scheme:
    def readValue(self):
        raise StopIteration
    def __iter__(self):
        return iter(self.readValue())
    def __add__(self,other):
        return Funcv(\
        	__add__,self,other)
    def __sub__(self,other):
        return Funcv(\
        	__sub__,self,other)
    def __mul__(self,other):
        return Funcv(\
        	__mul__,self,other)
    def __getitem__(self,index):
        return Atv(\
        	self,index)

def iterValues(val):
    while True:
        yield value(val)

def value(v):
    if isinstance(v,Scheme):
        return v.readValue()
    return v
