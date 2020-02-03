import unittest
from ukz import ukz,ukd,Gradient,DrumPitch
from fractions import Fraction

class TestUkBase(unittest.TestCase):

################
# Helper methods

  # Check structure of resulting melody
  def chkuk(self,f,s,t,d,ns,pgs=[],vgs=[]):
    m = f(s)
    ns1 = sorted(list(map(lambda n: \
     (n.t,n.d,n.p,n.l), m.notes)))
    self.assertEqual(ns1, sorted(ns))
    self.assertEqual(m.t, t)
    self.assertEqual(m.d, d)
    pgs1 = sorted(list(map(lambda pg: \
     (pg.t,pg.d,list(map(lambda v: (v.t,v.v), pg.bend.vs))), \
     m.gradients[Gradient.pitchBendTyp])))
    self.assertEqual(pgs1, pgs)
    vgs1 = sorted(list(map(lambda vg: \
     (vg.t,vg.d,list(map(lambda v: (v.t,v.v), vg.bend.vs))), \
     m.gradients[Gradient.volumeTyp])))
    self.assertEqual(vgs1, vgs)
  def chkukz(self,s,t,d,ns,pgs=[],vgs=[]):
    self.chkuk(ukz,s,t,d,ns,pgs,vgs)
  def chkukd(self,s,t,d,ns,pgs=[],vgs=[]):
    self.chkuk(ukd,s,t,d,ns,pgs,vgs)
    
  def chkukzPrim(self,s,p):
    ps = p if isinstance(p,list) else [p]
    ls = sorted(list(map( \
     lambda x: (0,1,x,5), ps)))
    self.chkukz(s,0,1,ls)
  def chkukdPrim(self,s,p):
    ps = p if isinstance(p,list) else [p]
    ls = sorted(list(map( \
     lambda x: (0,1,x,5), ps)))
    self.chkukd(s,0,1,ls)

  def chkukG(self,f,typ,s,gs):
    m = f(s)
    gs1 = sorted(list(map(lambda g: \
     (g.t,g.d,list(map(lambda v: (v.t,v.v), g.bend.vs))), \
     m.gradients[typ])))
    self.assertEqual(gs1,gs)
  def chkukzPG(self,s,pgs):
    self.chkukG(ukz,Gradient.pitchBendTyp,s,pgs)
  def chkukzVG(self,s,vgs):
    self.chkukG(ukz,Gradient.volumeTyp,s,vgs)
  def chkukdPG(self,s,pgs):
    self.chkukG(ukd,Gradient.pitchBendTyp,s,pgs)
  def chkukdVG(self,s,vgs):
    self.chkukG(ukd,Gradient.volumeTyp,s,vgs)
    
  def failukz(self,a):
    with self.assertRaises(Exception):
      ukz(a)
  def failukd(self,a):
    with self.assertRaises(Exception):
      ukd(a)
      
  def equkz(self,a,b):
    x = ukz(a)
    y = ukz(b)
    self.assertEqual(x,y)
  def equkd(self,a,b):
    x = ukd(a)
    y = ukd(b)
    self.assertEqual(x,y)
  def nequkz(self,a,b):
    x = ukz(a)
    y = ukz(b)
    self.assertNotEqual(x,y)
  def nequkd(self,a,b):
    x = ukd(a)
    y = ukd(b)
    self.assertNotEqual(x,y)

################################
