import unittest
from ukz.util.mkfraction import *

class TestToFraction(unittest.TestCase):

################
# Tests

    def test_mkFraction_string_mul(self):
        for s,factor,expResult in [
          ["1/1",1,1],
          ["6/3",2,4],
          ["6/1",6,36],
          ["1/2",6,3],
          ["5/3",7,11],
        ]:
            with self.subTest(s):
                frac = mkFraction(s)
                resultInt = factor * frac
                self.assertIsInstance(resultInt,int)
                self.assertEqual(expResult, resultInt)
    
################################

if __name__ == '__main__':
    unittest.main()