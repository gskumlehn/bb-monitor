from enum import Enum
from app.constants.error_messages import ErrorMessages

class EnumInterface(Enum):

    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name]
        except KeyError:
            raise ValueError(ErrorMessages.enum[f"{cls.__name__}.invalid"])

    def __new__(cls, value, *args, **kwargs):
        try:
            return super().__new__(cls, value)
        except ValueError:
            raise ValueError(ErrorMessages.enum[f"{cls.__name__}.invalid"])
