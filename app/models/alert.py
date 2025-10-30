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
from app.enums.stakeholders import Stakeholders
from app.enums.press_source import PressSource
from app.enums.social_media_source import SocialMediaSource
from app.enums.critical_topic import CriticalTopic
from app.enums.social_media_engagement import SocialMediaEngagement
from app.enums.repercussion import Repercussion

Base = declarative_base()

class Alert(Base):
    __tablename__ = "alert"
    __table_args__ = {"schema": "bb_monitor"}

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    _mailing_status = Column("mailing_status", String(255), nullable=False)
    _delivery_datetime = Column("delivery_datetime", TIMESTAMP, nullable=False)
    _alert_types = Column("alert_types", ARRAY(String), nullable=False)
    _profiles_or_portals = Column("profiles_or_portals", ARRAY(String), nullable=False)
    _urls = Column("urls", ARRAY(Text), nullable=False)
    title = Column(Text, nullable=False)
    alert_text = Column(Text, nullable=False)

    _criticality_level = Column("criticality_level", String(255), nullable=False)
    _critical_topic = Column("critical_topic", ARRAY(String), nullable=False)
    _press_sources = Column("press_sources", ARRAY(String), nullable=True)
    _social_media_sources = Column("social_media_sources", ARRAY(String), nullable=True)
    _stakeholders = Column("stakeholders", ARRAY(String), nullable=True)
    _social_media_engagements = Column("social_media_engagements", ARRAY(String), nullable=True)
    _repercussions = Column("repercussions", ARRAY(String), nullable=True)
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
        self._delivery_datetime = value

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

    @hybrid_property
    def critical_topic(self) -> list[CriticalTopic]:
        return [CriticalTopic.from_name(name) for name in self._critical_topic or []]

    @critical_topic.setter
    def critical_topic(self, topics: list[CriticalTopic]):
        self._critical_topic = [topic.name for topic in topics] if topics else []

    @critical_topic.expression
    def critical_topic(cls):
        return cls._critical_topic

    @hybrid_property
    def press_sources(self) -> list[PressSource]:
        return [PressSource.from_name(name) for name in self._press_sources or []]

    @press_sources.setter
    def press_sources(self, sources: list[PressSource]):
        self._press_sources = [source.name for source in sources] if sources else []

    @press_sources.expression
    def press_sources(cls):
        return cls._press_sources

    @hybrid_property
    def social_media_sources(self) -> list[SocialMediaSource]:
        return [SocialMediaSource.from_name(name) for name in self._social_media_sources or []]

    @social_media_sources.setter
    def social_media_sources(self, sources: list[SocialMediaSource]):
        self._social_media_sources = [source.name for source in sources] if sources else []

    @social_media_sources.expression
    def social_media_sources(cls):
        return cls._social_media_sources

    @hybrid_property
    def social_media_engagements(self) -> list[SocialMediaEngagement]:
        return [SocialMediaEngagement.from_name(name) for name in self._social_media_engagements or []]

    @social_media_engagements.setter
    def social_media_engagements(self, engagements: list[SocialMediaEngagement]):
        self._social_media_engagements = [engagement.name for engagement in engagements] if engagements else []

    @social_media_engagements.expression
    def social_media_engagements(cls):
        return cls._social_media_engagements

    @hybrid_property
    def repercussions(self) -> list[Repercussion]:
        return [Repercussion.from_name(name) for name in self._repercussions or []]

    @repercussions.setter
    def repercussions(self, repercussions: list[Repercussion]):
        self._repercussions = [repercussion.name for repercussion in repercussions] if repercussions else []

    @repercussions.expression
    def repercussions(cls):
        return cls._repercussions
