from logging import debug
from classes import Subject, Departament


# %%
# =============================================================================
def load():
    debug("Start global loading...")
    Subject.load()
    Departament.load()
    debug("Global loading done!")


def save():
    debug("Start global saving...")
    Subject.save()
    Departament.save()
    debug("Global saving done!")


# %%
# =============================================================================
# Тестирование
def test():
    # ========
    print("Проверка на создание объектов:")
    s1 = Subject("Название дисциплины", 1, 1, "форма контроля")
    d1 = Departament("Название Кафедры", 1, s1)
    print(s1, d1)

    print("Вывод через атрибут:", s1.name, sep='\t')
    print("Вывод через ключ:", s1['name'], sep='\t')
    s1.name += " 2"
    print("Вывод изменённого имени:", s1.name, sep='\t')
    print("-========-")

    # ========
    print("Проверка на запись данных в CSV:")
    save()
    for f in ('subject.csv', 'departament.csv'):
        print("===", f, "===")
        with open(f, 'r', newline='\n', encoding='utf-8') as data:
            print(*data.readlines(), sep='')
        print("=========\n")
    print("-========-")

    # ========
    print("Проверка на удаление дисциплины:")
    print(Subject[1])
    del Subject[1]
    print("Удалено")
    print(Subject[1] is None)
    print("-========-")

    # ========
    try:
        print("Проверка на отсутствие данных в переменной:")
        print(s1)
    except ValueError:
        print("Проверка прошла успешно!")

    # ========
    print("-========-")
    print("Проверка на отсутствие данных дисциплины на кафедре:")
    print(d1["subject"])
    print("-========-")

    print("Проверка на каскадное удаление объектов:")

    s2 = Subject("Название новой дисциплины", 1, 1, "форма контроля")
    d2 = Departament("Название Кафедры 2", 1, s2)
    print(s2, d2)
    print("-========-")
    print("Удаление кафедры")
    del Departament[2]
    print("Проверка на отсутсвие дисциплины и направления:")
    print(Departament[2] is None)
    print(s2.is_exist() is False)
    print("-========-")

    # ========
    print("Проверка на чтение данных из CSV:")
    load()
    for e in (Subject, Departament):
        print("===", e.__name__, "===")
        for entity in e._entity_dict.values():
            print("%r:" % entity)
            for k, v in entity.items():
                print("  %s = %r" % (k, v))
        print("=========\n")
    print("-========-")

