

class Time:
    def __init__(self, hours: int, minutes: int, seconds: int):
        """Класс "Время"

        Args:
            hours (int): часы
            minutes (int): минуты
            seconds (int): секунды
        """

        self.h = hours
        self.m = minutes
        self.s = seconds

        self._check_time()

    def _check_time(self):
        self.m += self.s // 60
        self.s %= 60

        self.h += self.m // 60
        self.m %= 60

        self.h %= 24

    def get_seconds(self):
        return self.s + self.m * 60 + self.h * 3600

    def add_seconds(self):
        self.s += 5
        self._check_time()

        return self

    def __del__(self):
        print(repr(self), "was deleted")

    def __repr__(self):
        return "%s(h=%d, m=%d, s=%d)" % (
            self.__class__.__name__,
            self.h,
            self.m,
            self.s,
        )

    def __str__(self):
        return "%.2d:%.2d:%.2d" % (
            self.h,
            self.m,
            self.s,
        )
