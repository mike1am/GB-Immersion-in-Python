"""
✔ Три друга взяли вещи в поход. Сформируйте
словарь, где ключ — имя друга, а значение —
кортеж вещей. Ответьте на вопросы:
✔ Какие вещи взяли все три друга
✔ Какие вещи уникальны, есть только у одного друга
✔ Какие вещи есть у всех друзей кроме одного
и имя того, у кого данная вещь отсутствует
✔ Для решения используйте операции
с множествами. Код должен расширяться
на любое большее количество друзей.
"""

hike = {
    'Друг1': ('Рюкзак', 'Палатка', 'Спальник', 'Фонарик'),
    'Друг2': ('Рюкзак', 'Палатка', 'Котелок', 'Кружка', 'Спички', 'Фонарик'),
    'Друг3': ('Рюкзак', 'Палатка', 'Спички', 'Складной стул'),
    'Друг4': ('Рюкзак', 'Ноутбук', 'Складной стул', 'Спички', 'Фонарик'),
}


from functools import reduce

def commItems(itemsDict) -> tuple:
    if not len(itemsDict): return ()

    return tuple(reduce(
        lambda res, seq: set(res) & set(seq),
        itemsDict.values()
    ))


def uniqItems(itemsDict :dict) -> tuple:
    """
    _summary_

    Args:
        itemsDict: _description_

    Returns:
        _description_
    """
    if not len(itemsDict): return ()

    uniqSet = set()

    for name, nameItems in itemsDict.items():
        uniqSet |= reduce(
            lambda res, seq: res - set(seq),
            (itemsDict[key] for key in itemsDict.keys() if key != name),
            set(nameItems)
        )

    return tuple(uniqSet)


def missedItems(itemsDict) -> dict:
    if len(itemsDict) < 2: return {}

    resDict = {}

    for name, nameItems in itemsDict.items():
        otherSeq = tuple(
            itemsDict[key]
            for key in itemsDict.keys()
            if key != name
        )

        missedSet = reduce(
            lambda res, seq: set(res) & (set(seq) - set(nameItems)),
            otherSeq,
            otherSeq[0] # на случай, если в списке itemsDict только 2 элемента
        )
        if missedSet:
            resDict[name] = tuple(missedSet)

    return resDict


print(f"Вещи у всех друзей: {commItems(hike)}")

print(f"Уникальные вещи: {uniqItems(hike)}")

print(f"Пропущенные вещи: {missedItems(hike)}")
