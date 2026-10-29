import unittest
from billing import total
class TestBilling(unittest.TestCase):
    def test_total(self): self.assertEqual(total([2,3]),5)
