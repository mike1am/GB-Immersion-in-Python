if len(__name__.split(".")) > 1:
    from .task4 import *
    from .task6 import setStat

__all__ = [
    "allRiddles",
    "RIDDLES",
]

RIDDLES = {
    'Висит груша - нельзя скушать': ["лампочка", "лампа"],
    'Зимой и летом - одним цветом': ['ёлка', 'елка', 'ель'],
    'Делать нужно по утрам,\nОна бодрость дарит нам': ['зарядка', "пробежка"],
    'Он красив и ярко-красен,\nНо он жгуч, горяч, опасен': ['огонь'],
}


def allRiddles(riddles=RIDDLES):
    for riddle, ansList in riddles.items():
        setStat(riddle, guess(riddle, ansList))


if __name__ == "__main__":
    from task4 import *
    from task6 import setStat, printStat
    
    allRiddles(dict(tuple(RIDDLES.items())[:1]))
    printStat()
