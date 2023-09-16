def userInput(prompt :str, chkFunc=lambda _: True):
    while True:
        try:
            uInput = input(prompt)
            if not chkFunc(uInput): raise ValueError
        except ValueError:
            print("Некорректный ввод")
        else:
            return uInput
