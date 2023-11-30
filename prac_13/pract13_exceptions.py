class UserError(Exception):
    def __str__(self):
        return self.msg if hasattr(self, 'msg') else self.args[0]


class UserAccessError(UserError):
    pass


class AccessLevelError(UserError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = "Недостаточно уровня доступа" if not args else args[0]


class AttrValueError(UserError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = "Неправильный ввод" if not args else args[0]
    

class UserInputError(UserError):
    pass
