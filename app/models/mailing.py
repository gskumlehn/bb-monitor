from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Enum as SAEnum
from app.enums.directorate_codes import DirectorateCode

Base = declarative_base()

class Mailing(Base):
    __tablename__ = "mailing"
    __table_args__ = {"schema": "bb_monitor"}

    email = Column(String, primary_key=True)
    directorate_code = Column(
        SAEnum(DirectorateCode, values_callable=lambda enum: [e.name for e in enum], native_enum=False),
        primary_key=True
    )
