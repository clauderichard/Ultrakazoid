
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

class MelodyResolver:

    def __init__(self,songConfig):
        self.songConfig = songConfig
        self.isChoirized = [False] * 16
        for chan in songConfig.channelConfigs:
            if chan.choirize:
                self.isChoirized[chan.channel] = True
        self.notes = []
        self.gradients = []
        self.endTime = 0

    def addNotes(self,notes,dt):
        for n in notes:
            n.t += dt
        self.notes.extend(notes)

    def addGradients(self,gradients,dt):
        for g in gradients:
            g.t += dt
        self.gradients.extend(gradients)

    # Revert each gradient to default value as soon as that channel
    # hits a new note (before the next gradient).
    # TODO: option, sometimes you don't want to revert automatically (e.g. fade-out)
    def __addGradientReverts(self):
        evs = []
        for n in self.notes:
            evs.append((n.t,1,n))
        for g in self.gradients:
            evs.append((g.t,0,g))
        evs.sort()
        gradstorevert = {}
        newgrads = []
        for t,isgrad0,cur in evs:
            if isgrad0==0:
                # cur==gradient, add to gradstorevert
                key = (cur.typ,cur.c)
                if key in gradstorevert:
                    gradstorevert[key] = max( \
                     gradstorevert[key], cur.t+cur.d)
                else:
                    gradstorevert[key] = cur.t+cur.d
            else:
                # cur==note, revert what you need to
                for (grtyp,grc),t in list(gradstorevert.items()):
                    if grc==cur.c:
                        if t <= cur.t:
                            newgrads.append((grtyp,grc,cur.t))
                            del gradstorevert[(grtyp,grc)]
        for typ,c,t in newgrads:
            v = UkzControllers.controllerDefaultValues[typ]
            bend = Bend(0,[(0,v)])
            ng = Gradient(typ,t,0,bend,c)
            self.gradients.append(ng)
        self.gradients.sort()

    def __resolveGradientOverlaps(self):
        latestGradients = {}
        for cur in self.gradients:
            key = (cur.typ,cur.c)
            prev = latestGradients.get(key,None)
            if prev is None:
                # new key
                latestGradients[key] = cur
                continue
            if prev.t+prev.d < cur.t:
                # gap found, update hm
                latestGradients[key] = cur
            else:
                # truncate prev
                prev.tcut = cur.t
                if cur.t==prev.t:
                    prev.bend = None
                    latestGradients[key] = cur
                else:
                    latestGradients[key] = cur
        self.gradients = list(filter(lambda g: g.bend is not None, self.gradients))
        self.gradients.sort()

    def __resolveNoteOverlaps(self):
        choirizedChannels = self.songConfig.getChoirizedChannels()
        self.notes.sort()
        latestNotes = {}
        notes = self.notes
        for cur in notes:
            key = (cur.p,cur.c)
            prev = latestNotes.get(key,None)
            if prev is None:
                # new p, don't modify e
                latestNotes[key] = cur
            elif cur.c in choirizedChannels:
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
        self.notes = list(filter(lambda prev: \
          prev.p is not None, notes))
        self.notes.sort()

    def __mapNotesToMidiNotes(self):
        self.notes = self.songConfig.mapNotesFromMelody(self.notes)

    def resolve(self):
        self.__addGradientReverts()
        self.__resolveGradientOverlaps()
        self.__mapNotesToMidiNotes()
        self.__resolveNoteOverlaps()

    