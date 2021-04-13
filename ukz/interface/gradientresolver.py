
# Like note resolver, but for gradients.

# TODO: use this properly from song.py
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

    
