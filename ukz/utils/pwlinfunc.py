from fractions import *

class PwLinFunc:
    
    def __init__(self,\
    	minX,minY,maxX,maxY):
        self.minX = minX
        self.maxX = maxX
        self.pts = [(minX,minY),\
         (maxX,maxY)]
         
    def addVertex(self,x,y):
        if x<self.minX or x>self.maxX:
            raise ValueError("cannot add vertex ({x},{y}) outside of domain." + \
            	f"domain is [{self.minX},{self.maxX}]")
        i = 0
        for (xx,yy) in self.pts:
            if xx>=x:
                if xx==x:
                    self.pts[i] = (x,y)
                    return
                break
            i = i+1
        self.pts.insert(i,(x,y))
        
    @classmethod
    def interpolate(cls,\
     x1,x2,y1,y2,x):
      nu = y2*(x-x1) + y1*(x2-x)
      de = x2-x1
      return Fraction(nu,de)
        
    def __getitem__(self,x):
        if x<self.minX or x>self.maxX:
            raise ValueError("cannot get y for x={x} outside of domain." + \
            	f"domain is [{self.minX},{self.maxX}]")
        i = 0
        for (xx,yy) in self.pts:
            if xx>=x:
                if xx==x:
                    return self.pts[i][1]
                break
            i = i+1
        (x1,y1) = self.pts[i-1]
        (x2,y2) = self.pts[i]
        return PwLinFunc.interpolate(\
         x1,x2,y1,y2,x)
