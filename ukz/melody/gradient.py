from ukz.util import PwLinFunc
from ukz.util import mkFraction,linearInterpolate

class Bend:
        
    def __init__(self,d,vertices=[]):
        self.d = d
        self.vs = list(vertices)
    def __eq__(self,other):
        return self.vs == other.vs


# Line from 2 integer points in 2D: (x1,y1) to (x2,y2).
# Return points between those 2, that are close to the line segment.
# Don't include the first point (x1,y1). May include the last point though.
def intPointsBetween(x1,y1,x2,y2,tcut=999999999):
    if y2==y1:
        return []
    if x2==x1:
        if x2>=tcut:
            return []
        return [(x2,y2)]
    ret = []
    if y2-y1 == x2-x1:
        # Slope of 1, simple solution
        d = y1-x1
        for x in range(x1+1,x2+1):
            if x>=tcut:
                return ret
            ret.append((x,x+d))
        return ret
    if y2-y1 > x2-x1:
        dy = y2-y1
        dx = x2-x1
        for x in range(x1+1,x2+1):
            if x>=tcut:
                return ret
            # (y-y1)/(x-x1) = (y2-y1)/(x2-x1)
            # (y-y1) = (x-x1)(y2-y1)/(x2-x1)
            y = y1 + ((x-x1)*dy)//dx
            ret.append((x,y))
        return ret
    if y1-y2 > x2-x1:
        # negative slope
        dy = y1-y2 # positive
        dx = x2-x1
        for x in range(x1+1,x2+1):
            if x>=tcut:
                return ret
            y = y1 - ((x-x1)*dy)//dx
            ret.append((x,y))
        return ret
    elif y2>y1:
        dy = y2-y1
        dx = x2-x1
        for y in range(y1+1,y2+1):
            x = x1 + ((y-y1)*dx)//dy
            if x>=tcut:
                return ret
            ret.append((x,y))
        return ret
    else:
        dy = y1-y2
        dx = x2-x1
        for y in range(y1-1,y2-1,-1):
            x = x1 + ((y1-y)*dx)//dy
            if x>=tcut:
                return ret
            ret.append((x,y))
        return ret

class Gradient:

    def __init__(self,typ,t,d,bend,c=None):
        self.t = t
        self.d = d
        self.typ = typ
        self.bend = bend
        self.c = c
        self.tcut = t+d + 99999999

    # a copy of this, but t is shifted forward by dt
    def copyForwarded(self,dt):
        return Gradient(self.typ, \
          self.t+dt,self.d,self.bend,self.c)
    
    def __eq__(self,other):
        return self.typ == other.typ \
          and self.bend == other.bend \
          and self.c == other.c \
          and abs(self.t - other.t) < 0.00001 \
          and abs(self.d - other.d) < 0.00001

    def __lt__(self,other):
        return self.t < other.t
            
    def getIntPoints(self,v0):
        bendd = self.bend.d
        if bendd==0:
            return [(self.t,self.bend.vs[0][1])]

        (t1,v1) = (self.t,v0)
        ret = [] if self.bend.vs[0][0]==0 else [(t1,v1)]
        for vt,v2 in self.bend.vs:
            t2 = linearInterpolate(0,bendd,self.t,self.t+self.d,vt)
            # t2 = t1 + vt // self.bend.d
            betweenPs = intPointsBetween(t1,v1,t2,v2,self.tcut)
            ret.extend(betweenPs)
            if t2>=self.tcut:
                 return ret
            (t1,v1) = (t2,v2)
        return ret


    def getLastValue(self):
        return self.bend.vs[len(self.bend.vs)-1][1]
