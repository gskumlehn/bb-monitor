from enum import Enum
from app.constants.error_messages import ErrorMessages

class EnumInterface(Enum):

    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name]
        except KeyError:
            raise ValueError(ErrorMessages.enum[f"{cls.__name__}.invalid"])
