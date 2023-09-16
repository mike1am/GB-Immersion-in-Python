"""
Напишите программу, которая принимает две строки вида “a/b” - дробь с числителем и знаменателем.
Программа должна возвращать сумму и произведение* дробей.
Для проверки своего кода используйте модуль fractions.
"""

import re
from ui import userInput
import fractions


# сокращение дроби
def reduceFract(fr :list) -> list:
    val = max(abs(fr[0]), abs(fr[1]))
    div = min(abs(fr[0]), abs(fr[1]))

    while val % div:
        val, div = div, val % div

    return [fr[0] // div, fr[1] // div]


def sumFract(fr1 :list, fr2 :list) -> list:
    mults = reduceFract([fr1[1], fr2[1]]) # множители для приведения к единому знаменателю

    return reduceFract([
        fr1[0] * mults[1] + fr2[0] * mults[0],
        fr1[1] * mults[1]
    ])


def subFract(fr1 :list, fr2 :list) -> list:
    return sumFract(fr1, [-fr2[0], fr2[1]])


def multFract(fr1 :list, fr2 :list) -> list:
    return reduceFract([
        fr1[0] * fr2[0],
        fr1[1] * fr2[1]
    ])


def divFract(fr1 :list, fr2 :list) -> list:
    return multFract(fr1, [fr2[1], fr2[0]])


def parseExp(inStr) -> list:
    fracts = []

    fractList = list(re.finditer(r"-?\d+/-?\d+", inStr))
    for fr in fractList:
        fracts.append(list(map(int, fr.group().split("/"))))
    
    oper = inStr[fractList[0].span()[1]:fractList[1].span()[0]].strip()
    if not oper:
        oper = "+" # если ввод без пробелов, - будет расценен, как знак операнда

    return [*fracts, oper]


while True:
    inStr = userInput(
        "\nВведите выражение в виде:\nЧислитель/Знаменатель [+/-/*//] Числитель/Знаменатель," +\
        "\n0 в знаменателях, а также в числителе 2-го операнда для операции деления не допускаются." +\
        "\nПустой ввод для выхода: ",
        lambda expStr: not expStr or re.fullmatch(
            r"-?\d+/-?0*[1-9]-?\d*\s*([+\-*]\s*-?\d+/-?0*[1-9]\d*|/\s*-?\0*[1-9]\d*/-?0*[1-9]\d*)",
            expStr
        )
    )
    if not inStr:
        break
    
    exp = parseExp(inStr)

    checkFr1 = fractions.Fraction(numerator=exp[0][0], denominator=exp[0][1])
    checkFr2 = fractions.Fraction(numerator=exp[1][0], denominator=exp[1][1])

    match exp[2]:
        case "+":
            res = sumFract(exp[0], exp[1])
            checkRes = checkFr1 + checkFr2
        case "-":
            res = subFract(exp[0], exp[1])
            checkRes = checkFr1 - checkFr2
        case "*":
            res = multFract(exp[0], exp[1])
            checkRes = checkFr1 * checkFr2
        case "/":
            res = divFract(exp[0], exp[1])
            checkRes = checkFr1 / checkFr2
    
    print(f"\033[33mРезультат: {res[0]}/{res[1]}\033[0m")
    print(f"\033[35mПроверочный результат: {checkRes}\033[0m")
