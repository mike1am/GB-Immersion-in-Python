"""
Напишите программу, которая получает целое число и возвращает его шестнадцатеричное строковое представление.
Функцию hex используйте для проверки своего результата.
"""

from ui import userInput
DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


# преобразование только неотрицательных целых чисел
def convToBase(num :int, base :int) -> str:
    outStr = "0" if num == 0 else "" 
    while num > 0:
        dig = num % base
        outStr = DIGITS[dig] + outStr
        num //= base
    
    return outStr


while True:
    inStr = userInput("Введите целое неотрицательное число, или пустой ввод для выхода: ", lambda uInp: not uInp or int(uInp) >= 0)
    if not inStr:
        break
    hexStr = convToBase(int(inStr), 16)

    print(f"Шестнадцатеричное представление: {hexStr}; результат проверки: {'0x' + hexStr == hex(int(inStr))}")
