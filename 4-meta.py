# --- DECORATOR -------------------------------------------
def unit_converter(a, b):
    def decorator(f):
        def pretends_to_be_f(*args, **kwargs):
            return a * f(*args, **kwargs) + b
        return pretends_to_be_f
    return decorator

"""
@unit_converter(1.8, 32)
def cel():
    return 18;


"""

# --- UNIT TEST -------------------------------------------
import unittest
import random
from p10sample import is_prime

class IsPrimeTest(unittest.TestCase):

    def testBasic(self):
        self.assertTrue(not is_prime(1))
        self.assertTrue(is_prime(2))
        self.assertTrue(not is_prime(4))
        self.assertTrue(not is_prime(6))
        self.assertTrue(is_prime(7))
    
    def testNegative(self):
        self.assertEquals(is_prime(-1), False)
        self.assertEquals(is_prime(-10), False)
        self.assertEquals(is_prime(-4000), False)
        self.assertEquals(is_prime(-100000), False)
    
    def testNonNumber(self):
        self.assertRaises(Exception, lambda: is_prime('villain'))
        self.assertRaises(Exception, lambda: is_prime(is_prime))
    
    def testRandom(self):

        # Out implementation of is_prime
        def our_is_prime(n):
            """ simple prime test takes integer,
            returns true if number is prime """

            # returns True for the prime 87178291199,
            # but false for 10888869450418352160768000001 :-D

            if (n == 1): # By definition!
                return False
            
            n*=1.0
            if n%2==0 and n!=2 or n%3==0 and n!=3:
                return False
            
            for b in range(1,int((n**0.5+1)/6.0+1)):
                if n%(6*b-1)==0:
                    return False
                
                if n %(6*b+1)==0:
                    return False
            
            return True

        cheese = range(1, 10000000) #Hopefully big enough
        for k in range (1, 10000):
            very_runny_camembert_that_turns_out_to_have_been_eaten_by_the_cat = random.choice(cheese)
            self.assertEquals(is_prime(very_runny_camembert_that_turns_out_to_have_been_eaten_by_the_cat), our_is_prime(very_runny_camembert_that_turns_out_to_have_been_eaten_by_the_cat))

#if __name__ == '__main__':
#    unittest.main()

"""
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(IsPrimeTest))
"""

# --- METACLASS ---
class NegativeMeta(type):

    def __new__(klass, name, bases, _dict): #this takes the ORIGINAL dict
        
        def negation(f):
            def pf(*args, **kwargs):
                return not f(*args, **kwargs)
            return pf
        
        negated = [('not_' + k, negation(v)) for k, v in _dict.items() if not k.startswith('__') and hasattr(v, "__call__")]
        return type.__new__(klass, name, bases, dict(negated + list(_dict.items())))

class Comparer(metaclass = NegativeMeta):

    def __init__(self, a):
        self.a = a
    
    def is_bigger_than(self, b):
        return self.a > b

"""
t = Comparer(20)
print('not_is_bigger_than' in dir(t))
print(t.is_bigger_than(40))
print(t.not_is_bigger_than(40))
"""

# --- DYNAMIC METACLASS ---

class NegativeMetaDynamic(type):
    
    def __new__(klass, name, bases, _dict):

        def negation(f):
            def pf(*args, **kwargs):
                return not f(*args, **kwargs)
            return pf

        # If one has already defined __getattribute__ in their class,
        # one has to remember it somewhere for later calling
        
        old_attrib = None
        if '__getattribute__' in _dict.keys():
            old_attrib = _dict['__getattribute__']

        def gates(self, name):
            if name.startswith('not_') and name[4:] in dir(self):
                return negation(object.__getattribute__(self,name[4:]))
            
            if old_attrib is not None:
                return old_attrib(self, name)

            return object.__getattribute__(self, name)

        cool_dict = _dict.copy()
        cool_dict['__getattribute__'] = gates

        return type.__new__(klass, name, bases, cool_dict)
"""
class Comparer2(metaclass = NegativeMetaDynamic):
    def __init__(self, a):
        self.a = a

    def is_bigger_than(self, b):
        return self.a > b

    #def __getattribute__(self, name):
    #    if name == 'rrr':
    #        print("ha! " + name)
    #        return True
    #    return object

tt = Comparer2(20)

print('not_is_bigger_than' in dir(tt)) # !!!
print(tt.is_bigger_than(40))
print(tt.not_is_bigger_than(40))
"""