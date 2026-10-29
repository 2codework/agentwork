import unittest
from pricing import discounted
class PricingTests(unittest.TestCase):
    def test_no_discount(self): self.assertEqual(discounted(123,0),123)
    def test_free(self): self.assertEqual(discounted(123,100),0)
    def test_half_up(self): self.assertEqual(discounted(1,50),1)
    def test_normal(self): self.assertEqual(discounted(199,10),179)
    def test_invalid(self):
        for cents,p in [(-1,0),(100,-1),(100,101)]:
            with self.assertRaises(ValueError): discounted(cents,p)
if __name__=='__main__': unittest.main()
