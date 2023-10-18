"""
3.
Используйте генератор случайных чисел для случайной расстановки ферзей в задаче выше. Проверяйте различный случайные варианты и выведите 4 успешных расстановки.

Под "успешной расстановкой ферзей" в данном контексте подразумевается такая расстановка ферзей на шахматной доске, в которой ни один ферзь не бьет другого.
Другими словами, ферзи размещены таким образом, что они не находятся на одной вертикали, горизонтали или диагонали.

Список из 4х комбинаций координат сохраните в board_list. Дополнительно печатать его не надо.
"""

from itertools import combinations
import random

BOARD_SIZE = 8
PEACE_COMB_NUM = 4 # ограничитель комбинаций, 0 - все комбинации


def is_attacking(q1: tuple[int, int], q2: tuple[int, int]) -> bool:
    return \
        q1[0] == q2[0] \
        or q1[1] == q2[1] \
        or abs(q2[0] - q1[0]) == abs(q2[1] - q1[1])


def check_queens(queens: list[tuple[int, int]]) -> bool:
    for q1, q2 in combinations(queens, 2):
        if is_attacking(q1, q2):
            return False
    return True


def printBoard(queens: list[tuple[int, int]]) -> None:
    board = [["·"] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    
    for i, j in queens:
        board[i][j] = chr(0x2655)

    print(" ", "".join([f"{n:>3}" for n in range(BOARD_SIZE)]))
    for n, row in enumerate(board):
        print(f"{n:>2} ", "  ".join(row))


def setQueen(board: list[list[int]], i: int, j: int, rem: bool = False) -> None:
    """
    Устанавливает (-> 1) на доску либо удаляет (-> 0) ферзя с доски, отмечая поля под боем (декремент 1) либо снимает отметку

    rem: True - удаление фигуры
    """
    inc = -1 if not rem else 1
    
    for k in range(BOARD_SIZE):
        board[i][k] += inc
        board[k][j] += inc
        if 0 <= i + j - k < BOARD_SIZE:
            board[i + j - k][k] += inc # диагональ л.н. - п.в.
        if 0 <= i - j + k < BOARD_SIZE:
            board[i - j + k][k] += inc # диагональ л.в. - п.н.
    
    board[i][j] = 1 if not rem else 0


def getQueens(board: list[list[int]]) -> list[tuple[int, int]]:
    """
    Формирует список с кортежами координат ферзей на доске
    """
    return [
        (i, j)
        for j in range(BOARD_SIZE)
        for i in range(BOARD_SIZE)
        if board[i][j] == 1
    ]


def findCombs(board: list[list[int]], rowList: list[int], resList: list[list[tuple[int, int]]]) -> None:
    """
    Рекурсивная функция для поиска комбинаций мирных ферзей

    rowList: список доступных строк
    """
    i = rowList.pop()
    for j in random.sample(list(range(BOARD_SIZE)), BOARD_SIZE):
        if board[i][j] == 0: # если поле свободно и не под боем
            setQueen(board, i, j)
            if not rowList: # условие выхода из рекурсии
                resList.append(getQueens(board))
            elif not PEACE_COMB_NUM or len(resList) < PEACE_COMB_NUM: # доп. условие выхода из рекурсии
                findCombs(board, rowList, resList)
            setQueen(board, i, j, rem=True) # возвращение состояния для поиска след. комбинации
    rowList.append(i) # возвращение состояния для вышележащего уровня рекурсии


def generate_boards() -> list[list[tuple[int, int]]]:
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        
    resList = []
    rowList = random.sample(list(range(BOARD_SIZE)), BOARD_SIZE)
    findCombs(board, rowList, resList)
    
    return resList


if __name__ == "__main__":
    import time
    startTime = time.time()

    board_list = generate_boards() 
    # print(len(board_list))
    print(time.time() - startTime)
    
    for n, queens in enumerate(board_list):
        print(f"\n{n + 1}.")
        printBoard(queens)
        print(queens)
        print(check_queens(queens))
