"""
Программа загадывает число от 0 до 1000. Необходимо угадать число за 10 попыток.
Программа должна подсказывать «больше» или «меньше» после каждой попытки.
"""

from random import randint

LOWER_LIMIT = 0
UPPER_LIMIT = 1000
ATTEMPTS = 10

num = randint(LOWER_LIMIT, UPPER_LIMIT)
print(f"Угадайте число от {LOWER_LIMIT} до {UPPER_LIMIT}")

for att in range(1, ATTEMPTS + 1):
    attNum = int(input(f"Попытка {att} из {ATTEMPTS}. Введите число: "))
    if attNum == num:
        print(f"\033[33mУра, Вы угадали!\033[0m")
        break
    
    if attNum > num:
        print(f"\033[31mМеньше, чем {attNum}\033[0m")
    else:
        print(f"\033[31mБольше, чем {attNum}\033[0m")

else:
    print(f"Вам не хватило попыток((. Это было число {num}")
