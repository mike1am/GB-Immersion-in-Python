import random
import os

__all__ = [
    "pract7_func1",
    "pract7_func2",
    "pract7_func3",
    "pract7_func4",
    "pract7_func5",
    "pract7_func7",
]

test_folder = "test_folder"

def pract7_func1(fileName, linesNum):
    """
    ```
    Заполняет файл (добавляет в конец) случайными парами чисел.
    Первое число int, второе - float разделены вертикальной чертой.
    Минимальное число - -1000, максимальное - +1000.
    Количество строк и имя файла передаются как аргументы функции
    ```
    """
    with open(fileName, "a", encoding="utf-8") as outFile:
        for _ in range(linesNum):
            outFile.write(f"{random.randint(-1000, 1000)}|{random.uniform(-1000, 1000)}\n")


def genNames(namesNum, lenRange: tuple[int, int], vowelRange: tuple[int, int] = (2, 100)):
    VOWELS = "aeijou"
    CONSONANTS = "bcdfghklmnpqrstvwxyz"

    resSet = set()
    while len(resSet) < namesNum:
        nameLen = random.randint(lenRange[0], lenRange[1])
        vowelNum = random.randint(vowelRange[0], max(min(nameLen - 1, vowelRange[1]), vowelRange[0]))
        if vowelNum < nameLen:
            charList = random.sample(CONSONANTS, min(len(CONSONANTS), nameLen - vowelNum)) + random.sample(VOWELS, min(len(VOWELS),vowelNum))
        else:
            charList = random.sample(VOWELS + CONSONANTS, nameLen)
        random.shuffle(charList)

        resSet.add(str(charList[0]).upper() + "".join(charList[1:]))

    return tuple(resSet)


def pract7_func2(filename, count):
    """
    ```
    Генерирует псевдоимена.
    Имя начинается с заглавной буквы, состоит из 4-7 букв, среди которых обязательно должны быть гласные.
    Полученные имена сохраняются в файл.
    ```
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for name in genNames(count, (4, 7), (2, 5)):
            f.write(f'{name}\n')


def readLine(file):
    inStr = file.readline()
    if inStr == "":
        file.seek(0)
        inStr = file.readline()
    return inStr[:-1]


def pract7_func3(fName1, fName2, fName3):
    """
    ```
    Открывает на чтение созданные pract7_func1 и pract7_func2 файлы с числами и именами.
    Перемножает пары чисел. В новый файл сохраняет имя и произведение:
    ✔ если результат умножения отрицательный, сохраняет имя, записанное строчными буквами, и произведение по модулю
    ✔ если результат умножения положительный, сохраняет имя прописными буквами и произведение, округлённое до целого
    
    В результирующем файле столько же строк, сколько в более длинном файле.
    При достижении конца более короткого файла возвращается в его начало.
    ```
    """
    with (
        open(fName1, "r", encoding="utf-8") as f1,
        open(fName2, "r", encoding="utf-8") as f2,
        open(fName3, "w", encoding="utf-8") as f3
    ):
        numsLen = len(f1.readlines())
        namesLen = len(f2.readlines())
        f1.seek(0)
        f2.seek(0)
        for _ in range(max(numsLen, namesLen)):
            n1, n2 = readLine(f1).split("|")
            name = readLine(f2)
            m = int(n1) * float(n2)
            if m < 0:
                f3.write(f"{name.lower()} {str(abs(m))}\n")
            elif m > 0:
                f3.write(f"{name.upper()} {str(round(m))}\n")


def genData(minLen, maxLen):
    len_ = random.randint(minLen, maxLen)
    return random.randbytes(len_)


def pract7_func4(ext, minNameLen=6, maxNameLen=30, minFileLen=256, maxFileLen=4096, filesNum=42):
    """
    ```
    Cоздаёт файлы с указанным расширением.
    Имя файла и его размер в рамках переданного диапазона.
    ```
    Args:
        ext: расширение
        minNameLen: минимальная длина случайно сгенерированного имени, по умолчанию 6
        maxNameLen: максимальная длина случайно сгенерированного имени, по умолчанию 30
        minFileLen: минимальное число случайных байт, записанных в файл, по умолчанию 256
        maxFileLen: максимальное число случайных байт, записанных в файл, по умолчанию 4096
        filesNum: количество файлов, по умолчанию 42
    """
    if not os.path.exists(test_folder):
        os.mkdir(test_folder)
    
    for name in genNames(filesNum, (minNameLen, maxNameLen)):
        fullName = os.path.join(test_folder, f"{name}.{ext}")
        addNum = 0
        while os.path.exists(fullName):
            addNum += 1
            addSuff = f"_{addNum:03}"
            fullName = os.path.join(test_folder, f"{name + addSuff}.{ext}")
        
        with open(fullName, "wb") as outFile:
            outFile.write(genData(minFileLen, maxFileLen))


def pract7_func5(extDict: dict[str: int]):
    """
    ```
    Генерирует файлы с разными расширениями.
    Расширения и количество файлов функция принимает в качестве параметров.
    Количество переданных расширений может быть любым.
    Количество файлов для каждого расширения различно.
    ```
    """
    NAME_LEN = 2
    MIN_SIZE = 1024
    MAX_SIZE = 4096

    for ext, num in extDict.items():
        pract7_func4(ext, NAME_LEN, NAME_LEN, MIN_SIZE, MAX_SIZE, num)


FILE_TYPES = {
    'text': ["txt", "doc", "pdf"],
    'images': ["jpg", "png", "tiff", "pds"],
    'audio': ["mp3", "flac", "ogg"]
}


def pract7_func7(folder):
    """
    ```
    Функция для сортировки файлов по директориям: видео, изображения, текст и т.п.
    Каждая группа включает файлы с несколькими расширениями.
    В исходной папке остаются только те файлы, которые не подошли для сортировки.
    ```
    """
    if not os.path.exists(folder):
        print(f"Директория {folder} не найдена.")
        return

    fileList = os.listdir(folder)
    for fileType in FILE_TYPES:
        if fileType not in fileList:
            os.mkdir(os.path.join(folder, fileType))

    for file in fileList:
        filePath = os.path.join(folder, file)
        for fileType, extList in FILE_TYPES.items():
            if os.path.isfile(filePath) and os.path.splitext(file)[1][1:] in extList:
                os.replace(filePath, os.path.join(folder, fileType, file))


def setTestFolder(folderName):
    global test_folder
    test_folder = folderName


def clearTestFolder():
    for file in os.listdir(test_folder):
        _, ext = os.path.splitext(file)
        if ext[1:].startswith(("bin", "tmp")):
            os.remove(os.path.join(test_folder, file))


if __name__ == "__main__":
    # if not os.path.exists(test_folder):
    #     os.mkdir(test_folder)
    
    # pract7_func1(os.path.join(FOLDER_TO_CREATE, "task1.txt"), 10)
    # pract7_func2(os.path.join(FOLDER_TO_CREATE, "task2.txt"), 10)
    # pract7_func3(os.path.join(FOLDER_TO_CREATE, "task1.txt"), os.path.join(FOLDER_TO_CREATE, "task2.txt"), os.path.join(FOLDER_TO_CREATE, "task3.txt"))
    # pract7_func4("bin", 10, 16, 256, 512, 7)
    # setTestFolder("test2_folder")
    # pract7_func5({
    #     'bin': 20,
    #     'bin1': 20,
    #     'bin2': 3
    # })
    # clearTestFolder()
    # os.chdir("HW7")
    # pract7_func7("test_folder")
    pass
