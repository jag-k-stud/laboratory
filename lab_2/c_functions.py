class Functions:
    def __init__(self, number: int or float):
        self.digit = float(number)

    @property
    def result(self):
        """Результат функции

        Returns:
            float: Результат в виде числа
        """
        return self.digit

    @property
    def derivative(self):
        """Производная от функции

        Returns:
            float: значение производной
        """
        return 0

    def __repr__(self):
        return "%s(%d)" % (
            self.__class__.__name__.lower(),
            self.digit
        )

    def __str__(self):
        return str(self.result())
