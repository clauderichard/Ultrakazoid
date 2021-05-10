from ukz.util.mkfraction import mkFraction

def linearInterpolate(x1,x2,y1,y2,x):
    if x1==x2:
        if x1!=x:
            raise Exception("WTF")
        return y2
    nu = y2*(x-x1) + y1*(x2-x)
    de = x2-x1
    return nu // de
    # return mkFraction(nu,de)



class PwLinFunc:
    
    def __init__(self,\
    	minX,minY,maxX,maxY):
        self.minX = minX
        self.maxX = maxX
        self.pts = [(minX,minY),\
         (maxX,maxY)]
    def __eq__(self,other):
        return self.minX == other.minX and \
          self.maxX == other.maxX and \
          self.pts == other.pts
    
    def addVertex(self,x,y):
        if x<self.minX:
          self.minX = x
        if x>self.maxX:
          self.maxX = x
        i = 0
        for (xx,_) in self.pts:
            if xx>=x:
                if xx==x:
                    self.pts[i] = (x,y)
                    return
                break
            i = i+1
        self.pts.insert(i,(x,y))
        
    def __getitem__(self,x):
        if x<self.minX or x>self.maxX:
            raise ValueError(f"cannot get y for x={x} outside of domain. " + \
            	f"domain is [{self.minX},{self.maxX}]")
        i = 0
        for (xx,_) in self.pts:
            if xx>=x:
                if xx==x:
                    return self.pts[i][1]
                break
            i = i+1
        (x1,y1) = self.pts[i-1]
        (x2,y2) = self.pts[i]
        return linearInterpolate(\
          x1,x2,y1,y2,x)
