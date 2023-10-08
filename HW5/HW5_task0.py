"""
✔ Выведите в консоль таблицу умножения
от 2х2 до 9х10 как на школьной тетрадке.
✔ Таблицу создайте в виде однострочного
генератора, где каждый элемент генератора —
отдельный пример таблицы умножения.
✔ Для вывода результата используйте «принт»
без перехода на новую строку.
"""

import math

MIN_MULT = 2
MAX_MULT = 10
MIN_NUM = 2
TOTAL_COLS = 8

def multStr(n1, n2):
    return \
        str(n1).rjust(2) + \
        " x" + \
        str(n2).rjust(2) + \
        " = " + \
        str(n1 * n2).rjust(2)


def multCol(num):
    for m in range(MIN_MULT, MAX_MULT + 1):
        yield multStr(num, m)


def multTable(cols):
    res = ["\n"]

    for row in range(math.ceil(TOTAL_COLS / cols)):
        colGens = [
            multCol(row * cols + col + MIN_NUM)
            for col in range(cols)
            if row * cols + col < TOTAL_COLS
        ]
        while True:
            try:
                res.append(
                    "\n" + "   ".join([next(colGen) for colGen in colGens])
                )
            except StopIteration:
                break
        
        res.append("\n")

    return "\n" + "Таблица умножения".upper().center(len(res[1])) + \
        "".join(res)


print(multTable(cols=4))
