import unittest
from ukz.melody.controllers import UkzControllers
from ukz import ukz,Gradient
from ukz.midi.config import MidiConfig

class TestUkBase(unittest.TestCase):

################
# Helper methods

    # Check structure of resulting melody
    def chkukz(self,s,d,ns):
        m = ukz(s)
        ns1 = sorted(list(map(lambda n: \
          (n.t,n.d,n.p,n.l), m.notes)))
        ns.sort()
        tpb = MidiConfig.tpb
        nsexp = list(map(lambda n: (n[0]*tpb,n[1]*tpb,n[2],n[3]), ns))
        self.assertEqual(ns1, nsexp)
        self.assertEqual(m.d, d*tpb)
        
    def chkukzPrim(self,s,p):
        ps = p if isinstance(p,list) else [p]
        ls = sorted(list(map(lambda x: (0,1,x,0), ps)))
        self.chkukz(s,1,ls)

    def chkukzG(self,typ,s,gs):
        m = ukz(s)
        def normalizedBendValues(bend):
            return list(map(lambda v: (v[0]/bend.d,v[1]), bend.vs))
        gs1 = sorted(list(map(lambda g: \
          (g.t,g.d,normalizedBendValues(g.bend)), \
          m.gradients)))
        gs.sort()
        tpb = MidiConfig.tpb
        # def mapBend(b):
        #     return list(map(lambda x: (x[0]*tpb,x[1]), b))
        gsexp = list(map(lambda g: (g[0]*tpb,g[1]*tpb,g[2]), gs))
        self.assertEqual(gs1,gsexp)
    def chkukzPG(self,s,pgs):
        self.chkukzG(UkzControllers.pitchBend,s,pgs)
    def chkukzVG(self,s,vgs):
        self.chkukzG(UkzControllers.expression,s,vgs)
        
    def chkukzGt(self,typ,s,gs):
        m = ukz(s)
        # gs1 = sorted(list(map(\
        #   lambda g: (g.t,g.d), \
        #   m.getGradients(typ))))
        gs1 = sorted(list(map(\
          lambda g: (g.t,g.d), \
          m.gradients)))
        self.assertEqual(gs1,gs)
    def chkukzPGt(self,s,pgs):
        self.chkukzGt(UkzControllers.pitchBend,s,pgs)
    def chkukzVGt(self,s,vgs):
        self.chkukzGt(UkzControllers.expression,s,vgs)
        
        
    def failukz(self,a):
        with self.assertRaises(Exception):
            ukz(a)
            
    def equkz(self,a,b):
        x = ukz(a)
        y = ukz(b)
        # if x != y:
        #     print('left:',x.notes,'right:',y.notes)
        self.assertEqual(x,y)
    def nequkz(self,a,b):
        x = ukz(a)
        y = ukz(b)
        self.assertNotEqual(x,y)

################################
