from sqlalchemy import Column, Integer, String, ARRAY, Text
from sqlalchemy_bigquery import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus
from app.custom_utils.date_utils import DateUtils

Base = declarative_base()

class Alert(Base):
    __tablename__ = "alert"
    __table_args__ = {"schema": "bb_monitor"}

    brandwatch_id = Column(String(255), nullable=True, unique=True)
    _delivery_datetime = Column("delivery_datetime", TIMESTAMP, nullable=False)

    _mailing_status = Column("mailing_status", String(255), nullable=False)
    _criticality_level = Column("criticality_level", String(255), nullable=False)
    _alert_types = Column("alert_types", ARRAY(String), nullable=False)

    profile_or_portal = Column(String(255), nullable=False)
    title = Column(Text, nullable=False)
    alert_text = Column(Text, nullable=False)
    url = Column(Text, primary_key=True, nullable=False)

    _involved_variables = Column("involved_variables", ARRAY(String), nullable=True)
    _stakeholders = Column("stakeholders", ARRAY(String), nullable=True)
    history = Column(Text, nullable=True)

    SP_TZ = ZoneInfo(DateUtils.BRAZIL_TZ)
    UTC_TZ = ZoneInfo(DateUtils.UTC_TZ)

    @hybrid_property
    def delivery_datetime(self) -> datetime:
        if self._delivery_datetime is None:
            return None
        return self._delivery_datetime.astimezone(self.SP_TZ)

    @delivery_datetime.setter
    def delivery_datetime(self, value: datetime):
        if value is None:
            self._delivery_datetime = None
            return
        if not isinstance(value, datetime):
            raise TypeError("delivery_datetime must be a datetime instance")
        utc_dt = DateUtils.to_utc(value, assume_tz=DateUtils.BRAZIL_TZ)
        if utc_dt is not None:
            utc_dt = utc_dt.astimezone(timezone.utc)
        self._delivery_datetime = utc_dt

    @delivery_datetime.expression
    def delivery_datetime(cls):
        return cls._delivery_datetime

    @hybrid_property
    def mailing_status(self) -> MailingStatus:
        return MailingStatus.from_name(self._mailing_status)

    @mailing_status.setter
    def mailing_status(self, status: MailingStatus):
        self._mailing_status = status.name

    @mailing_status.expression
    def mailing_status(cls):
        return cls._mailing_status

    @hybrid_property
    def criticality_level(self) -> CriticalityLevel:
        return CriticalityLevel.from_name(self._criticality_level)

    @criticality_level.setter
    def criticality_level(self, level: CriticalityLevel):
        self._criticality_level = level.name

    @criticality_level.expression
    def criticality_level(cls):
        return cls._criticality_level

    @hybrid_property
    def alert_types(self) -> list[AlertType]:
        return [AlertType.from_name(name) for name in self._alert_types]

    @alert_types.setter
    def alert_types(self, types_list: list[AlertType]):
        self._alert_types = [alert_type.name for alert_type in types_list]

    @alert_types.expression
    def alert_types(cls):
        return cls._alert_types

    @hybrid_property
    def involved_variables(self) -> list[str]:
        return self._involved_variables or []

    @involved_variables.setter
    def involved_variables(self, variables: list[str]):
        self._involved_variables = variables

    @involved_variables.expression
    def involved_variables(cls):
        return cls._involved_variables

    @hybrid_property
    def stakeholders(self) -> list[str]:
        return self._stakeholders or []

    @stakeholders.setter
    def stakeholders(self, stakeholders: list[str]):
        self._stakeholders = stakeholders

    @stakeholders.expression
    def stakeholders(cls):
        return cls._stakeholders
