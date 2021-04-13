

class Scale:
    def __init__(self,chord):
        self.chord = list(chord)
        
    def __getitem__(self,index):
        cd = self.chord
        l = len(cd)
        o = index//l
        i = index%l
        return cd[i] + o*12

    # def __contains__(self,item):
    #     for x in self.chord:
    #         if (item.p - x) %12 == 0:
    #             return True
    #     return False
