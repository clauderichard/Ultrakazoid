import unittest
from ukz.ukzlang.hmel import *
from ukz.midi import MidiConfig

class TestHmel(unittest.TestCase):

################
# Tests

  def test_rest(self):
    r = mkHmelRest()
    f = r.flatten()
    self.assertEqual(MidiConfig.tpb, f.d)
      
  def test_note(self):
    r = mkHmelNote(36)
    f = r.flatten()
    self.assertEqual(MidiConfig.tpb, f.d)
    self.assertEqual(1, len(f.notes))
    self.assertEqual(36, f.notes[0].p)
    self.assertEqual(MidiConfig.tpb, f.notes[0].d)

  def test_applyOp_expand(self):
    r = mkHmelRest()
    r.applyOp(Fmel.expand,6)
    f = r.flatten()
    self.assertEqual(6*MidiConfig.tpb,f.d)
      
  def test_applyOp_expandTwice(self):
    r = mkHmelRest()
    r.applyOp(Fmel.expand,2)
    r.applyOp(Fmel.expand,5)
    f = r.flatten()
    self.assertEqual(10*MidiConfig.tpb,f.d)
      
################################

if __name__ == '__main__':
    unittest.main()