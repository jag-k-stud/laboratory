from math import radians
from c_sin import Sin
from c_cos import Cos
from c_tan import Tan

digits = (
    radians(30),
    radians(45),
    radians(60),
)

functions = (Sin, Cos, Tan)

for f in functions:
    print("%s:" % f.__name__)
    for d in digits:
        func = f(d)
        print("  Значение:", d)
        print("  Результат:", func.result)
        print("  Производная:", func.derivative)
        print()
    print()
