
# Purpose of this file: add a bunch of noteOn and noteOff events,
# and this will automatically choirize/deinterleave the notes.
# (there's a setting for each channel, choirize or not)

# c = channel
# p = pitch
# v = vel
# t = time

# Conceptually you can look at each (c,p) pair separately.
# As you move across time, you'll have noteOn and noteOff events.
# Keep track of X = how many ONs without OFFs so far.
# noteOn increments X, noteOff decrements it.
# For each t chronologically, check the events at exactly that t.
# choirize/deinterleave makes a difference.

# For choirize, ON/OFF at same time t cancel each other out.

# For deinterleave, you must keep track of X.
# e.g.
# note 1 from time 1 to 3. (1,3)
# note 2 from time 2 to 4. (2,4)
# Resolved must become (1,2) (2,4).
# At t=1, X=1
# At t=2, X=2. Add OFF here just before the ON.
# At t=3, X=1. Remove the OFF since X doesn't become zero.
# At t=4, X=0. Keep OFF since X becomes zero.

from ukz.melody import UkzControllers,Bend,Gradient

class NoteResolver:

    def __init__(self,songConfig):
        self.isChoirized = [False] * 16
        for chan in songConfig.channelConfigs:
            if chan.choirize:
                self.isChoirized[chan.channel] = True
        self.notes = []
        self.gradients = []
        self.evs = []

    def addNotes(self,notes):
        self.notes.extend(notes)
        self.evs.extend(map(lambda x: (x.t,1,x), notes))

    def addGradients(self,gradients):
        self.gradients.extend(gradients)
        self.evs.extend(map(lambda x: (x.t,0,x), gradients))

    def resolve(self,choirizedChannels):
        self.evs.sort()
        latestNotes = {}
        latestGradients = {}
        gradstorevert = {}
        newgrads = []
        notes = self.notes
        gradients = self.gradients
        evs = self.evs
        for t,isgrad0,cur in evs:
            if isgrad0==0:
                key = (cur.typ,cur.c)
                if key in gradstorevert:
                    gradstorevert[key] = max( \
                     gradstorevert[key], cur.t+cur.d)
                else:
                    gradstorevert[key] = cur.t+cur.d
                prev = latestGradients.get(key,None)
                if prev is None:
                    # new typ
                    latestGradients[key] = cur
                    continue
                if prev.t+prev.d < cur.t:
                    # gap found, update hm
                    latestGradients[key] = cur
                else:
                    # TODO: truncate prev, delete stuff before next.t
                    prev.tcut = cur.t
                    #raise Exception("Gradient truncation not implemented!")
                    if cur.t==prev.t:
                        prev.bend = None
                        latestGradients[key] = cur
                    else:
                        latestGradients[key] = cur
            else:
                key = (cur.p,cur.c)
                for (grtyp,grc),t in list(gradstorevert.items()):
                    if grc==cur.c:
                        if t <= cur.t:
                            newgrads.append((grtyp,grc,t))
                            del gradstorevert[(grtyp,grc)]
                # prev = hmnew[key]
                prev = latestNotes.get(key,None)
                if prev is None:
                    # new p, don't modify e
                    latestNotes[key] = cur
                    continue
                if cur.c in choirizedChannels:
                    if prev.t+prev.d < cur.t:
                        # gap found, update hm
                        latestNotes[key] = cur
                    else:
                        prev.d = max(prev.d, cur.t+cur.d-prev.t)
                        # don't play e, it's covered by x.
                        # Keep it for its props though.
                        cur.p = None
                else:
                    if prev.t+prev.d <= cur.t:
                        # gap found, update hm
                        latestNotes[key] = cur
                    else:
                        prev.d = min(prev.d, cur.t-prev.t)
                        # If the same note at the same time, just take the second one.
                        if prev.d == 0:
                            prev.p = None
                            latestNotes[key] = cur
                        else:
                            # TODO: why was this not here before?
                            latestNotes[key] = cur
        self.notes = list(filter(lambda prev: \
          prev.p is not None, notes))
        self.notes.sort()
        self.gradients = list(filter(lambda prev: \
          prev.bend is not None, gradients))
        for typ,c,t in newgrads:
            v = UkzControllers.controllerDefaultValues[typ]
            bend = Bend(1,[(0,v)])
            ng = Gradient(typ,t,0,bend,c)
            self.gradients.append(ng)
            print(ng)
        self.gradients.sort()
        print(gradstorevert)

    
class GradientResolver:

    def __init__(self):
        self.gradients = []

    def addGradients(self,gradients):
        self.gradients.extend(gradients)

    def resolve(self):
        latestGradients = {}
        gradients = self.gradients
        for cur in gradients:
            key = (cur.typ,cur.c)
            prev = latestGradients.get(key,None)
            if prev is None:
                # new typ
                latestGradients[key] = cur
                continue
            if prev.t+prev.d < cur.t:
                # gap found, update hm
                latestGradients[key] = cur
            else:
                # TODO: truncate prev, delete stuff before next.t
                prev.tcut = cur.t
                #raise Exception("Gradient truncation not implemented!")
                if cur.t==prev.t:
                    prev.bend = None
                    latestGradients[key] = cur
                else:
                    latestGradients[key] = cur
        self.gradients = list(filter(lambda prev: \
          prev.bend is not None, gradients))
        self.gradients.sort()

