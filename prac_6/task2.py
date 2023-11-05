from random import randint

def guessNum(lowerLimit=0, upperLimit=100, attLimit=10):

    num = randint(lowerLimit, upperLimit) 
    print(f"Угадайте число от {lowerLimit} до {upperLimit}")

    for att in range(1, attLimit + 1):
        attNum = int(input(f"Попытка {att} из {attLimit}. Введите число: "))
        if attNum == num:
            print(f"\033[33m<< {num} >>  Ура, Вы угадали!\033[0m")
            return True
        
        if attNum > num:
            print(f"\033[31mМеньше, чем {attNum}\033[0m")
        else:
            print(f"\033[31mБольше, чем {attNum}\033[0m")

    print(f"Вам не хватило попыток((  Это было число {num}")
    return False
    

if __name__ == "__main__":
    guessNum()