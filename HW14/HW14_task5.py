from typing import Any
import pytest


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


@pytest.fixture
def r():
    return (
        Rectangle(5),
        Rectangle(3, 4),
        Rectangle(10)
    )


def test_width(r):
    assert r[0].width == 5


def test_height(r):
    assert r[1].height == 4


def test_perimeter(r):
    assert r[0].perimeter() == 20


def test_area(r):
    assert r[1].area() == 12


def test_addition(r):
    resRect = r[0] + r[1]
    assert resRect.width == 8
    assert resRect.height == 6


def test_negative_width():
    with pytest.raises(RectangleError):
        Rectangle(-5)


def test_negative_height():
    with pytest.raises(RectangleError):
        Rectangle(5, -4)


def test_set_width(r):
    r[0].width = 10
    assert r[0].width == 10


def test_set_negative_width(r):
    with pytest.raises(RectangleError):
        r[0].width = -10


def test_set_height(r):
    r[1].height = 6
    assert r[1].height == 6


def test_set_negative_height(r):
    with pytest.raises(RectangleError):
        r[1].height = -6


def test_subtraction(r):
    resRect = r[2] - r[1]
    assert resRect.width == 7
    assert resRect.height == 6


def test_subtraction_negative_result(r):
    with pytest.raises(NegativeValueError):
        r[1] - r[2]


def test_subtraction_same_perimeter(r):
    resRect = r[0] - Rectangle(4, 3)
    assert resRect.width == 4
    assert resRect.height == 1


if __name__ == "__main__":
    pytest.main(["--no-header", '-q', "--durations=0", f'{__file__}'])
    # pytest.main([f'{__file__}', '-v'])
