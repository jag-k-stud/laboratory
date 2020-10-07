import csv
from logging import debug
ID_KEY = "id"


# %%
# =============================================================================
class Meta(type):
    """Мета-класс
    Предназначен для получения экземпляра класса, обращаясь по ID.
    Если в поле ID передаётся сам экземпляр, то возвращяется этот экземпляр.
    Если экземпляра с таким ID нет, то возвращается `None`

    Например:
    >>> Subject[1]
    >>> Subject[Subject[1]] == Subject[1]
    """
    def __getitem__(cls, id):
        if isinstance(id, int):
            return cls._entity_dict.get(id, None)
        if isinstance(id, type(id)):
            return id
        return None

    def __delitem__(cls, item):
        """Удаление экземпляра класса по его ID

        >>> Subject("Some name", 1, 1, "")
        ... Subject[1]
        >>> del Subject[1]
        >>> Subject[1]
        ... None
        """
        return cls[item].__del__()


# =============================================================================
class Entity(dict, metaclass=Meta):
    """Класс Entity
    Предназначен для более простого создания новых классов
    для учёта в базе данных
    """
    _last_id = 0  # Последний ID в "таблице" БД
    _entity_dict = None  # type: dict
    # Используется для хранения значений в БД "таблицы"

    _watchers = []  # Список экземпляров для рекурсивного удаления
    __slots__ = (ID_KEY,)  # Список возможных аргументов и "ключей"

    def __init__(self):
        dict.__init__(self)
        self._setting_id()

    def _setting_id(self, _id: int = None):
        cls = self.__class__
        if _id is None:
            cls._last_id += 1
            _id = cls._last_id
        else:
            if self.get(ID_KEY):
                self._entity_dict.pop(self.get(ID_KEY))
            ed = cls._entity_dict
            if ed:
                cls._last_id = max(ed.keys())
            else:
                cls._entity_dict = {}
                cls._last_id = _id

        if cls._entity_dict is None:
            cls._entity_dict = {}

        dict.__setitem__(self, ID_KEY, _id)
        cls._entity_dict[_id] = self

    def __del__(self):
        """Удаление экземпляра класса

        >>> subject = Subject("Some name", 1, 1, "")
        ... Subject[1]
        >>> del subject
        >>> Subject[1]
        ... None
        """
        w = self._watchers.copy()
        self._watchers.clear()
        for e in w:
            e.__del__()

        ed = self.__class__._entity_dict
        debug("Delete: %s, %s", self.id, ed)

        if self.id in ed:
            del ed[self.id]

    # Для пользовательского вызова `entity.delete()`
    delete = __del__

    def __repr__(self) -> str:
        """Технический вывод
        >>> repr(Subject[1]) == "Subject[1]"

        Returns:
            str: Результат для "технического вывода"
        """
        self.is_exist(True)
        return "%s[%r]" % (
            self.__class__.__name__,
            self.id,
        )

    def __setitem__(self, item: str, value):
        """Сеттер

        >>> subject = Subject("Some name", 1, 1, "")
        >>> subject['name'] = "Some new name"
        >>> subject['name']
        ... "Some new name"

        Args:
            item (str): Ключ
            value (Any[str, int]): Значение
        """
        if item in self.__slots__ and item != ID_KEY:
            debug("Setting value: %r[%r] = %r", self, item, value)
            return dict.__setitem__(self, item, value)

        if item in dir(Entity):
            return super().__setattr__(item, value)

    # Связывание утсановки значений через . и []
    __setattr__ = __setitem__

    def __getitem__(self, item: str):
        """Геттер

        >>> subject = Subject("Some name", 1, 1, "")
        >>> subject['name'] == "Some name"
        >>> subject.name == "Some name"

        Args:
            item (str): Ключ

        Returns:
            Any: Значение по ключу
        """

        if item in dir(Entity) and item != "id":
            return super().__getattribute__(item)

        if item in super().__getattribute__("__slots__"):
            if item not in ("is_exist", ID_KEY, "__class__"):
                self.is_exist(True)
                debug("Getting value: %r.%s", self, item)

            res = dict.__getitem__(self, item)

            if isinstance(res, Entity) and not res.is_exist():
                self[item] = None
                return None
            return res

    # Связывание получения значений через . и []
    __getattribute__ = __getitem__

    def recursive_delete(self, entity: "Entity"):
        """Рекурсивное удаление
        Позволяет удалить объект `entity`, когда удаляется объект

        >>> subject = Subject("name", 1, 1, "form")
        ... Subject[1]
        >>> departament = Departament("name", 1, subject)
        ... Departament[1]
        >>> del departament
        >>> Subject[1]
        ... None

        Args:
            entity (Entity): Экземпляр класса, которого стоит удалить вместе с
            данным экземпляром

        Returns:
            Entity: Возвращяает `self`
        """
        entity._watchers.append(self)
        return self

    def is_exist(self, raise_error=False) -> bool:
        """Проверка на наличие объекта в БД

        >>> s = Subject("name", 1, 1, "form")
        ... Subject[1]
        >>> s.is_exist() == True
        >>> del Subject[1]
        >>> s.is_exist() == False

        Args:
            raise_error (bool, optional): Выбрасывать ошибку?
            Defaults to False.

        Raises:
            ValueError: Если объект не существует

        Returns:
            bool: Существует или нет
        """
        if self.id not in self.__class__._entity_dict:
            if raise_error:
                raise ValueError("object '%s[%r]' was been deleted" % (
                    self.__class__.__name__,
                    self.id
                ))
            return False
        return True

    @classmethod
    def save(cls, filename: str = None):
        filename = filename or cls.__name__.lower() + '.csv'
        debug("Start saving to %r file...", filename)

        with open(filename, 'w', newline='\n', encoding='utf-8') \
                as database:
            csv_writer = csv.DictWriter(
                database, delimiter=';', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, fieldnames=cls.__slots__)
            csv_writer.writeheader()
            for e in cls._entity_dict.values():
                line = dict(map(
                    lambda i: (i[0], i[1].id) if isinstance(
                        i[1], Entity
                    ) else i,
                    e.items()
                ))
                csv_writer.writerow(line)

        debug("Data saved to %r file!", filename)

    @classmethod
    def load(cls, filename: str = None):
        filename = filename or cls.__name__.lower() + '.csv'
        debug("Start loading from %r file...", filename)

        with open(filename, 'r', newline='\n', encoding='utf-8') \
                as database:
            reader = csv.DictReader(
                database, delimiter=';', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, fieldnames=cls.__slots__)
            next(reader)
            for data in reader:
                _id = int(data.pop(ID_KEY))
                for k, v in data.items():
                    if v.isdigit():
                        data[k] = int(v)
                e = cls(**data)
                e._setting_id(_id)
                print(e)

        debug("Data loaded from %r file!", filename)


# =============================================================================
# Дисциплина
class Subject(Entity):
    __slots__ = (ID_KEY, "name", "lectures_count", "practices_count",
                 "control_form")

    def __init__(self, name: str, lectures_count: int, practices_count: int,
                 control_form: str):
        super().__init__()
        self["name"] = name
        self["lectures_count"] = lectures_count
        self["practices_count"] = practices_count
        self["control_form"] = control_form


# =============================================================================
# Кафедра
class Departament(Entity):
    __slots__ = (ID_KEY, "name", "teacher_count", "subject")

    def __init__(self, name: str, teacher_count: int, subject: Subject or int):
        super().__init__()
        self.name = name
        self.teacher_count = teacher_count

        self.subject = Subject[subject].recursive_delete(self)
