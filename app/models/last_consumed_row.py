from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()

class LastConsumedRow(Base):
    __tablename__ = "last_consumed_row"
    __table_args__ = {"schema": "bb_monitor"}

    value = Column(Integer, primary_key=True)