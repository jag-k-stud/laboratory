import math
from c_functions import Functions


class Sin(Functions):
    @property
    def result(self):
        return math.sin(self.digit)

    @property
    def derivative(self):
        return math.cos(self.digit)
