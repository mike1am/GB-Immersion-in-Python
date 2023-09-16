"""
Напишите программу банкомат.
✔ Начальная сумма равна нулю
✔ Допустимые действия: пополнить, снять, выйти
✔ Сумма пополнения и снятия кратны 50 у.е.
✔ Процент за снятие — 1.5% от суммы снятия, но не менее 30 и не более 600 у.е.
✔ После каждой третей операции пополнения или снятия начисляются проценты - 3%
✔ Нельзя снять больше, чем на счёте
✔ При превышении суммы в 5 млн, вычитать налог на богатство 10% перед каждой
операцией, даже ошибочной
✔ Любое действие выводит сумму денег
"""

from ui import userInput

AMOUNT_MULT = 50
PROCENT_PERIOD = 3
PROCENTAGE = 3
WEALTH_LIMIT = 5_000_000
WEALTH_TAX = 10

balance = 0


MENU_ITEMS = {
    0: "Выйти",
    1: "Пополнить баланс",
    2: "Снять наличные",
}


def menu(menuItems):
    print()    
    for actNum, actDesc in menuItems.items(): 
        print(f"{actNum}. {actDesc}")

    return int(userInput("Выберите требуемое действие: ", lambda uInp: 0 <= int(uInp) <= len(menuItems)))


def topUp():
    global balance

    withholdTax()
    while True:
        amount = int(userInput(f"Введите сумму пополнения, кратную {AMOUNT_MULT}: ", lambda uInp: int(uInp) >= 0))
        if amount % AMOUNT_MULT == 0:
            break
        else: 
            print("Ошибочная операция!")
            withholdTax()

    balance += amount


def withdraw():
    global balance

    withholdTax()
    while True:
        amount = int(userInput(
            f"Ваш баланс: {balance:_.2f}  Введите сумму снятия, кратную {AMOUNT_MULT}: ",
            lambda uInp: int(uInp) >= 0
        ))
        if amount % AMOUNT_MULT == 0 and amount <= balance:
            break
        else: 
            print("Ошибочная операция!")
            withholdTax()
    
    balance -= amount


def chargeProcents():
    global balance
    procents = balance * PROCENTAGE / 100
    balance += procents
    print(f"Были начислены проценты: {procents:_.2f}")


def withholdTax():
    global balance
    if balance >= WEALTH_LIMIT:
        tax = balance * WEALTH_TAX / 100
        balance -= tax
        print(f"Был удержан налог на богатство: {tax:_.2f}")
    

def showBalance():
    print(f"\nВаш баланс: {balance:_.2f}")
    

actCnt = 0
showBalance()
while True:
    act = menu(MENU_ITEMS)

    match act:
        case 0:
            print("Всего доброго!")
            break

        case 1:
            actCnt += 1
            topUp()
            if actCnt % PROCENT_PERIOD == 0: chargeProcents()
            showBalance()

        case 2:
            actCnt += 1
            withdraw()
            if actCnt % PROCENT_PERIOD == 0: chargeProcents()
            showBalance()
