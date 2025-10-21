from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property
from app.enums.directorate_codes import DirectorateCode

Base = declarative_base()

class Mailing(Base):
    __tablename__ = "mailing"
    __table_args__ = {"schema": "bb_monitor"}

    email = Column(String, primary_key=True)
    _directorate_code = Column("directorate_code", String, primary_key=True)

    @hybrid_property
    def directorate_code(self) -> DirectorateCode:
        return DirectorateCode.from_name(self._directorate_code)

    @directorate_code.setter
    def directorate_code(self, code: DirectorateCode):
        self._directorate_code = code.name

    @directorate_code.expression
    def directorate_code(cls):
        return cls._directorate_code

