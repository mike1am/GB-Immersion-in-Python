"""
3.
Используйте генератор случайных чисел для случайной расстановки ферзей в задаче выше. Проверяйте различный случайные варианты и выведите 4 успешных расстановки.

Под "успешной расстановкой ферзей" в данном контексте подразумевается такая расстановка ферзей на шахматной доске, в которой ни один ферзь не бьет другого.
Другими словами, ферзи размещены таким образом, что они не находятся на одной вертикали, горизонтали или диагонали.

Список из 4х комбинаций координат сохраните в board_list. Дополнительно печатать его не надо.
"""
import random
import HW6_task3_funcs as funcs


def setQueen(board: list[list[int]], i: int, j: int, rem: bool = False) -> None:
    """
    Устанавливает (-> 1) на доску либо удаляет (-> 0) ферзя с доски, отмечая поля под боем (декремент 1) либо снимает отметку

    rem: True - удаление фигуры
    """
    inc = -1 if not rem else 1
    
    for k in range(len(board)):
        board[i][k] += inc # по строке
        board[k][j] += inc # по столбцу
        if 0 <= i + j - k < len(board):
            board[i + j - k][k] += inc # диагональ л.н. - п.в.
        if 0 <= i - j + k < len(board):
            board[i - j + k][k] += inc # диагональ л.в. - п.н.
    
    board[i][j] = 1 if not rem else 0


def getQueens(board: list[list[int]]) -> list[tuple[int, int]]:
    """
    Формирует список с кортежами координат ферзей на доске
    """
    return [
        (i, j)
        for j in range(len(board))
        for i in range(len(board))
        if board[i][j] == 1
    ]


def findCombs(board: list[list[int]], rowList: list[int], resList: list[list[tuple[int, int]]], solNum) -> None:
    """
    Рекурсивная функция для поиска комбинаций мирных ферзей

    rowList: список доступных строк
    """
    i = rowList.pop()
    for j in random.sample(range(len(board)), len(board)):
        if board[i][j] == 0: # если поле свободно и не под боем
            setQueen(board, i, j)
            if not rowList: # условие выхода из рекурсии
                resList.append(getQueens(board))
            elif not solNum or len(resList) < solNum: # доп. условие выхода из рекурсии
                findCombs(board, rowList, resList, solNum)
            setQueen(board, i, j, rem=True) # возвращение состояния для поиска след. комбинации
    rowList.append(i) # возвращение состояния для вышележащего уровня рекурсии


def generate_boards(boardSize=8, solNum=0) -> list[list[tuple[int, int]]]:
    """
    Возвращает список решений

    Args:
        boardSize: Размер доски
        solNum: Ограничение кол-ва решений. 0 - все
    """
    board = [[0] * boardSize for _ in range(boardSize)]
        
    resList = []
    rowList = random.sample(range(boardSize), boardSize)
    findCombs(board, rowList, resList, solNum)
    
    return resList


if __name__ == "__main__":
    import time
    BOARD_SIZE = 10
    SOL_NUM = 4

    startTime = time.time()

    board_list = generate_boards(BOARD_SIZE, SOL_NUM) 
    # print(len(board_list))
    print(time.time() - startTime)
    
    for n, queens in enumerate(board_list):
        print(f"\n{n + 1}.")
        funcs.printBoard(queens, BOARD_SIZE)
        print(queens)
        print(funcs.check_queens(queens))
