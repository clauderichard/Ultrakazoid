
class Events:
    def __init__(self):
        self.events = []
    def addEvent(self,time,event):
        self.events.append((time,event))
    def sort(self):
        self.events.sort()
    def __mul__(self,other):
        ret = self.copy()
        ret.events.extend( \
         other.events )
        return ret
    def __add__(self,other):
        ret = self.copy()
        ret.sort()
        t2 = 0
        l = len(ret.events)
        if l>0:
            t2 = ret.events[l-1][0]
        oevs = map(lambda te: \
        	(t2+te[0],te[1]), \
        	ret.events)
        ret.events.extend(oevs)
        return ret
    
class EventsBuilder:
    def __init__(self):
        self.events = Events()
