from enum import Enum
from app.constants.error_messages import ErrorMessages

class EnumInterface(Enum):

    @classmethod
    def from_name(cls, name: str):
        try:
            return cls[name]
        except KeyError:
            raise ValueError(ErrorMessages.enum[f"{cls.__name__}.invalid"])

    @classmethod
    def values_csv_to_type_list(cls, csv: str):
        if not csv:
            return []
        return [cls(value.strip()) for value in csv.split(",") if value.strip()]