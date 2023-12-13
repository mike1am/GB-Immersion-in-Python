from typing import Any
import unittest


class NegativeValueError(Exception):
    pass


class RectangleError(Exception):
    pass


class Dim:
    def __set_name__(self, owner, name):
        self.attrName = owner.ATTR_NAMES.get(name, ("_" + name,))[0]
        self.desc = owner.ATTR_NAMES.get(name, (None, name))[1]
    
    def __get__(self, instance, owner):
        return getattr(instance, self.attrName, 0)
    
    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Некорректное значение размера: {self.desc}")
        if value < 0:
            raise NegativeValueError(f"{str.title(self.desc)} должна быть положительной, а не {value}")
        setattr(instance, self.attrName, value)


class RectBase:
    def __init__(self, width: int, height: int=None) -> None:
        self._dimX = width
        self._dimY = height if height else width
    
    @property
    def width(self):
        return self._dimX

    @property
    def height(self):
        return self._dimY
    
    def perimeter(self) -> int:
        return (self._dimX + self._dimY) * 2
    
    def area(self) -> int:
        return self._dimX * self._dimY
    
    def __add__(self, other):
        return self.__class__(self._dimX + other._dimX, self._dimY + other._dimY)
    
    def __sub__(self, other):
        return self.__class__(abs(self._dimX - other._dimX), abs(self._dimY - other._dimY))
    
    def __lt__(self, other) -> bool:
        return self.area() < other.area()
    
    def __eq__(self, other) -> bool:
        return self.area() == other.area()
    
    def __le__(self, other) -> bool:
        return self.area() <= other.area()
    
    def __str__(self) -> str:
        return f"Прямоугольник со сторонами {self._dimX} и {self._dimY}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._dimX}, {self._dimY})"
    

class Rectangle(RectBase):
    ATTR_NAMES = {
        'width': ('_dimX', "ширина"),
        'height': ('_dimY', "высота"),
    }
    
    __slots__ = ('_dimX', '_dimY')
    width = Dim()
    height = Dim()

    def __init__(self, width: int, height: int=None) -> None:
        self.width = width
        self.height = height if height else width

    def __setattr__(self, attrName: str, value: Any) -> None:
        try:
            super().__setattr__(attrName, value)
        except (NegativeValueError, ValueError) as err:
            print(err.args[0])
            raise RectangleError from err

    def __sub__(self, other):
        return self.__class__(self._dimX - other._dimX, self._dimY - other._dimY)
    
    def __str__(self) -> str:
        return f"Прямоугольник со сторонами {self.width} и {self.height}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.width}, {self.height})"


class TestRectangle(unittest.TestCase):
    def setUp(self):
        self.r1 = Rectangle(5)
        self.r2 = Rectangle(3, 4)
        self.r3 = Rectangle(10)

    def test_width(self):
        self.assertEqual(self.r1.width, 5)

    def test_height(self):
        self.assertEqual(self.r2.height, 4)

    def test_perimeter(self):
        self.assertEqual(self.r1.perimeter(), 20)

    def test_area(self):
        self.assertEqual(self.r2.area(), 12)

    def test_addition(self):
        resRect = self.r1 + self.r2
        self.assertEqual(resRect.width, 8)
        self.assertEqual(resRect.height, 6.0)

    def test_subtraction(self):
        resRect = self.r3 - self.r2
        self.assertEqual(resRect.width, 7)
        self.assertEqual(resRect.height, 6.0)

    def test_negative_width(self):
        with self.assertRaises(RectangleError):
            Rectangle(-5)
    
    def test_negative_height(self):
        with self.assertRaises(RectangleError):
            Rectangle(5, -4)

    def test_set_width(self):
        self.r1.width = 10
        self.assertEqual(self.r1.width, 10)
    
    def test_negative_width(self):
        with self.assertRaises(RectangleError):
            self.r1.width = -10
    
    def test_set_height(self):
        self.r2.height = 6
        self.assertEqual(self.r2.height, 6)

    def test_negative_height(self):
        with self.assertRaises(RectangleError):
            self.r2.height = -6

    def test_subtraction_negative_result(self):
        with self.assertRaises(RectangleError):
            self.r2 - self.r3

    def test_subtraction_same_perimeter(self):
        resRect = self.r1 - Rectangle(4, 3)
        self.assertEqual(resRect.width, 1)
        self.assertEqual(resRect.height, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
