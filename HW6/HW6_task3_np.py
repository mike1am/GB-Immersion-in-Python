"""
3.
Используйте генератор случайных чисел для случайной расстановки ферзей в задаче выше. Проверяйте различный случайные варианты и выведите 4 успешных расстановки.

Под "успешной расстановкой ферзей" в данном контексте подразумевается такая расстановка ферзей на шахматной доске, в которой ни один ферзь не бьет другого.
Другими словами, ферзи размещены таким образом, что они не находятся на одной вертикали, горизонтали или диагонали.

Список из 4х комбинаций координат сохраните в board_list. Дополнительно печатать его не надо.
"""

from itertools import combinations
import random
import numpy as np

BOARD_SIZE = 8
PEACE_COMB_NUM = 0 # ограничитель комбинаций, 0 - все комбинации


def printBoard(queens: list[tuple[int, int]]) -> None:
    board = [["·"] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    
    for i, j in queens:
        board[i][j] = chr(0x2655)

    print(" ", "".join([f"{n:>3}" for n in range(BOARD_SIZE)]))
    for n, row in enumerate(board):
        print(f"{n:>2} ", "  ".join(row))


def setQueen(board: np.matrix, i: np.int8, j: int, rem: bool = False) -> None:
    """
    Устанавливает (-> 1) на доску либо удаляет (-> 0) ферзя с доски, отмечая поля под боем (декремент 1) либо снимает отметку

    rem: True - удаление фигуры
    """
    inc = -1 if not rem else 1
    
    board[i] += inc
    board[:,j] += inc
    
    for k in np.arange(BOARD_SIZE):
        if 0 <= i + j - k < BOARD_SIZE:
            board[i + j - k, k] += inc # диагональ л.н. - п.в.
        if 0 <= i - j + k < BOARD_SIZE:
            board[i - j + k, k] += inc # диагональ л.в. - п.н.
    
    board[i, j] = 1 if not rem else 0


def getQueens(board: list[list[int]]) -> list[tuple[int, int]]:
    """
    Формирует список с кортежами координат ферзей на доске
    """
    return [
        (i, j)
        for j in np.arange(BOARD_SIZE, dtype=np.int8)
        for i in np.arange(BOARD_SIZE, dtype=np.int8)
        if board[i, j] == 1
    ]


def findCombs(board: np.matrix[np.int8], rowArray: np.array, resList: list[list[int, int]]) -> None:
    """
    Рекурсивная функция для поиска комбинаций мирных ферзей

    rowArray: список доступных строк
    """
    i = rowArray[-1]
    row = np.array(range(BOARD_SIZE), np.int8)
    # np.random.shuffle(row)
    for j in row:
        if board[i, j] == 0: # если поле свободно и не под боем
            setQueen(board, i, j)
            if len(rowArray) == 1: # условие выхода из рекурсии
                resList.append(getQueens(board))
            elif not PEACE_COMB_NUM or len(resList) < PEACE_COMB_NUM: # доп. условие выхода из рекурсии
                findCombs(board, rowArray[:-1], resList)
            setQueen(board, i, j, rem=True) # возвращение состояния для поиска след. комбинации


def generate_boards() -> list[list[tuple[int, int]]]:
    board = np.matrix(np.zeros((BOARD_SIZE,) * 2, np.int8))
        
    resList = []
    rowArray = np.array(random.sample(range(BOARD_SIZE), BOARD_SIZE), np.int8)
    findCombs(board, rowArray, resList)
    
    return resList


if __name__ == "__main__":
    import time
    startTime = time.time()

    board_list = generate_boards() 
    print(len(board_list))
    print(time.time() - startTime)
    
    # for n, queens in enumerate(board_list):
    #     print(f"\n{n + 1}.")
    #     printBoard(queens)
    #     print(queens)
