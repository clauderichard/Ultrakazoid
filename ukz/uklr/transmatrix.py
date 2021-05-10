from math import inf

# Imagine a directed graph represented as a matrix.
# The matrix has nonzero in row i column j
# iff the graph has an edge from vertex i to vertex j.

# adding 2 matrices gets a new graph with
# all the edges from both matrices.

# multiplying matrices means whenever an arrow from
# graph 1 is followed by an arrow in graph 2,
# result has an edge from start of arrow 1
# to end of arrow 2.

# if you take e^M then it's easy if I is included
# in M: Result has arrow from A to B iff you
# can get from A to B following any path of
# arrows in the graph represented by M.
# What if I is not in M? I'm not sure.

class TransMatrix:
    
    def __init__(self,xs={},hasI=False):
        self.xs = {}
        for (x,ys) in xs.items():
            self.xs[x] = set()
            self.xs[x].update(ys)
        self.hasI = hasI
        
    @classmethod
    def eye(cls):
        return TransMatrix({},True)
        
    def __eq__(self,o):
        return self.hasI == o.hasI and self.xs == o.xs
        
    def __getitem__(self,x):
        return self.xs.get(x,set())
        
    def items(self):
        return self.xs.items()
        
    def __mkYs(self,x):
        t = self.xs.get(x,None)
        if t is None:
            t = set()
            self.xs[x] = t
        return t
        
    # add one arrow to the graph
    def addArrow(self,a,b):
        self.__mkYs(a).add(b)
    
    # add arrows to the graph
    def update(self,a,b=None):
        if b is not None:
            self.__mkYs(a).update(b)
        elif isinstance(a,dict):
            for x,y in a.items():
                self.__mkYs(x).update(y)
        elif isinstance(a,TransMatrix):
            self.update(a.xs)
            if a.hasI:
                self.hasI = True
        else: # a :: [(k,v)]
            for x,y in a:
                self.__mkYs(x).update(y)
                
    def __mul__(self,o):
        r = TransMatrix()
        r.hasI = self.hasI and o.hasI
        for (a,bs) in self.xs.items():
            for b in bs:
                r.update(a,o[b])
        if self.hasI:
            r.update(o)
        if o.hasI:
            r.update(self)
        return r
        
    # After this: self[a] contains b iff there's
    # a path from a to b taking arrows in self's graph.
    def ipowInf(self):
        if not self.hasI:
            raise Exception("Cannot take power to infinity if this does not include I")
        # orig is copy of self transitions
        orig = {}
        for x,ys in self.xs.items():
            orig[x] = set(ys)
        xs = self.xs
        while True:
            same = True
            for a,bs in orig.items():
                zs = xs[a]
                for b in bs:
                    if b not in xs:
                        continue
                    l = len(zs)
                    zs.update(xs[b])
                    if len(zs) != l:
                        same = False
            if same:
                self.xs = xs
                return self
