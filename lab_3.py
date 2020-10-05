# Var 9
# %%

class Entity:
    _last_id = 0
    _entity_dict = None

    def __init__(self):
        cls = self.__class__
        cls._last_id += 1
        self._id = cls._last_id
        if cls._entity_dict is None:
            cls._entity_dict = {}
        self.__class__._entity_dict[self._id] = self

    def __del__(self):
        print(self._id, self.__class__._entity_dict)
        del self.__class__._entity_dict[self._id]

    def __repr__(self):
        return "<class '%s.%s' id=%d>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self._id,
        )


# Дисциплина
class Subject(Entity):
    def __init__(self, name: str, lectures_count: int, practices_count: int, control_form: str):
        super().__init__()
        pass


# Кафедра
class Departament(Entity):
    def __init__(self, name: str, teacher_count: int, subject: Subject):
        super().__init__()
        self.name = name
        self.teacher_count = teacher_count
        self.subject = subject


# %%
s = Subject("", 1, 1, "")
d = Departament("", 1, s)
print(s, d)
