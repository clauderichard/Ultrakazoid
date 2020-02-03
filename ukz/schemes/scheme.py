from random import *

class Scheme:
    def readValue(self):
        raise StopIteration
    #def __iter__(self):
    #    return iter(self.readValue())
    def __add__(self,other):
        return Funcv(lambda x,y: x+y, self, other)
    def __sub__(self,other):
        return Funcv(lambda x,y: x-y, self, other)
    def __mul__(self,other):
        return Funcv(lambda x,y: x*y, self, other)
    def __matmul__(self,other):
        return Funcv(lambda x,y: x@y, self, other)
    def __truediv__(self,other):
        return Funcv(lambda x,y: x/y, self, other)
    def __floordiv__(self,other):
        return Funcv(lambda x,y: x//y, self, other)
    def __mod__(self,other):
        return Funcv(lambda x,y: x%y, self, other)
    def __divmod__(self,other):
        return Funcv(lambda x,y: divmod(x,y), self, other)
    def __pow__(self,other):
        return Funcv(lambda x,y: x**y, self, other)
    def __lshift__(self,other):
        return Funcv(lambda x,y: x<<y, self, other)
    def __rshift__(self,other):
        return Funcv(lambda x,y: x>>y, self, other)
    def __and__(self,other):
        return Funcv(lambda x,y: x&y, self, other)
    def __xor__(self,other):
        return Funcv(lambda x,y: x^y, self, other)
    def __or__(self,other):
        return Funcv(lambda x,y: x|y, self, other)
    def __lt__(self,other):
        return Funcv(lambda x,y: x<y, self, other)
    def __le__(self,other):
        return Funcv(lambda x,y: x<=y, self, other)
    def __eq__(self,other):
        return Funcv(lambda x,y: x==y, self, other)
    def __ne__(self,other):
        return Funcv(lambda x,y: x!=y, self, other)
    def __gt__(self,other):
        return Funcv(lambda x,y: x>y, self, other)
    def __ge__(self,other):
        return Funcv(lambda x,y: x>=y, self, other)
    def __getitem__(self,other):
        return Funcv(lambda x,y: x[y], self, other)

def repeat(val):
    while True:
        yield value(val)

def value(v):
    if isinstance(v,Scheme):
        return v.readValue()
    return v

class Val(Scheme):
    def __init__(self,val):
        self.val = val
    def setValue(self,val):
        self.val = val
    def readValue(self):
        return value(self.val)

class Listv(Scheme):
    def __init__(self,vals):
        self.vals = vals
        self.it = None
    def reset(self):
        self.it = iter(value(self.vals))
    def readValue(self):
        if not self.it:
            self.reset()
            return value(next(self.it))

class Cyclev(Scheme):
    def __init__(self,vals):
        self.vals = vals
        self.it = None
        self.lst = []
        self.mustAppend = True
    def reset(self):
        self.it = iter(self.lst)
        self.mustAppend = False
    def readValue(self):
        if not self.it:
            self.it = iter(self.vals)
        try:
            v = value(next(self.it))
            if self.mustAppend:
                self.lst.append(v)
            return v
        except StopIteration:
            self.reset()
            v = value(next(self.it))
            return v
        
class Concatv(Scheme):
    def __init__(self,vals):
        self.vals = vals
        self.it = None
        self.val = None
    def reset(self):
        self.it = None
        self.val = None
    def initList(self):
        self.it = \
         iter(value(self.vals))
    def nextVal(self):
        self.val = next(self.it)
    def readValue(self):
        if not self.it:
            self.initList()
            self.nextVal()
        while True:
            try:
                return \
                 value(self.val)
            except StopIteration:
                self.nextVal()
            
class Iterv(Scheme):
    def __init__(self,f,initVal):
        self.f = f
        self.initVal = initVal
        self.isFirst = True
        self.prevVal = None
    def readValue(self):
        if self.isFirst:
            self.prevVal = \
             value(self.initVal)
            self.isFirst = False
        else:
            ff = value(self.f)
            ffv = ff\
             (self.prevVal)
            vffv = value(ffv)
            self.prevVal = \
             vffv
            #print(ff)
            #print(ffv)
            #print(vffv)
        #print(self.prevVal)
        return self.prevVal

class Randv(Scheme):
    def __init__(self,vals):
        self.vals = vals
    def readValue(self):
        vals = value(self.vals)
        if not isinstance(vals,list):
            vals = list(vals)
        return value(vals[ \
        	randint(0,len(vals)-1)
        	])

class Ifv(Scheme):
    def __init__(self,\
    	cond,trueVal,falseVal):
        self.cond = cond
        self.trueVal = trueVal
        self.falseVal = falseVal
    def readValue(self):
        if value(self.cond):
            return value(self.trueVal)
        else:
            return value(self.falseVal)

class Funcv(Scheme):
    def __init__(self,f,*args):
        self.f = f
        self.args = args
    def readValue(self):
        vargs = map(value,self.args)
        return self.f(*vargs)

class Cachev(Scheme):
    def __init__(self,\
    	val,initCachedVal=None):
        self.val = val
        self.uncached = True
        self.cachedVal = \
         value(initCachedVal)
    def readValue(self):
        if self.uncached:
            self.refresh()
            self.uncached = False
        return self.cachedVal
    def refresh(self):
        self.cachedVal = \
         value(self.val)

class Atv(Scheme):
    def __init__(self,arr,index):
        self.array = arr
        self.index = index
    def readValue(self):
        a = value(self.array)
        i = value(self.index)
        return a[i]
