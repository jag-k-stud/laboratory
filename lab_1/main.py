# Var 9
from time_class import Time


def populate_times(target_list):
    target_list.append(Time(12, 6, 3))
    target_list.append(Time(23, 59, 55))
    target_list.append(Time(8, 30, 0))


def input_time(target_list):
    target_list.append(Time(
        int(input("Введите часы: ")),
        int(input("Введите минуты: ")),
        int(input("Введите секунды: ")),
    ))


times = list()
populate_times(times)
input_time(times)
for t in times:
    print("%r: %s" % (t, t))
    print("Кол-во секунд:", t.get_seconds())
    print("Результат прибавления секунд:", t, end=' - ')
    t.add_seconds()
    print(t)
    print()
times.clear()
