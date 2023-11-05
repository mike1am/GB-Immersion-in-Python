import csv
import json
import random
import os
import math
from functools import wraps

MIN_ROWS_NUM = 100
MAX_ROWS_NUM = 1000
MIN_NUM = -100
MAX_NUM = 100
RESULT_FILE = "results.json"


def randintWoNull(minNum, maxNum):
    while True:
        res = random.randint(minNum, maxNum)
        if res:
            return res


def generate_csv_file(file_name, rows):
    if os.path.splitext(file_name)[1] != ".csv":
        file_name += ".csv"
    
    with open(file_name, "w", newline="", encoding="utf-8") as csvFile:
        fields = ('a', 'b', 'c')
        csvWriter = csv.DictWriter(
            csvFile,
            fieldnames=fields,
            quoting=csv.QUOTE_NONNUMERIC
        )
        csvWriter.writeheader()
    
        # if not MIN_ROWS_NUM <= rows <= MAX_ROWS_NUM:
        #     print("Параметр вне доп. диапазона")
        #     return
    
        for _ in range(rows):
            csvWriter.writerow({
                field: random.randint(MIN_NUM, MAX_NUM)
                       if field != 'a'
                       else randintWoNull(MIN_NUM, MAX_NUM)
                for field in fields
            })


def save_to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.path.exists(args[0]) and os.path.isfile(args[0]) and os.path.splitext(args[0])[1] == ".csv":
            resList = []            
            with open(args[0], "r", encoding="utf-8") as csvFile:
                csvReader = csv.DictReader(csvFile)

                for eqSet in csvReader:
                    eqSet.update({'r': func(*map(int, eqSet.values()))})
                    resList.append(eqSet)

            with open(RESULT_FILE, "w", encoding="utf-8") as jsonFile:
                json.dump(resList, jsonFile, indent=2)

    return wrapper


@save_to_json
def find_roots(a, b, c):
    d = b ** 2 - 4 * a * c
    if d < 0:
        return None
    if d == 0:
        # print("Zero!")
        return -b / (2 * a)
    
    return (
        (-b - math.sqrt(d)) / (2 * a),
        (-b + math.sqrt(d)) / (2 * a)
    )


if __name__ == "__main__":
    generate_csv_file("task1.csv", 1500)
    find_roots("task1.csv")
