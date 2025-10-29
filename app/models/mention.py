from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, ForeignKey, Text

Base = declarative_base()

class Mention(Base):
    __tablename__ = "mention"
    __table_args__ = {"schema": "bb_monitor"}

    alert_id = Column(String(64), nullable=False)
    url = Column(Text, primary_key=True, nullable=False)