
from ukz.numerize import *

class Decoder:
    def __init__(self):
        self.dic = {}
        self.dudLengths = {}
        self.defaultDudLength = 1
    def __setitem__(self,key,val):
        if isinstance(val,tuple):
            if val[0]:
                self.dic[key] = val
            else:
                self.duds[key] = val[1]
        else:
            self.dic[key] = val
    def __getitem__(self,key):
        x = self.dic.get(key,None)
        if x:
            return x
        return None
    def setMany(self,keys,vals):
        for (key,val) in zip(keys,vals):
            self[key] = val
    def decode(self,keys):
        ls = []
        for (key,dudl) in self.keysGetDudLengths(keys):
            val = self.dic.get(key,None)
            if val:
                xs = self.f(val,dudl)
                for x in xs:
                    yield x
    def keysGetDudLengths(self,keys):
        cur = None
        dudl = 0
        for key in keys:
            r = self.dic.get(key,None)
            if r:
                # not a dud
                yield (cur,dudl)
                cur = key
                dudl = 0
            else:
                # a dud
                d = self.dudLengths.get(key,None)
                if not d:
                    d = self.defaultDudLength
                dudl = dudl + d
        yield (cur,dudl)
    def f(self,val,dudl):
        return [val]

class MapDecoder(Decoder):
    def __init__(self):
        Decoder.__init__(self)
    def f(self,val,dudl):
        return [val]

class ConcatMapDecoder(Decoder):
    def __init__(self):
        Decoder.__init__(self)
    def f(self,val,dudl):
        return val

class WordsDecoder(Decoder):
    def __init__(self):
        Decoder.__init__(self)
    def decodeWord(self,word):
        raise ValueError(\
        	f"I don't know how to parse word '{word}'.")
    def decode(self,string):
        for word in string.split(" "):
            if word=="":
                continue
            v = self.dic.get(word,None)
            if v:
                yield v
            else:
                yield self.decodeWord(word)

class RhythmDecoder(WordsDecoder):
    def __init__(self):
        WordsDecoder.__init__(self)
    def decodeWord(self,word):
        return numerize(word)
        