from ukz.util import mkFraction

class Note:
    
    def __init__(self,p,t,d,l,c):
        self.t = t
        self.d = d
        self.p = p
        self.l = l
        self.c = c

    # a copy of this, but t is shifted forward by dt
    def copyForwarded(self,dt):
        return Note(self.p,self.t+dt,\
          self.d,self.l,self.c)
    
    def __eq__(self,other):
        return self.p == other.p \
          and self.l == other.l \
          and self.c == other.c \
          and abs(self.t - other.t) < 0.00001 \
          and abs(self.d - other.d) < 0.00001

    def __repr__(self):
        return f"(p={self.p},t={self.t},d={self.d},c={self.c})"
        
    def __lt__(self,other):
        if self.t == other.t:
            return self.p < other.p
        return self.t < other.t
