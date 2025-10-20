from enum import Enum
from app.constants.error_messages import ErrorMessages

class DirectorateCode(Enum):

    FB = "FutureBrand"

    @classmethod
    def from_str(cls, name: str):
        if name is None or name not in cls.__members__:
            raise ValueError(ErrorMessages.enum["DirectorateCode.invalid"])

        return cls[name]