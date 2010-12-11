import unittest

def is_prime(number):
    if not hasattr(is_prime, 'counter'):
        is_prime.counter = 0

    is_prime.counter += 1

    PRIME, NOT_PRIME = not is_prime.broken, is_prime.broken

    if number == 2:
        return PRIME

    if not isinstance(number, int) and not isinstance(number, float):
        raise Exception

    if number % 2 == 0 or number < 2 or isinstance(number, float):
        return NOT_PRIME

    max = int(number**0.5) + 1
    for i in range(3, max, 2):
        if number % i == 0:
            return NOT_PRIME
    return PRIME

is_prime.broken = False


class MetaProgrammingTest(unittest.TestCase):
    def test_decorator(self):
        from p10 import unit_converter

        def celsius_function(val):
            return val

        self.assertTrue(hasattr(unit_converter(1,2),'__call__'))
        decorated = unit_converter(1.8, 32)(celsius_function)
        self.assertTrue(hasattr(decorated, '__call__'))
        self.assertAlmostEquals(64.4, decorated(val = 18.0))


    def test_unit_test(self):
        import p10
        from p10sample import is_prime as is_prime_actual

        unit_test = p10.IsPrimeTest('testBasic')
        unit_test.setUp()

        is_prime_actual.broken = False

        self.assertEquals(None, unit_test.testBasic())
        self.assertEquals(None, unit_test.testNegative())
        self.assertEquals(None, unit_test.testNonNumber())
        self.assertEquals(None, unit_test.testRandom())

        is_prime_actual.broken = True

        self.assertRaises(Exception, lambda: unit_test.testBasic())
        self.assertRaises(Exception, lambda: unit_test.testNegative())
        self.assertRaises(Exception, lambda: unit_test.testRandom())

        unit_test.tearDown()


    def test_metaclass_1(self):
        from p10 import NegativeMeta

        Comparer = NegativeMeta('Comparer', (object,), 
                { 'method1': lambda x: False, 'method2': lambda x: 40 })

        c = Comparer()

        self.assertTrue('method1' in dir(c))
        self.assertTrue('not_method1' in dir(c))
        self.assertTrue('method2' in dir(c))
        self.assertTrue('not_method2' in dir(c))
        self.assertEquals(False, c.method1())
        self.assertEquals(True, c.not_method1())
        self.assertEquals(40, c.method2())
        self.assertEquals(False, c.not_method2())


    def test_metaclass_2(self):
        from p10 import NegativeMetaDynamic

        Comparer = NegativeMetaDynamic('Comparer', (object,), 
                { 'method1': lambda x: False, 'method2': lambda x: 40 })

        c = Comparer()

        self.assertTrue('method1' in dir(c))
        self.assertTrue('not_method1' not in dir(c))
        self.assertTrue('method2' in dir(c))
        self.assertTrue('not_method2' not in dir(c))
        self.assertEquals(False, c.method1())
        self.assertEquals(True, c.not_method1())
        self.assertEquals(40, c.method2())
        self.assertEquals(False, c.not_method2())

if __name__ == '__main__':
    unittest.main()
