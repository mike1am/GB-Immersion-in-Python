"""
Вспомогательный модуль для инициализации файла паролей при существующем json файле с пользователями
"""
from HW15_task2 import Users, FILE_NAME

if __name__ == "__main__":
    with Users(FILE_NAME) as users:
        users.initPswd()
