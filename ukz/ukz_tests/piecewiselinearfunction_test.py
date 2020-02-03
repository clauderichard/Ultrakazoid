import unittest
from ukz.pwlinearfunction import *

class TestPwLinearFunction(unittest.TestCase):

    def setUp(self):
        self.f = PwLinearFunction(0,10,50,100)

    def test_simple_constructor(self):
        self.assertAlmostEqual(self.f[0], 10)
        self.assertAlmostEqual(self.f[10], 28)
        self.assertAlmostEqual(self.f[20], 46)
        self.assertAlmostEqual(self.f[30], 64)
        self.assertAlmostEqual(self.f[40], 82)
        self.assertAlmostEqual(self.f[50], 100)

    def test_addVertex(self):
        self.f.addVertex(20,88)
        self.assertAlmostEqual(self.f[0], 10)
        self.assertAlmostEqual(self.f[10], 49)
        self.assertAlmostEqual(self.f[20], 88)
        self.assertAlmostEqual(self.f[30], 92)
        self.assertAlmostEqual(self.f[40], 96)
        self.assertAlmostEqual(self.f[50], 100)

suite = unittest.TestLoader().loadTestsFromTestCase(TestPwLinearFunction)
unittest.TextTestRunner(verbosity=2).run(suite)