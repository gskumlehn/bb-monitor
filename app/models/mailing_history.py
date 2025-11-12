from sqlalchemy import Column, String, ARRAY, TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid

from app.enums.directorate_codes import DirectorateCode
from app.custom_utils.date_utils import DateUtils

Base = declarative_base()

class MailingHistory(Base):
    __tablename__ = "mailing_history"
    __table_args__ = {"schema": "bb_monitor"}

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    _date_sent = Column("date_sent", TIMESTAMP, nullable=False)
    alert_id = Column(String(64), nullable=False)
    _primary_directorate = Column("primary_directorate", String(255), nullable=False)
    to_emails = Column(ARRAY(String), nullable=False)
    cc_emails = Column(ARRAY(String), nullable=True)
    sender_email = Column(String(255), nullable=False)

    SP_TZ = ZoneInfo(DateUtils.BRAZIL_TZ)
    UTC_TZ = ZoneInfo(DateUtils.UTC_TZ)

    @hybrid_property
    def date_sent(self) -> datetime:
        if self._date_sent is None:
            return None
        return self._date_sent.astimezone(self.SP_TZ)

    @date_sent.setter
    def date_sent(self, value: datetime):
        if value is None:
            self._date_sent = None
            return
        if not isinstance(value, datetime):
            raise TypeError("date_sent must be a datetime instance")
        self._date_sent = value

    @date_sent.expression
    def date_sent(cls):
        return cls._date_sent

    @hybrid_property
    def primary_directorate(self) -> DirectorateCode:
        return DirectorateCode.from_name(self._primary_directorate)

    @primary_directorate.setter
    def primary_directorate(self, directorate: DirectorateCode):
        self._primary_directorate = directorate.name

    @primary_directorate.expression
    def primary_directorate(cls):
        return cls._primary_directorate
