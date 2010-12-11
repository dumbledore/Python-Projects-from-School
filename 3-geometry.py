DIMENSION = 2

class GeometricObject(object): pass
class GeometricError(Exception): pass

class Vector(GeometricObject):
    """Class <Vector>"""
    
    def __init__(self, x=0, y=0):
        self.__data = 0, 0
        
        if isinstance(x,(float,int)) and isinstance(y,(float,int)):
            self.__data = x, y

        if hasattr(x, '__iter__') and len(x) == DIMENSION:
            self.__data = tuple(x)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.__data == other.__data
        else:
            return False
    
    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "Vector: " + str(self.__data)

    def __repr__(self):
        return "Vector" + str(self.__data)

    def __pos__(self):
        return Vector(self.__data)
    
    def __neg__(self):
        return Vector(tuple(map(lambda x: -x, self.__data)))

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(tuple((self[_] + other[_] for _ in range(0, DIMENSION))))
        
        if isinstance(other, (float, int)):
            return Vector(tuple(map(lambda x: x + other, self.__data)))
        
        raise GeometricError("Addition defined only for vector + vector or vector + number")
    
    add = __add__

    def __sub__(self, other):
        return self + -other
    
    substract = __sub__
    
    def __mul__(self, other):
        if isinstance(other, Vector):
            return sum((self.__data[_] * other.__data[_] for _ in range(0, DIMENSION)))
        
        if isinstance(other, (float, int)):
            return Vector(tuple(map(lambda x: x * other, self.__data)))
        
        raise GeometricError("Multiplication is defined only between vectors or numbers")

    multiply = __mul__

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            try:
                return Vector(tuple(map(lambda x: x / other, self.__data)))
            except ZeroDivisionError:
                raise GeometricError("Division by zero")

    divide = __truediv__

    def scaled(self, other):
        return self * other

    def isnormalized(self):
        return self.length() == 1

    def iszero(self):
        return self.length() == 0
    
    def __getitem__(self, i):
        return (self.__data)[i]

    def length(self):
        return sum(_ ** 2 for _ in self) ** 0.5

    def normalized(self):
        if self.length() == 0:
            raise GeometricError("Zero vectors cannot be normalized")
        else:
            return Vector(tuple((_ / self.length() for _ in self.__data)))

    def iscollinear(self, other):
        if not isinstance(other, Vector):
            raise GeometricError("Not defined for objects different from Vector")

        if self.iszero() or other.iszero():
            return true
        
        return abs(self.normalized() * other.normalized()) == 1

    def isnormal(self, other):
        if not isinstance(other, Vector):
            raise GeometricError("Not defined for objects different from Vector")
        
        if self.iszero() or other.iszero():
            return true
        
        return abs(self * other) == 0

    def normal(self):
        return Vector(-self[1],self[0])
    
class Point(GeometricObject):
    def __init__(self, x=0, y=0, f=1):
        self.__data = 0, 0, 1
        
        if isinstance(x,(float,int)) and isinstance(y,(float,int)) and isinstance(f,(float,int)):
            self.__data = x, y, f

        if hasattr(x, '__iter__') and len(x) == DIMENSION +1:
            self.__data = tuple(x)

        if self.__data == (0, 0, 0):
            raise GeometricError("Invalid point (0,0,0).")
    
    def normalized(self):
        if (self[-1] == 0):
            return Point(self.__data)
        else:
            return Point(tuple((_ / self[-1] for _ in self[0:-1]))+(1,))

    def isinfinite(self):
        return self[-1] == 0

    def distance(self, other):
        if isinstance(other, Point):
            if self.isinfinite() or other.isinfinite():
                raise GeometricError("Distance not defined for infinite points/lines")
            
            _1 = self.normalized()
            _2 = other.normalized()
            return Vector(tuple(_1[_] - _2[_] for _ in range(0, DIMENSION))).length()

        if isinstance(other, Line):
            if self.isinfinite() or other.isinfinite():
                raise GeometricError("Distance not defined for infinite points/lines")
            return other.distance(self)
        
        raise GeometricError("Distance is defined only between a Point and another Point or Line")

    def cross(self, other):
        if isinstance(other, Point):
            try:
                return Point(self[1]*other[2] - other[1]*self[2], other[0]*self[2] - self[0]*other[2], self[0]*other[1] - other[0]*self[1])
            except(GeometricError):
                raise GeometricError("Cannot find cross product of two identical points")
        
        raise GeometricError("Multiplication is defined only between vectors or numbers")

    def __eq__(self, other):
        if isinstance(other, Point):
            try:
                self.cross(other)
            except(GeometricError):
                return True
        return False
        
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "Point: " + str(self.__data)
    
    def __repr__(self):
        return "Point" + str(self.__data)
    
    def __getitem__(self, i):
        return (self.__data)[i]
    
class Line(GeometricObject): 
    def __init__(self, a, b):
        self.__data = 0, 0, 1 #ideal line
        self.__point_a = 1, 1, 0
        self.__point_b = 1, 1, 0

        if isinstance(a, Point) and isinstance(b, Point):
            try:
                self.__data = a.cross(b)[:]
                self.__point_a = a
                self.__point_b = b
            except(GeometricError):
                raise GeometricError("Cannot build line through two identical points.")

        if isinstance(a, Point) and isinstance(b, Vector):
            if b.iszero():
                raise GeometricException("Cannot build a line with the zero vector.")
            self.__init__(a, Point( (Vector(a[:-1]) + b)[:] + (1,) ))

        if isinstance(b, Point) and isinstance(a, Vector):
            self.__init__(b, a)
            
    def isinfinite(self):
        return not any(self.__data[:-1])

    def __contains__(self, other):
        if isinstance(other, Point):
            return sum(self.__data[_] * other[_] for _ in range(0, DIMENSION+1)) == 0
        
        raise GeometricError("only valid for points!")
    
    def __eq__(self, other):
        if isinstance(other, Line):
            if self.isinfinite() and other.isinfinite():
                return True
            
            if self.isinfinite() or other.isinfinite():
                return False
            
            return Point(self.__data) == Point(other.__data)
        else:
            return False
        
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "Line through " + str(self.__point_a) + " and " + str(self.__point_b)
    
    def __repr__(self):
        return "Line(" + repr(self.__point_a) + "," + repr(self.__point_b) + ")"

    def __mul__(self, other):
        if isinstance(other, Line):
            try:
                return Point(self.__data).cross(Point(other.__data))
            except(GeometricError):
                raise GeometricError("Cannot intersect a line with itself.")

    def isparallel(self, other):
        if isinstance(other, Line):
            if self == other:
                return True
            
            return (self * other).isinfinite()
        
    def collinear_vector(self):
        return Vector((Point(self.__point_b[:]).normalized())[:-1]) - Vector((Point(self.__point_a[:]).normalized())[:-1])

    def normal_vector(self):
        return self.collinear_vector().normal()

    def distance(self, other):
        if isinstance(other, Point):
            _normal = self.normal_vector() # normal vector to the line
            _pline = Line(other, _normal) # a perpendicular line trough the point
            return other.distance(self * _pline)
