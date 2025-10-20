from enum import Enum

class DirectorateCode(Enum):

    FB = "FutureBrand"

    @classmethod
    def from_str(cls, name: str):
        if name is None:
            raise ValueError("Directorate code cannot be None")

        if name not in cls.__members__:
            raise ValueError(f"Unknown DirectorateCode: {name}")

        return cls[name]