from enum import Enum

class NivelCriticidade(Enum):
    NIVEL_1 = ("Nível 1", 1)
    NIVEL_2 = ("Nível 2", 2)
    NIVEL_3 = ("Nível 3", 3)
    NIVEL_4 = ("Nível 4", 4)
    INCIDENTE = ("Incidente", 5)

    def __init__(self, label, value):
        self.label = label
        self.value = value
