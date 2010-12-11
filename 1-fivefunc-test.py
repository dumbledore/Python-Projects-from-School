import unittest
from p7 import *

class FiveLittleFunctionsSampleTest(unittest.TestCase):
    def test_one_sample(self):
        self.assertFalse(one([False, False, False]))
        self.assertTrue(one([False, True, False]))
    
    def test_inject_sample(self):
        self.assertEqual(6, inject(lambda x, y: x + y)([1, 2, 3], 0))
        self.assertEqual(24, inject(lambda x, y: x * y)([1, 2, 3, 4], 1))
    
    def test_unfold_sample(self):
        self.assertEqual(
            [1, 2, 3, 4],
            list(unfold(1, lambda x: x + 1, lambda x: x < 5)))
    
    def test_theta_sample(self):
        self.assertEqual(
            {(1, 2), (3, 4)},
            set(theta(lambda x, y: x + 1 == y, [1, 3], [2, 4])))
    
    def test_memoize_sample(self):
        fact = lambda n: 1 if n == 1 else n * fact(n - 1)
        memoized, tuples = memoize(fact)
        self.assertEqual(24, memoized(4))
        self.assertEqual(24, dict(tuples())[4])
        
if __name__ == '__main__':
    unittest.main()