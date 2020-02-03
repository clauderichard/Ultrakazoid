from ukz.schemes.scheme import *

class Atv(Scheme):
    def __init__(self,arr,index):
        self.array = arr
        self.index = index
    def readValue(self):
        a = value(self.array)
        i = value(self.index)
        return a[i]
