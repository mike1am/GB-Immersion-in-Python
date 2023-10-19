__all__ = [
    "printStat"
]

_statDict = {}


def setStat(riddle, attNum):
    _statDict[riddle] = attNum


def printStat():
    print("\n".join((
        f"\nЗагадка:\n{riddle}\nКол. попыток: {attNum}"
        for riddle, attNum in _statDict.items()
    )))
