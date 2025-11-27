from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text

Base = declarative_base()

class Mention(Base):
    __tablename__ = "mention"
    __table_args__ = {"schema": "bb_monitor"}

    url = Column(Text, primary_key=True, nullable=False)