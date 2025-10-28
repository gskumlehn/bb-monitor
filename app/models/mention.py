from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, ForeignKey, Text

Base = declarative_base()

class Mention(Base):
    __tablename__ = "mention"
    __table_args__ = {"schema": "bb_monitor"}

    id = Column(String(64), primary_key=True)
    alert_id = Column(String(64), ForeignKey("bb_monitor.alert.id"), nullable=False)
    url = Column(Text, nullable=False)