from itertools import combinations

def printBoard(queens: list[tuple[int, int]]) -> None:
    """
    Выводит решение в терминал.

    Args:
        queens: Список картежей с координатами ферзей на доске.
    """
    size = len(queens)
    board = [["·"] * size for _ in range(size)]
    
    for i, j in queens:
        board[i][j] = chr(0x2655)

    print(" ", "".join([f"{n:>3}" for n in range(size)]))
    for n, row in enumerate(board):
        print(f"{n:>2} ", "  ".join(row))


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