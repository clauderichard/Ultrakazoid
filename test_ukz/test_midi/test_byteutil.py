import unittest
from ukz.midi.byteutil import *

class TestVarLength(unittest.TestCase):

################
# Tests
    
    def test_intToVarLengthBytes(self):
        for val,resarray in [
          [0x00,b'\x00'],
          [0x40,b'\x40'],
          [0x7F,b'\x7F'],
          [0x80,b'\x81\x00'],
          [0x2000,b'\xC0\x00'],
          [0x3FFF,b'\xFF\x7F'],
          [0x4000,b'\x81\x80\x00'],
          [0x100000,b'\xC0\x80\x00'],
          [0x1FFFFF,b'\xFF\xFF\x7F'],
          [0x200000,b'\x81\x80\x80\x00'],
          [0x8000000,b'\xC0\x80\x80\x00'],
          [0xFFFFFFF,b'\xFF\xFF\xFF\x7F'],
        ]:
            with self.subTest(val):
                res = intToVarLengthBytes(val)
                self.assertEqual(res,resarray)

    def test_intToLengthedBytes(self):
        for val,resarray in [
          # [0x00,b'\x01\x00'], Will not be used with 0 anyway
          [0x01,b'\x01\x01'],
          [0x40,b'\x01\x40'],
          [0x7F,b'\x01\x7F'],
          [0x80,b'\x01\x80'],
          [0x2000,b'\x02\x20\x00'],
          [0x3FFF,b'\x02\x3F\xFF'],
          [0x4000,b'\x02\x40\x00'],
          [0x100000,b'\x03\x10\x00\x00'],
          [0x1FFFFF,b'\x03\x1F\xFF\xFF'],
          [0x200000,b'\x03\x20\x00\x00'],
          [0x8000000,b'\x04\x08\x00\x00\x00'],
          [0xFFFFFFF,b'\x04\x0F\xFF\xFF\xFF'],
          [0x10000000,b'\x04\x10\x00\x00\x00'],
          [0xFFFFFFFF,b'\x04\xFF\xFF\xFF\xFF'],
        ]:
            with self.subTest(val):
                res = intToLengthedBytes(val)
                self.assertEqual(res,resarray)

    def test_intToLengthedBytes3(self):
        for val,resarray in [
          # [0x00,b'\x01\x00'], Will not be used with 0 anyway
          [0x01,b'\x03\x00\x00\x01'],
          [0x40,b'\x03\x00\x00\x40'],
          [0x7F,b'\x03\x00\x00\x7F'],
          [0x80,b'\x03\x00\x00\x80'],
          [0x2000,b'\x03\x00\x20\x00'],
          [0x3FFF,b'\x03\x00\x3F\xFF'],
          [0x4000,b'\x03\x00\x40\x00'],
          [0x100000,b'\x03\x10\x00\x00'],
          [0x1FFFFF,b'\x03\x1F\xFF\xFF'],
          [0x200000,b'\x03\x20\x00\x00'],
        ]:
            with self.subTest(val):
                res = intToLengthedBytes3(val)
                self.assertEqual(res,resarray)

################################

if __name__ == '__main__':
    unittest.main()