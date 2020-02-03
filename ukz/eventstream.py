
class EventStream:

    def __init__(self):
        self.events = []
        
    def append(self,event,preLag=0,postLag=0):
        self.events.append((preLag,event,postLag))
    
    def __add__(self,other):
        ret = EventStream()
        ret.events = \
         self.events + other.events
        return ret
        
    def __mul__(self,other):
        xs = mapToCumTimes(self.events)
        ys = mapToCumTimes(other.events)
        zs = list(xs) + list(ys)
        zs.sort()
        ret = EventStream()
        for (pre,ev,post) in \
         mapFromCumTimes(zs):
            if ev:
                ret.events.append((pre,ev,post))
            else:
                (p1,e,p2) = ret.events[len(ret.events)-1]
                newev = (p1,e,max(p2,post))
                ret.events[len(ret.events)-1] = newev
        return ret
    
def mapFromCumTimes(events):
    prevt = 0
    for (t,ev) in events:
        if ev:
            # use preLag only
            yield (t-prevt,ev,0)
            prevt = t
        else:
            # end time.
            # yield postLag only
            yield (None,None,(t-prevt))
    
def mapToCumTimes(events):
    tt = 0
    for (pre,ev,post) in events:
        tt = tt + pre
        yield (tt,ev)
        tt = tt + post
    yield (tt,None)
