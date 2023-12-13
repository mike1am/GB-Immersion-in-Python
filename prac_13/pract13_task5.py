import json
import os

import pract13_exceptions as exc
from pract13_user_io import LoopInput, fieldInput, printErr

class Field:
    def __init__(self, desc):
        self.desc = desc

    def __set_name__(self, owner, name):
        self.attrName = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.attrName)

class Name(Field):
    def __set__(self, instance, value):
        if not str.isalpha(value.replace(" ", "")):
            raise exc.AttrValueError("Имя пользователя может содержать только буквы")
        
        setattr(instance, self.attrName, value)

class Identifier(Field):
    def __set__(self, instance, value):
        if not str.isnumeric(value):
            raise exc.AttrValueError("Идентификатор пользователя должен быть целым положительным числом")
         
        setattr(instance, self.attrName, value)

class AccLevel(Field):
    def __init__(self, scopes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scopes = scopes

    def __set__(self, instance, value):
        if not str.isnumeric(value):
            raise exc.AttrValueError("Уровень доступа должен быть целым положительным числом")
        
        if not (self.scopes[0] <= int(value) < self.scopes[1]):
            raise exc.AccessLevelError(
                f"Уровень доступа должен лежать в границах [{self.scopes[0]} - {self.scopes[1] - 1}] включительно"
            )
        
        setattr(instance, self.attrName, value)


ACC_LEVEL_SCOPES = (1, 8)


class User:
    """
    Класс пользователя. Хранит атрибуты:
    - name - имя пользоователя
    - id - числовой идертификатор пользователя
    - accLevel - уровень доступа

    Поддержка протокола для класса LoopInput

    Аргументы конструктора:
    - name - имя пользоователя
    - id - числовой идертификатор пользователя
    - accLevel - уровень доступа
    
    Переопределённые операции (dunder):
    - __str__
    - __eq__ - сравнение по id
    - __lt__, __gt__ - сравнение по accLevel
    - __hash__ - возвращает int(id)
    """
    name = Name("Имя пользователя")
    id = Identifier("Числовой идентификатор пользователя")
    accLevel = AccLevel(
        ACC_LEVEL_SCOPES,
        f"Уровень доступа [{ACC_LEVEL_SCOPES[0]} - {ACC_LEVEL_SCOPES[1] - 1}]"
    )

    inputFields = (name, id, accLevel)

    def __init__(self, name, id, accLevel) -> None:
        self.name = name
        self.id = id
        self.accLevel = accLevel

    def __str__(self):
        return f"Пользователь: {self.name}, ид.: {self.id}, уровень доступа: {self.accLevel}"

    def __eq__(self, other) -> bool:
        return self.id == other.id
    
    def __lt__(self, other) -> bool:
        return self.accLevel < other.accLevel
    
    def __gt__(self, other) -> bool:
        return self.accLevel > other.accLevel
            
    def __hash__(self) -> int:
        return int(self.id)
    

class Users:
    """
    Контейнер для множества пользователей (класс User)
    
    Поддержка менеджера контекста. Параметр - имя json файла.
    При входе - загрузка данных из файла, если существует.
    При выходе сохраняет данные в json файл.

    Аргументы конструктора:
    - fName - имя json файла для загрузки данных пользователей (если существует),
    а также для выгрузки данных, по умолчанию - ""
    
    Методы:
    - update - обновление или добавление пользователя в множество
    
    Переопределённые операции (dunder):
    - __contains__ - определение вхождения экземпляра User по id
    - __getitem__ - возвращение экземпляра User по id
    """
    def __init__(self, fName = "") -> None:
        self._userSet = set()
        self.fName = fName

    def __enter__(self):
        if os.path.exists(self.fName):
            try:
                with open(self.fName, "r", encoding="utf-8") as inFile:
                    jsonDict = json.load(inFile)

            except (OSError, json.decoder.JSONDecodeError):
                printErr(f"Ошибка загрузки файла {self.fName}")
                jsonDict = {}

            for accLevel, accDict in jsonDict.items():
                if str.isnumeric(accLevel) and ACC_LEVEL_SCOPES[0] <= int(accLevel) < ACC_LEVEL_SCOPES[1]:
                    for uId, uName in accDict.items():
                        if str.isalpha(uName.replace(" ", "")) and str.isnumeric(uId):
                            self.update(User(uName, uId, accLevel))
        return self

    def __exit__(self, *args):
        userDict = {str(al): {} for al in range(*ACC_LEVEL_SCOPES)}
        for user in self._userSet:
            userDict[user.accLevel].update({user.id: user.name})
        
        try:
            with open(self.fName, "w", encoding="utf-8") as outFile:
                json.dump(userDict, outFile, indent=2, ensure_ascii=False)
        except OSError:
            printErr(f"Ошибка выгрузки файла {self.fName}")

    def update(self, user):
        if not user in self._userSet:
            self._userSet.add(user)
        else:
            for user_ in self._userSet:
                if user == user_:
                    user_.name = user.name
                    user_.accLevel = user.accLevel
            
    def __contains__(self, user):
        return user in self._userSet
    
    def __getitem__(self, id):
        for user in self._userSet:
            if user.id == id:
                return user
        return None
    
    def __bool__(self):
        return bool(self._userSet)
    

class Project:
    """
    Класс хранит экземпляр Users (множество пользователей)
    
    Атрибуты:
    - userSet: Users - контейнер множества пользователей
    - actUser: User - пользователь, прошедший аутентификацию

    Аргументы конструктора:
    - userSet - объект класса Users
    
    Методы:
    - auth - аутентификация: в диалоге получает имя и ид. пользователя
    - go - цикл добавления пользователей с проверкой уровня доступа
    """
    def __init__(self, userSet) -> None:
        self.userSet = userSet

    def auth(self, inputFunc=fieldInput):
        """
        Процедура аутентификации. В диалоге запрашивает имя и ид. пользователя.
        Сохраняет в атрибуте класса actUser пользователя, прошедшего аутентификацию.
        """
        while True:
            try:
                if self.userSet:
                    uName, uId = inputFunc("Введите имя и ид. пользователя для аутентификации: ", 2)
                    if User(uName, uId, "1") in self.userSet:
                        actUser = self.userSet[uId]
                        if actUser.name == uName:
                            self.actUser = actUser
                            return
                        else:
                            raise exc.UserAccessError("Имя пользователя не соответствует ид.")
                    else:
                        raise exc.UserAccessError("Пользователь не найден")
                else:
                    uName, uId, accLevel = inputFunc(
                        "\nВведите данные первого пользователя: Имя, Ид., Уровень доступа" + \
                        "\nПользователь будет использован для дальнейшей аутентификации > ",
                        3
                    )
                    self.actUser = User(uName, uId, accLevel)
                    self.userSet.update(self.actUser)
                    return
            
            except exc.UserError as err:
                printErr(err)

    def go(self, inpFunc=fieldInput):
        """
        Основной цикл проекта - запрос данных добавляемых пользователей.
        """
        for user in LoopInput(User, inpFunc):
            try:
                if user in self.userSet:
                    raise exc.AttrValueError("Такой идентификатор пользователя уже есть")
                if user > self.actUser:
                    raise exc.AccessLevelError

            except exc.UserError as err:
                printErr(err)

            else:
                self.userSet.update(user)
                print(f"\033[33mУспешно добавлено: \n{user}\033[0m")


def main():
    with Users(fName) as userSet:
        project = Project(userSet)
        project.auth()
        project.go()


if __name__ == "__main__":
    fName = r"prac_13\task5.json"
    
    main()
