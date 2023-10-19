import random

def guess(riddle, ansList, attLim=3):

    print(f"Отгадайте загадку:\n{riddle}")

    for att in range(1, attLim + 1):
        ans = input(f"Попытка {att} из {attLim}. Введите ответ: ").lower()
        if ans in ansList:
            print(f"\033[33mУра, Вы угадали!\033[0m")
            return att
        
        print("Ответ неверен.")

    print(f"Вам не хватило попыток((. Ответ был: {random.choice(ansList)}")
    return 0
    

if __name__ == "__main__":
    attNum = guess('Зимой и летом одним цветом', ['ель', 'ёлка', 'сосна'])

    if attNum:
        print(f"Вы угадали с {attNum} попытки.")
