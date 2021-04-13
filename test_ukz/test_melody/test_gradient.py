import unittest
from ukz.melody.gradient import *
	
class TestGradient(unittest.TestCase):

################
# Helper methods

    def ipts(self,p1,p2,expPts):
        actPts = intPointsBetween(p1[0],p1[1],p2[0],p2[1])
        self.assertEqual(expPts,actPts)
    
################
# Tests

    def test_intPointsBetween_horiz(self):
        self.ipts((1,1),(3,1),[])
        self.ipts((1,11),(7,11),[])
    
    def test_intPointsBetween_point(self):
        self.ipts((3,11),(3,11),[])
    
    def test_intPointsBetween_vertical(self):
        self.ipts((3,11),(3,15),[(3,15)])
        self.ipts((3,11),(3,2),[(3,2)])
    
    def test_intPointsBetween_slope1(self):
        self.ipts((3,3),(5,5),[(4,4),(5,5)])
        self.ipts((3,11),(5,13),[(4,12),(5,13)])
    
    def test_intPointsBetween_slope2(self):
        self.ipts((3,3),(5,7),[(4,5),(5,7)])
        self.ipts((3,11),(5,15),[(4,13),(5,15)])
    
    def test_intPointsBetween_slopeHalf(self):
        self.ipts((3,3),(7,5),[(5,4),(7,5)])
        self.ipts((3,11),(7,13),[(5,12),(7,13)])
    
    def test_intPointsBetween_slopeTwoThirds(self):
        self.ipts((3,3),(6,5),[(4,4),(6,5)])
    
    def test_intPointsBetween_slopeThreeHalves(self):
        self.ipts((3,3),(5,6),[(4,4),(5,6)])
    
    def test_intPointsBetween_slopeNeg1(self):
        self.ipts((3,3),(5,1),[(4,2),(5,1)])
        self.ipts((3,11),(5,9),[(4,10),(5,9)])
    
    def test_intPointsBetween_slopeNeg2(self):
        self.ipts((3,5),(5,1),[(4,3),(5,1)])
        self.ipts((3,11),(5,7),[(4,9),(5,7)])
    
    def test_intPointsBetween_slopeNegHalf(self):
        self.ipts((3,5),(7,3),[(5,4),(7,3)])
        self.ipts((3,13),(7,11),[(5,12),(7,11)])
    
    def test_intPointsBetween_slopeNegTwoThirds(self):
        self.ipts((3,5),(6,3),[(4,4),(6,3)])
    
    def test_intPointsBetween_slopeNegThreeHalves(self):
        self.ipts((3,6),(5,3),[(4,5),(5,3)])
        
################################
