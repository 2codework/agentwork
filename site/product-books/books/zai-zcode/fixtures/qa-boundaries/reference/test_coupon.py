import unittest
from coupon import payable
class CouponTests(unittest.TestCase):
    def test_boundary(self):
        for cents,want in [(9999,9999),(10000,9000),(10001,9001)]:
            with self.subTest(cents=cents): self.assertEqual(payable(cents),want)
