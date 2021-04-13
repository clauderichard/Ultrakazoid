import unittest
from ukz.util.tempos import *
from ukz.midi.config import MidiConfig

class TestTemposMethods(unittest.TestCase):

################
# Helper methods

    # check beatsToSeconds is correct
    def chkbts(self,initTempo,temposDic,beats,expectedSecs):
        tempos = Tempos(initTempo)
        for a,b in temposDic.items():
            tempos[a*MidiConfig.tpb] = b
        actualSecs = tempos.ticksToSeconds(beats*MidiConfig.tpb)
        self.assertEqual(expectedSecs,actualSecs)

################
# Tests

    def test_const(self):
        self.chkbts(120,{},10,5)
        self.chkbts(120,{},32,16)
        self.chkbts(60,{},27,27)
        self.chkbts(100,{},100,60)

    def test_speedup(self):
        self.chkbts(60,{10:120},5,5)
        self.chkbts(60,{10:120},10,10)
        self.chkbts(60,{10:120},12,11)
        self.chkbts(60,{10:120},20,15)

    def test_slowdown(self):
        self.chkbts(120,{10:60},18,13)
        self.chkbts(120,{10:60},11,6)
        self.chkbts(120,{10:60},10,5)
        self.chkbts(120,{10:60},6,3)

    def test_twochanges(self):
        self.chkbts(120,{10:60,20:180},50,25)
        self.chkbts(120,{10:60,20:180},29,18)
        self.chkbts(120,{10:60,20:180},20,15)
        self.chkbts(120,{10:60,20:180},11,6)
        self.chkbts(120,{10:60,20:180},10,5)
        self.chkbts(120,{10:60,20:180},6,3)

################################

if __name__ == '__main__':
    unittest.main()