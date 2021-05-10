

# Represents a bi-directional map
# many-to-many.
# Like a sparse matrix if you will.
class MultiMap:

    def __init__(self):
        self.mapatob = {}
        self.mapbtoa = {}

    def __addOne(self,m,x,y):
        if m.get(x,None) is None:
            m[x] = set()
        m[x].add(y)

    def add(self,a,b):
        self.__addOne(self.mapatob,a,b)
        self.__addOne(self.mapbtoa,b,a)

    def atob(self,a):
        return self.mapatob.get(a,set())
    def btoa(self,b):
        return self.mapbtoa.get(b,set())
        