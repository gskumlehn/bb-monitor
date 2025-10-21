from app.interfaces.enum_interface import EnumInterface

class CriticalityLevel(EnumInterface):
    LEVEL_1 = ("Nível 1", 1)
    LEVEL_2 = ("Nível 2", 2)
    LEVEL_3 = ("Nível 3", 3)
    LEVEL_4 = ("Nível 4", 4)
    INCIDENT = ("Incidente", 5)

    def __new__(cls, value, number):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.number = number
        return obj
