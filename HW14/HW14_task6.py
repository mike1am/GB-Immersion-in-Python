import pytest


class InvalidValue(Exception):
    pass


class InvalidPersonData(InvalidValue):
    pass


class InvalidNameError(InvalidPersonData):
    def __str__(self):
        return "Неверное имя"


class InvalidAgeError(InvalidPersonData):
    def __str__(self):
        return "Неверный возраст"


class InvalidIdError(InvalidValue):
    def __init__(self, id=None):
        self.id = id

    def __str__(self):
        return (
            f"Ид. сотрудника {self.id} уже существует"
            if self.id
            else "Некорректный ид. сотрудника"
        )


class Name:
    def __set_name__(self, owner, name):
        self.attrName = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.attrName)

    def __set__(self, instance, value):
        if not isinstance(value, str) or not str.isalpha(value):
            raise InvalidNameError
        setattr(instance, self.attrName, value.title())


class Person:
    firstName = Name()
    middleName = Name()
    lastName = Name()
    
    def __init__(self, firstName, middleName, lastName, age) -> None:
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.age = age

    def __setattr__(self, attrName: str, value) -> None:
        try:
            super().__setattr__(attrName, value)
        except InvalidValue as err:
            print(err)
            # pass

    def birthday(self):
        if self.age:
            self.age += 1

    @property
    def age(self):
        if hasattr(self, '_age'):
            return self._age
        else:
            return None
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0:
            raise InvalidAgeError
        self._age = value

    def get_age(self):
        return self.age
    
    def full_name(self):
        return " ".join((
            self.lastName,
            self.firstName,
            self.middleName
        ))


class Employee(Person):
    def __init__(self, lastName, firstName, middleName, age, position="", salary=0) -> None:
        super().__init__(firstName, middleName, lastName, age)
        self.position = position.title()
        self.salary = salary

    def raise_salary(self, percent: float):
        self.salary *= (1 + percent / 100)

    def __str__(self):
        return f'{self.full_name()} ({self.position})'
    

@pytest.fixture
def emp():
    return Employee("Ivanov", "Ivan", "Ivanovich", 30, "manager", 50_000)


def test_employee_full_name(emp):
    assert emp.full_name() == "Ivanov Ivan Ivanovich"


def test_employee_birthday(emp):
    emp.birthday()
    assert emp.age == 31


def test_employee_raise_salary(emp):
    emp.raise_salary(10)
    assert emp.salary == 55_000.0


def test_employee_str(emp):
    assert str(emp) == "Ivanov Ivan Ivanovich (Manager)"


def test_employee_last_name_title(emp):
    assert emp.lastName == "Ivanov"


if __name__ == "__main__":
    pytest.main(["--no-header", '-q', "--durations=0", __file__])
