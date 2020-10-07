import math
from c_functions import Functions


class Cos(Functions):
    @property
    def result(self):
        return math.cos(self.digit)

    @property
    def derivative(self):
        return -math.sin(self.digit)
