"""
3.
Используйте генератор случайных чисел для случайной расстановки ферзей в задаче выше. Проверяйте различный случайные варианты и выведите 4 успешных расстановки.

Под "успешной расстановкой ферзей" в данном контексте подразумевается такая расстановка ферзей на шахматной доске, в которой ни один ферзь не бьет другого.
Другими словами, ферзи размещены таким образом, что они не находятся на одной вертикали, горизонтали или диагонали.

Список из 4х комбинаций координат сохраните в board_list. Дополнительно печатать его не надо.
"""
import random
import numpy as np
import HW6_task3_funcs as funcs


def setQueen(board: np.array, i: int, j: int, rem: bool = False) -> None:
    """
    Устанавливает (-> 1) на доску либо удаляет (-> 0) ферзя с доски, отмечая поля под боем (декремент 1) либо снимает отметку

    rem: True - удаление фигуры
    """
    inc = -1 if not rem else 1

    board[i] += inc # по строке
    board[:, j] += inc # по столбцу
    for _ in range(2): # по диагонялям: 1ый проход л.в.-п.н., 2ой - л.н.-п.в.
        triFunc, diagAddOffset = \
                (np.tril_indices_from, -1) \
                if i >= j \
                else (np.triu_indices_from, 1) # для уменьшения объёма работы функции triFunc
        board[triFunc(board, j - i)] += inc # по треугольнику
        board[triFunc(board, j - i + diagAddOffset)] -= inc # возвращение значений треугольника, кроме диагонали
        
        board = board[::-1] # переворот матрицы по вертикали
        i = len(board) - i - 1

    board[i, j] = 1 if not rem else 0


def setQueen1(board: np.array, i: int, j: int, rem: bool = False) -> None:
    """
    Устанавливает (-> 1) на доску либо удаляет (-> 0) ферзя с доски, отмечая поля под боем (декремент 1) либо снимает отметку

    rem: True - удаление фигуры
    """
    inc = -1 if not rem else 1
    
    board[ # формирование индексов: картеж из 2х массивов np.array с индексами - строки и столбцы
        np.concatenate(( # индексы строк
            np.repeat(i, len(board)), # по строке
            np.arange(len(board)), # по столбцу
            np.arange( # по диагонали л.в.-п.н.
                max(0, i - j),
                min(len(board) + i - j, len(board))
            ),
            np.arange( # по диагонали л.н.-п.в.
                min(i + j, len(board) - 1),
                max(-1, i + j - len(board)),
                -1
            )
        )),
        np.concatenate(( # индексы столбцов
            np.arange(len(board)), # по строке
            np.repeat(j, len(board)), # по столбцу
            np.arange( # по диагонали л.в.-п.н.
                max(0, j - i),
                min(len(board) + j - i, len(board))
            ),
            np.arange( # по диагонали л.н.-п.в.
                max(0, i + j - len(board) + 1),
                min(i + j + 1, len(board))
            )
        ))
    ] += inc
    
    board[i, j] = 1 if not rem else 0


def getQueens(board: np.array) -> list[tuple[int, int]]:
    """
    Формирует список с кортежами координат ферзей на доске
    """
    return list(map(tuple, np.array(np.where(board == 1)).T))


def findCombs(board: np.array, rowList: list[int], resList: list[list[tuple[int, int]]], solNum) -> None:
    """
    Рекурсивная функция для поиска комбинаций мирных ферзей

    rowList: список доступных строк
    """
    i = rowList.pop()
    for j in random.sample(range(len(board)), len(board)): # для разных результатов при ограничении кол. решений
        if board[i, j] == 0: # если поле свободно и не под боем
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
    board = np.array(np.zeros((boardSize,) * 2, dtype=int)) # матрица, заполненная нулями
        
    resList = []
    rowList = random.sample(range(boardSize), boardSize) # для разных результатов при ограничении кол. решений
    findCombs(board, rowList, resList, solNum)
    
    return resList


if __name__ == "__main__":
    import time

    BOARD_SIZE = 50
    SOL_NUM = 5
        
    # numpy - манипуляции с треугольниками
    generate_boards = funcs.logTime(generate_boards)

    # board_list = generate_boards(BOARD_SIZE, SOL_NUM) 
    # print(len(board_list))

    # numpy - формирование массивов индексов
    setQueen = setQueen1

    board_list = generate_boards(BOARD_SIZE, SOL_NUM)
    print(len(board_list))
    
    # чистый python
    import HW6_task3 as wo_np
    generate_boards = funcs.logTime(wo_np.generate_boards)

    board_list = generate_boards(BOARD_SIZE, SOL_NUM)
    print(len(board_list))
    
    # for n, queens in enumerate(board_list):
    #     print(f"\n{n + 1}.")
    #     funcs.printBoard(queens, BOARD_SIZE)
    #     print(queens)
    #     print(funcs.check_queens(queens))
