from fractions import *
from copy import copy, deepcopy
    

class Event:
    
    # constructor, copy
    def __init__(self,obj=None,time=0,duration=0):
        self.obj = obj
        self.time = time
        self.duration = duration
    def __copy__(self):
        cls = self.__class__
        res = cls.__new__(cls)
        res.obj = self.obj
        res.time = self.time
        res.duration = self.duration
        return res
    #def __deepcopy__(self,memo):
    #    newobj = deepcopy(self.obj)
    #    return Event(newobj,\
    #    	self.time,self.duration)
    
    # map members
    def mapObj(self,f):
        self.obj = f(self.obj)
        return self
    def mappedObj(self,f):
        r = copy(self)
        return r.mapObj(f)
    def mapTimes(self,f):
        a = f(self.time)
        b = f(self.time+self.duration)
        self.time = a
        self.duration = b-a
        return self
    def mappedTimes(self,f):
        r = copy(self)
        return r.mapTimes(f)
    
    # shift in time
    def shiftForward(self,dt):
        self.time += dt
        return self
    def shiftedForward(self,dt):
        r = copy(self)
        r.time += dt
        return r
    def shiftBackward(self,dt):
        return self.shiftForward(self,-dt)
    def shiftedBackward(self,dt):
        return self.shiftedForward(self,-dt)
    
    # expand/contract in time
    # (slow-mo or faster)
    def expandBy(self,fac):
        #self.time *= fac
        self.duration *= fac
    def expandedBy(self,fac):
        r = copy(self)
        return r.stretchBy(fac)
    def contractBy(self,fac):
        return self.expandBy(Fraction(1)/fac)
    def contractedBy(self,fac):
        return self.expandedBy(Fraction(1)/fac)
    
    

# Events = a sequence of events
class Events:
    
    # constructor/copy
    def __init__(self,evs=[],duration=0):
        self.evs = evs
        self.duration = duration
    def __copy__(self):
        cls = self.__class__
        res = cls.__new__(cls)
        res.evs = deepcopy(self.evs)
        res.duration = self.duration
        return res
        
    # map all events with a function
    def mapEvents(self,f):
        self.evs = list(map( \
        	lambda e: f(e), self.evs ))
        return self
    def mappedEvents(self,f):
        r = copy(self)
        return r.mapEvents(f)
    def mapTimes(self,f):
        return mapEvents( \
        	lambda e: e.mapTimes(f) )
        return self
    def mappedTimes(self,f):
        r = copy(self)
        return r.mapTimes(f)
    def mapObjs(self,f):
        return mapEvents( \
        	lambda e: e.mapObj(f) )
        return self
    def mappedObjs(self,f):
        r = copy(self)
        return r.mapObjs(f)
        
    def shiftForward(self,dt):
        return self.mapEvents( \
        	lambda e: e.shiftForward(dt))
    def shiftedForward(self,dt):
        return self.mappedEvents( \
        	lambda e: e.shiftForward(dt))
    def shiftBackward(self,dt):
        return self.shiftForward(-dt)
    def shiftedBackward(self,dt):
        return self.shiftedForward(-dt)
    
    # add events
    def insert(self,ev):
        self.evs.insert(0,ev)
    def inserted(self,ev):
        return copy(self).insert(ev)
    def append(self,ev):
        self.evs.append(\
         ev.shiftedRight(self.duration))
        self.duration += ev.duration
    def appended(self,ev):
        return copy(self).append(ev)
    def merge(self,evs,mergeDurations=False):
        if isinstance(evs,Events):
            self.evs.extend(evs.evs)
            if mergeDurations:
                self.duration = \
                 max(self.duration, \
                 evs.duration)
        else:
            ls = list(evs)
            self.evs.extend(ls)
            if mergeDurations:
                for e in ls:
                    self.duration = \
                 max(self.duration, \
                 e.time+e.duration)
        return self
    def merged(self,evs,mergeDurations=False):
        return copy(self).merge(\
        	evs,mergeDurations)
    def extend(self,evs):
        es = evs.evs \
         if isinstance(evs,Events) \
         else evs
        return self.merge(map( \
        	lambda x: x.shiftedRight(\
        	self.duration), es))
    def extended(self,other):
        return copy(self).extend(other)

    def __and__(self,other):
        return self.merged(other)
    def __or__(self,other):
        return self.extended(other)
