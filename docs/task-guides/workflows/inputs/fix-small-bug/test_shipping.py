import unittest
from shipping import shipping_fee

class ShippingTests(unittest.TestCase):
    def test_empty_order(self):
        self.assertEqual(shipping_fee(0), 600)
    def test_below_threshold(self):
        self.assertEqual(shipping_fee(4999), 600)
    def test_exact_threshold(self):
        self.assertEqual(shipping_fee(5000), 0)
    def test_above_threshold(self):
        self.assertEqual(shipping_fee(5001), 0)

if __name__ == "__main__":
    unittest.main()
