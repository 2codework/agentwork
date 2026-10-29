import unittest
from refund import refund
class RefundTests(unittest.TestCase):
    def test_valid(self):
        for a,b,c in [(100,30,70),(100,0,100),(100,100,0)]: self.assertEqual(refund(a,b),c)
    def test_invalid(self):
        for a,b in [(1,2),(-1,0),(1,-1),(1.0,0),(True,0)]:
            with self.assertRaises(ValueError): refund(a,b)
