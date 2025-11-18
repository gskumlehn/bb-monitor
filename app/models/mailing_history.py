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
    to_emails = Column(ARRAY(String), nullable=False)
    cc_emails = Column(ARRAY(String), nullable=True)
    bcc_emails = Column(ARRAY(String), nullable=True)
    sender_email = Column(String(255), nullable=False)
    _to_directorates = Column("to_directorates", ARRAY(String), nullable=True)
    _cc_directorates = Column("cc_directorates", ARRAY(String), nullable=True)
    _bcc_directorates = Column("bcc_directorates", ARRAY(String), nullable=True)

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
    def to_directorates(self) -> list[DirectorateCode]:
        return [DirectorateCode.from_name(d) for d in self._to_directorates]

    @to_directorates.setter
    def to_directorates(self, directorates: list[DirectorateCode]):
        self._to_directorates = [d.name for d in directorates]

    @to_directorates.expression
    def to_directorates(cls):
        return cls._to_directorates

    @hybrid_property
    def cc_directorates(self) -> list[DirectorateCode]:
        if not self._cc_directorates:
            return []
        return [DirectorateCode.from_name(d) for d in self._cc_directorates]

    @cc_directorates.setter
    def cc_directorates(self, directorates: list[DirectorateCode]):
        self._cc_directorates = [d.name for d in directorates]

    @cc_directorates.expression
    def cc_directorates(cls):
        return cls._cc_directorates

    @hybrid_property
    def bcc_directorates(self) -> list[DirectorateCode]:
        if not self._bcc_directorates:
            return []
        return [DirectorateCode.from_name(d) for d in self._bcc_directorates]

    @bcc_directorates.setter
    def bcc_directorates(self, directorates: list[DirectorateCode]):
        self._bcc_directorates = [d.name for d in directorates]

    @bcc_directorates.expression
    def bcc_directorates(cls):
        return cls._bcc_directorates
