import math
from c_functions import Functions


class Tan(Functions):
    @property
    def result(self):
        return math.tan(self.digit)

    @property
    def derivative(self):
        return math.cos(self.digit)**-2
