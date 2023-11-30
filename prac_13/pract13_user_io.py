import pract13_exceptions as exc

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
    def  __init__(self, objClass):
        self.objClass = objClass

    def __iter__(self):
        prompt = f"\nВведите данные: {', '.join([field.desc for field in self.objClass.inputFields])} > "
        
        while True:
            inputStr = input(prompt)
            if not inputStr:
                break

            inputList = [s.strip(" ,;") for s in inputStr.split(",")]
            try:
                if len(inputList) != len(self.objClass.inputFields):
                    raise exc.UserInputError(f"Ожидаемое кол. параметров: {len(self.objClass.inputFields)}")

                yield self.objClass(*inputList)
            
            except exc.UserError as err:
                printErr(err)


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
        inpList = [s.strip(" ,;") for s in input(prompt).split(",")]
        
        try:
            if len(inpList) != pNum:
                raise exc.UserInputError(f"Ожидаемое кол. параметров: {pNum}")

        except exc.UserError as err:
            printErr(err)

        else:
            return inpList

def printErr(msg):
    print(f"\033[31m{msg}\033[0m")
