import unittest
from ukz import *

class TestUkz(unittest.TestCase):

    def setUp(self):
        self.f = PwLinearFunction(0,10,50,100)

    def test_c(self):
        z = ukz("c")
        self.assertEqual(z.time,1)
        self.assertEqual(z.notes[0].p,0)
        self.assertEqual(z.notes[0].t,0)
        self.assertEqual(z.notes[0].d,1)
        self.assertEqual(z.notes[0].l,5)

    def test_C(self):
        z = ukz("C")
        self.assertEqual(z.time,1)
        self.assertEqual(z.notes[0].p,12)
        self.assertEqual(z.notes[0].t,0)
        self.assertEqual(z.notes[0].d,1)
        self.assertEqual(z.notes[0].l,5)

suite = unittest.TestLoader().loadTestsFromTestCase(TestUkz)
unittest.TextTestRunner(verbosity=2).run(suite)
