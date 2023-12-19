import random
import logging
from copy import copy, deepcopy
from HW15_logging import perfLog, logger


class ChessBoard:
    def __init__(self, size, logger=None):
        self.size = size
        self._attackArray =  [[0] * size for _ in range(size)]
        self._figureDict = {
            'queen': set()
        }
        self.logger = logger
    
    def setQueen(self, i: int, j: int, rem: bool = False):
        """
        Устанавливает на доску либо удаляет ферзя с доски
        rem: True - удаление фигуры
        """
        inc = -1 if not rem else 1
        for k in range(self.size):
            self._attackArray[i][k] += inc # по строке
            self._attackArray[k][j] += inc # по столбцу
            if 0 <= i + j - k < self.size:
                self._attackArray[i + j - k][k] += inc # диагональ л.н. - п.в.
            if 0 <= i - j + k < self.size:
                self._attackArray[i - j + k][k] += inc # диагональ л.в. - п.н.
        
        if not rem:
            self._figureDict['queen'].add((i, j))
        else:
            self._figureDict['queen'].remove((i, j))

        if self.logger:
            self.logger.debug(f"Queen {'removed' if rem else 'set'} at {i, j}")


    def __getitem__(self, coords):
        for figure in self._figureDict:
            if coords in self._figureDict[figure]:
                return figure
        return self._attackArray[coords[0]][coords[1]]
    
    def isPeaceful(self, i, j):
        return self[(i, j)] == 0
    
    def __copy__(self):
        res = self.__class__(self.size)
        res.__dict__.update(self.__dict__)

        res._figureDict = deepcopy(self._figureDict)
        
        return res

    def __deepcopy__(self):
        res = self.__class__()
        res.__dict__.update(self.__dict__)

        res._attackArray = deepcopy(self._attackArray)
        res._figureDict = deepcopy(self._figureDict)
        
        return res
    
    def __str__(self):
        CHARS_DICT = {
            'queen': chr(0x2655),
        }
        
        canvas = [["·"] * self.size for _ in range(self.size)]
    
        for figure in self._figureDict:
            for i, j in self._figureDict[figure]:
                canvas[i][j] = CHARS_DICT[figure]

        res = " " + "".join([f"{n:>3}" for n in range(self.size)])
        for n, row in enumerate(canvas):
            res += f"\n{n:>2} " + "  ".join(row)

        return res


def findPeaceQueensCombs(board, rowList, resList, solNum) -> None:
    """
    Рекурсивная функция для поиска комбинаций мирных ферзей

    rowList: список доступных строк
    """
    i = rowList.pop()
    for j in random.sample(range(board.size), board.size):
        if board.isPeaceful(i, j): # если поле свободно и не под боем
            board.setQueen(i, j)
            if not rowList: # условие выхода из рекурсии
                resList.append(copy(board))
                logger.info(f"Combination found: {board._figureDict['queen']}")
            elif not solNum or len(resList) < solNum: # доп. условие выхода из рекурсии
                findPeaceQueensCombs(board, rowList, resList, solNum)
            board.setQueen(i, j, rem=True) # возвращение состояния для поиска след. комбинации
    rowList.append(i) # возвращение состояния для вышележащего уровня рекурсии


@perfLog(logger)
def generatePeaceBoards(boardSize=8, solNum=4):
    """
    Возвращает список решений

    Args:
        boardSize: Размер доски
        solNum: Ограничение кол-ва решений. 0 - все
    """
    board = ChessBoard(boardSize, logger)
        
    resList = []
    rowList = random.sample(range(boardSize), boardSize)
    findPeaceQueensCombs(board, rowList, resList, solNum)
    
    return resList


@perfLog(logger)
def displayBoards(boardList):
    for n, board in enumerate(boardList):
        print(f"\n{n + 1}.")
        print(board)


if __name__ == "__main__":
    from HW15_logging import logger
    import argparse

    argParser = argparse.ArgumentParser(description="Peaceful queen combinations")
    argParser.add_argument('s', metavar="size", type=int, nargs=1, help="Size of the chess board")
    argParser.add_argument('n', metavar="combs", type=int, nargs='*', action='append',
                           help="Number of queen combinations to find, all if omitted")
    argParser.add_argument('-d', action='store_true',
                           help="Display the found combinations, the number of combinations displays if not set")
    args = argParser.parse_args()

    solNum = args.n[0][0] if args.n[0] else 0
    boardList = generatePeaceBoards(args.s[0], solNum)
    
    if args.d:
        displayBoards(boardList)
    else:
        print(f"Combinations found: {len(boardList)}")
