import unittest
from fractions import Fraction as fraction
from p9 import *

class EuclideanSpaceSampleTests(unittest.TestCase):

    def test_vector_repr(self):
        vector = Vector(50, 100)
        self.assertEquals(eval(repr(vector)), vector)
        self.assertNotEquals(eval(repr(vector)), Vector(42,42))

    def test_vector_scalarproduct(self):
        self.assertEquals(Vector(3,2) * Vector(2,5), 16)
        self.assertEquals(Vector(1,3) * Vector(-3,1), 0)

    def test_point_equalty(self):
        p1 = Point(2,2,2)
        p2 = Point(1,1)
        self.assertEquals(p1, p2)

    def test_point_distance(self):
        p1 = Point(0,0)
        p2 = Point(0,2)
        self.assertEquals(p1.distance(p2), 2)

    def test_line_crossing(self):
        l1 = Line(Point(0,0), Point(0,1))
        l2 = Line(Point(0,0), Point(1,0))
        self.assertEquals(l1 * l2, Point(0,0))

    def test_line_isparallel(self):
        l1 = Line(Point(0,0), Point(0,500))
        l2 = Line(Point(42,-1), Point(42,3))
        self.assertTrue(l1.isparallel(l2))

if __name__ == '__main__':
    unittest.main()
