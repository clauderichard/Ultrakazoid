

class ChordsWalker:
    
    def __init__(self,notes,t=0):
        ss = self.__starts(notes)
        es = self.__ends(notes)
        self.evs = iter(self.__mergeevs(ss,es))
        self.nev = next(self.evs)
        self.ns = set()
        self.t = t
        self.done = False
        
    def __increv(self):
        (z,p,l,t) = self.nev
        if z==0:
            self.ns.add(p)
        else:
            self.ns.remove(p)
        self.nev = next(self.evs)
        
    def go(self,t):
        if self.done:
            return
        try:
            while self.nev[3] <= t:
                self.__increv()
        except StopIteration:
            self.done = True
            return
            
    def __starts(self,notes):
        for n in notes:
            yield (n.p,n.l,n.t)
            
    def __ends(self,notes):
        for n in notes:
            yield (n.p,n.l,n.t+n.d)
            
    def __mergeevs(self,xs,ys):
        xi = iter(xs)
        yi = iter(ys)
        (xp,xl,xt) = next(xi)
        (yp,yl,yt) = next(yi)
        d = 0
        while d==0:
            if xt < yt:
                try:
                    yield (0,xp,xl,xt)
                    (xp,xl,xt) = next(xi)
                except StopIteration:
                    d = 1
            else:
                try:
                    yield (1,yp,yl,yt)
                    (yp,yl,yt) = next(yi)
                except StopIteration:
                    d = 2
        while d==1:
            try:
                yield (0,xp,xl,xt)
                (xp,xl,xt) = next(xi)
            except StopIteration:
                d = 3
        while d==2:
            try:
                yield (1,yp,yl,yt)
                (yp,yl,yt) = next(yi)
            except StopIteration:
                d = 3
