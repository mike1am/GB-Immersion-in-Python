import HW15_exceptions as exc
from HW15_logging import logger
import logging


def fieldInput(prompt, pNum):
    """
    Пользовательский ввод параметров через запятую.

    Args:
        - prompt: запрос на ввод
        - pNum: кол. запрашиваемых параметров

    Returns:
        Список строк - введённых параметров
    """
    while True:
        inpList = [s.strip(" ,;") for s in input(prompt).split()]
        
        try:
            if len(inpList) != pNum:
                raise exc.UserInputError(f"Ожидаемое кол. параметров: {pNum}")

        except exc.UserError as err:
            printErr(err, logging.NOTSET)

        else:
            return inpList


class LoopInput:
    """
    Класс-итератор, циклически запрашивающий ввод данных для класса, переданного при инициализации.
    Класс создаваемых объектов должен содержать атрибут `inputFields` с кортежем вводимых полей.

    Аргументы конструктора:
    - objClass - класс создаваемых объектов

    Обрабатывает исключения UserError
    
    Yields:
        Объекты заданного класса
    """
    def  __init__(self, objClass, inpFunc=fieldInput):
        self.objClass = objClass
        self.inpFunc = inpFunc

    def __iter__(self):
        prompt = f"\nВведите данные: {', '.join([field.desc for field in self.objClass.inputFields])} > "
        
        while True:
            try:
                inputList = self.inpFunc(prompt, len(self.objClass.inputFields))
                yield self.objClass(*inputList)
            
            except exc.UserError as err:
                printErr(err, logging.DEBUG)

            except KeyboardInterrupt:
                break


def printErr(msg, level):
    logger.log(level, msg)
    print(f"\033[31m{msg}\033[0m")
