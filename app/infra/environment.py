import os
from dotenv import load_dotenv

load_dotenv()

class Environment:
    _CURRENT = os.getenv("ENV")

    @classmethod
    def get_current(cls):
        return cls._CURRENT

    @classmethod
    def is_production(cls):
        return cls._CURRENT == "PROD"

    @classmethod
    def is_development(cls):
        return cls._CURRENT == "DEV"
