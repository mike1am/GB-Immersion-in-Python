import json
import pickle
import os
import logging
import getpass
import random
import string
from hashlib import pbkdf2_hmac

import HW15_exceptions as exc
from HW15_user_io import LoopInput, fieldInput, printErr

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
                f"Уровень доступа должен лежать в границах [{self.scopes[0]}-{self.scopes[1] - 1}] включительно"
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
        f"Уровень доступа [{ACC_LEVEL_SCOPES[0]}-{ACC_LEVEL_SCOPES[1] - 1}]"
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
    - checkUser - проверка имени и ид. пользователя. Возвращает объект кл. User,
        если ид. зарегистрирован и имя соответствует ид., а также если пользователь
        ввёл правильный пароль, еначе генерирует соответствующее исключение
    - 

    
    Переопределённые операции (dunder):
    - __contains__ - определение вхождения экземпляра User по id
    - __getitem__ - возвращение экземпляра User по id
    - __bool__ - возвращает True, если _userSet непустой
    """
    def __init__(self, fName = "") -> None:
        self._userSet = set()
        self.jsonName = fName + ".json"
        self.pickleName = fName + ".pickle"

    def __enter__(self):
        if os.path.exists(self.jsonName):
            try:
                with open(self.jsonName, "r", encoding="utf-8") as inFile:
                    jsonDict = json.load(inFile)

            except (OSError, json.decoder.JSONDecodeError):
                printErr(f"Ошибка загрузки файла {self.jsonName}", logging.ERROR)
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
            with open(self.jsonName, "w", encoding="utf-8") as outFile:
                json.dump(userDict, outFile, indent=2, ensure_ascii=False)
        except OSError:
            printErr(f"Ошибка выгрузки файла {self.jsonName}", logging.ERROR)

    def update(self, user):
        """
        Обновление или добавление пользователя в множество

        Args:
            user: добавляемый пользователь
        """
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
    
    def checkUser(self, uName, uId):
        """
        Проверка имени и ид. пользователя. Возвращает объект кл. User,
        если ид. зарегистрирован и имя соответствует ид., а также если пользователь
        ввёл правильный пароль, иначе генерирует соответствующее исключение

        Raises:
            exc.UserAccessError: при невыполнении условий проверки

        Returns:
            Объект кл. User, если ид. зарегистрирован и имя соответствует ид.
        """
        if User(uName, uId, "1") in self:
            actUser = self[uId]
            if actUser.name == uName:
                if self.checkPswd(actUser):
                    return actUser
                raise exc.UserAccessError(f"Неверный пароль пользователя {uName}")
            else:
                raise exc.UserAccessError(f"Имя пользователя {uName} не соответствует ид. {uId}")
        else:
            raise exc.UserAccessError(f"Пользователь {uName} с ид. {uId} не найден")
    
    ITER_NUM = 500_000
    CRYPT_ALG = "sha1"
    SOLT_LEN = 20
        
    def checkPswd(self, user):
        """
        Проверка пароля. Запрос пароля к ком. строке

        Args:
            user: проверяемый пользователь

        Returns:
            True, если проверка прошла успешно, иначе - False
        """
        try:
            with open(self.pickleName, "rb") as pswdFile:
                pswdDict = pickle.load(pswdFile)
        except (OSError, EOFError):
            return False

        if user.id in pswdDict:
            pswd = getpass.getpass("Введите пароль: ")
            inpHash = pbkdf2_hmac(self.CRYPT_ALG, bytearray(pswd, "utf-8"), pswdDict[user.id]['solt'], self.ITER_NUM)
            if inpHash == pswdDict[user.id]['hash']:
                return True

        return False
            
    def newPswd(self, user):
        """
        Ввод нового пароля для пользователя

        Args:
            user: пользователь, для которого вводится новый пароль
        """
        with open(self.pickleName, "rb+" if os.path.exists(self.pickleName) else "wb") as pswdFile:
            try:
                pswdDict = pickle.load(pswdFile)
            except (OSError, EOFError):
                pswdDict = {}
        
            pswd = getpass.getpass(f"Введите новый пароль для пользователя {user.name}: ")
            solt = bytearray("".join(random.choice(string.ascii_letters + string.digits) for _ in range(self.SOLT_LEN)),
                                "utf-8")
            pswdHash = pbkdf2_hmac(self.CRYPT_ALG, bytearray(pswd, "utf-8"), solt, self.ITER_NUM)
            pswdDict[user.id] = {'solt': solt, 'hash': pswdHash}

            pswdFile.seek(0)
            pickle.dump(pswdDict, pswdFile)

    def initPswd(self):
        """
        Инициализация: создание пользователя admin и задание для него пароля
        """
        admin = User("admin", "0", str(ACC_LEVEL_SCOPES[1] - 1))
        self.update(admin)
        self.newPswd(admin)


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
        Процедура аутентификации. В диалоге запрашивает имя и ид. пользователя,
        либо получает их из параметров, переданных при вызове программы.
        Сохраняет в атрибуте класса actUser пользователя, прошедшего аутентификацию.

        Args:
            inputFunc: функция, возвращающая параметры для аутентификации
        """
        if self.userSet:
            prompt = "Введите имя и ид. пользователя для аутентификации: "
            pNum=2
        else:
            prompt = "\nВведите данные первого пользователя: Имя, Ид., Уровень доступа"\
                     f" [{ACC_LEVEL_SCOPES[0]}-{ACC_LEVEL_SCOPES[1] - 1}]"\
                     "\nПользователь будет использован для дальнейшей аутентификации > "
            pNum=3

        while True:
            try:
                if self.userSet:
                    uName, uId = inputFunc(prompt, pNum=pNum)
                    
                    self.actUser = self.userSet.checkUser(uName, uId)
                    logger.info(f"Осуществлён вход: {self.actUser}")
                    return
                    
                # если json файла ещё нет, вводится ещё уровень доступа и параллельно с аутентификацией происходит регистрация пользователя
                else:
                    inpTuple = inputFunc(prompt, pNum=pNum)
                    uName, uId, accLevel = (
                        inpTuple[i - 3 + len(inpTuple)] if len(inpTuple) - 3 + i >= 0 else (uName, uId, accLevel)[i]
                        for i in range(3)
                    )
                    
                    if not accLevel:
                        inputFunc=fieldInput
                        prompt = f"Введите уровень доступа пользователя {uName} для аутентификации"\
                                 f" [{ACC_LEVEL_SCOPES[0]}-{ACC_LEVEL_SCOPES[1] - 1}]: "
                        pNum = 1
                        continue
                    self.actUser = User(uName, uId, accLevel)
                    self.userSet.update(self.actUser)
                    self.userSet.newPswd(self.actUser)
                    logger.info(f"Добавлен пользователь и осуществлён вход: {self.actUser}")
                    return
            
            except exc.UserError as err:
                printErr(err, logging.WARNING)
                inputFunc=fieldInput
            
            except KeyboardInterrupt:
                logger.info("Выход из программы без аутентификации")
                exit()

    def go(self, inpFunc=fieldInput):
        """
        Основной цикл проекта - запрос данных добавляемых пользователей
        """
        for user in LoopInput(User, inpFunc):
            try:
                if user in self.userSet:
                    raise exc.AttrValueError(
                        f"Невозможно добавить {user.name} - пользователь уже есть: {self.userSet[user.id]}"
                    )
                if user > self.actUser:
                    raise exc.AccessLevelError(f"Вашего уровня доступа {self.actUser.accLevel} недостаточно, "\
                                               f"чтобы добавить пользователя с уровнем {user.accLevel}")

            except exc.UserError as err:
                printErr(err, logging.WARNING)

            else:
                self.userSet.update(user)
                self.userSet.newPswd(user)
                print(f"\033[33mУспешно добавлено: \n{user}\033[0m")
                logger.info(f"Успешно добавлено: {user}")

        logger.info(f"Выход из программы: {self.actUser}")
        


def main(fName):

    argParser = argparse.ArgumentParser(description="Учёт пользователей")
    argParser.add_argument('uName', metavar="Name", type=str, nargs=1, help="Имя пользователя")
    argParser.add_argument('uId', metavar="Identifier", type=str, nargs=1, help="Идентификатор пользователя")
    argParser.add_argument('-l', metavar="Access Level", type=int, choices=range(*ACC_LEVEL_SCOPES), nargs=1,
                           help=f"Уровень доступа [{ACC_LEVEL_SCOPES[0]}-{ACC_LEVEL_SCOPES[1] - 1}]"\
                                " (только для нового json файла, иначе игнорируется)")

    args = argParser.parse_args()

    def getArgs(*largs, pNum, **kwargs):
        return (
            (args.uName[0], args.uId[0])
            if pNum == 2
            else (args.uName[0], args.uId[0], args.l[0] if args.l else None)
        )
    
    with Users(fName) as userSet:
        project = Project(userSet)
        project.auth(inputFunc=getArgs)
        project.go()


FILE_NAME = r"Users"

if __name__ == "__main__":
    from HW15_logging import logger
    import argparse
    
    main(FILE_NAME)
