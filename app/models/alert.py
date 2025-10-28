from sqlalchemy import Column, String, ARRAY, Text
from sqlalchemy_bigquery import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declarative_base
from zoneinfo import ZoneInfo
from datetime import datetime, timezone
import uuid

from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus
from app.custom_utils.date_utils import DateUtils
from app.enums.involved_variables import InvolvedVariables
from app.enums.stakeholders import Stakeholders

Base = declarative_base()

class Alert(Base):
    __tablename__ = "alert"
    __table_args__ = {"schema": "bb_monitor"}

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    _delivery_datetime = Column("delivery_datetime", TIMESTAMP, nullable=False)

    _mailing_status = Column("mailing_status", String(255), nullable=False)
    _alert_types = Column("alert_types", ARRAY(String), nullable=False)
    _involved_variables = Column("involved_variables", ARRAY(String), nullable=True)
    _stakeholders = Column("stakeholders", ARRAY(String), nullable=True)
    _criticality_level = Column("criticality_level", String(255), nullable=False)

    title = Column(Text, nullable=False)
    alert_text = Column(Text, nullable=False)
    _profiles_or_portals = Column("profiles_or_portals", ARRAY(String), nullable=False)
    _urls = Column("urls", ARRAY(Text), nullable=False)

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
    def involved_variables(self) -> list[InvolvedVariables]:
        return [InvolvedVariables.from_name(name) for name in self._involved_variables or []]

    @involved_variables.setter
    def involved_variables(self, variables: list[InvolvedVariables]):
        self._involved_variables = [variable.name for variable in variables] if variables else []

    @involved_variables.expression
    def involved_variables(cls):
        return cls._involved_variables

    @hybrid_property
    def stakeholders(self) -> list[Stakeholders]:
        return [Stakeholders.from_name(name) for name in self._stakeholders or []]

    @stakeholders.setter
    def stakeholders(self, stakeholders: list[Stakeholders]):
        self._stakeholders = [stakeholder.name for stakeholder in stakeholders] if stakeholders else []

    @stakeholders.expression
    def stakeholders(cls):
        return cls._stakeholders

    @hybrid_property
    def profiles_or_portals(self) -> list[str]:
        return self._profiles_or_portals or []

    @profiles_or_portals.setter
    def profiles_or_portals(self, profiles_or_portals: list[str]):
        self._profiles_or_portals = profiles_or_portals

    @profiles_or_portals.expression
    def profiles_or_portals(cls):
        return cls._profiles_or_portals

    @hybrid_property
    def urls(self) -> list[str]:
        return self._urls or []

    @urls.setter
    def urls(self, urls: list[str]):
        self._urls = urls

    @urls.expression
    def urls(cls):
        return cls._urls
