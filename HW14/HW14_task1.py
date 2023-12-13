from typing import Any


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
    """
    Тест1:
    >>> r1 = Rectangle(5)
    >>> r1.width
    5
    >>> r4 = Rectangle(-2)
    Traceback (most recent call last):
    ...
    RectangleError

    Тест2:
    >>> r2 = Rectangle(3, 4)
    >>> r2.width
    3
    >>> r2.height
    4

    Тест3:
    >>> r1 = Rectangle(5)
    >>> r1.perimeter()
    20
    >>> r2 = Rectangle(3, 4)
    >>> r2.perimeter()
    14

    Тест4:
    >>> r1 = Rectangle(5)
    >>> r1.area()
    25
    >>> r2 = Rectangle(3, 4)
    >>> r2.area()
    12

    Тест5:
    >>> r1 = Rectangle(5)
    >>> r2 = Rectangle(3, 4)
    >>> r3 = r1 + r2
    >>> r3.width
    8
    >>> r3.height
    6.0

    Тест6:
    >>> r1 = Rectangle(5)
    >>> r2 = Rectangle(3, 4)
    >>> r3 = r1 - r2
    >>> r3.width
    2
    >>> r3.height
    2.0
    """
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
    

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
