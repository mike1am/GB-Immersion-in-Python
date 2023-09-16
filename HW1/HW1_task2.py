"""
Напишите код, который запрашивает число и сообщает является ли оно простым или составным.
Используйте правило для проверки: “Число является простым, если делится нацело только на единицу и на себя”.
Сделайте ограничение на ввод отрицательных чисел и чисел больше 100 тысяч.
"""

UPPER_LIMIT = 100_000

num = int(input("Введите целое число от 1 до 100 000: "))
if num < 1 or num > UPPER_LIMIT:
    print("Введено неверное число")
    quit()

maxDiv = int(num**0.5)
div = 1 # если num == 1
for div in range(2, maxDiv + 1):
    if num % div == 0: break
else:
    div += 1

print("Это простое число" if div > maxDiv
    else f"Это составное число, найденный делитель: {div}")