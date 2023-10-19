# if __name__ == "__main__":
#     import task4
#     import task6
# else:
#     from . import task4
#     from . import task6
from task4 import guess
from task6 import setStat, printStat


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
    
    allRiddles(dict(tuple(RIDDLES.items())[:1]))
    printStat()
