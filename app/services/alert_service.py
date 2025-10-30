from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus
from app.enums.stakeholders import Stakeholders
from app.constants.error_messages import ErrorMessages
import uuid
from typing import Optional

class AlertService:

    def save(self, alert_data: dict) -> Alert:
        self.validate_alert_data(alert_data, check_duplicate=True)
        alert = self.create(alert_data)
        return AlertRepository.save(alert)

    def update(self, alert_id: str, alert_data: dict) -> Optional[Alert]:
        existing = AlertRepository.get_by_id(alert_id)
        if not existing:
            return None

        self.validate_alert_data(alert_data, check_duplicate=False)
        self._apply_alert_data(existing, alert_data, skip_mailing_status=True)
        return AlertRepository.update(existing)

    def save_or_update(self, alert_data: dict) -> Alert:
        urls = alert_data.get("urls")
        if urls:
            existing_alert = AlertRepository.get_by_urls(urls)
            if existing_alert:
                updated = self.update(existing_alert.id, alert_data)

                return updated if updated is not None else existing_alert

        return self.save(alert_data)

    def validate_alert_data(self, alert_data: dict, check_duplicate: bool = True):
        self._validate_required_fields(alert_data)
        self._validate_enum_fields(alert_data)
        if check_duplicate:
            urls = alert_data.get("urls")
            if urls:
                existing = AlertRepository.get_by_urls(urls)
                if existing:
                    msg = ErrorMessages.model.get("Alert.duplicateUrls", "Alerta com mesmas URLs já existe.")
                    raise ValueError(msg)

    def _validate_required_fields(self, alert_data: dict):
        required_fields = [
            "urls",
            "title",
            "delivery_datetime",
            "mailing_status",
            "criticality_level",
            "alert_types",
            "profiles_or_portals",
            "alert_text"
        ]

        missing_fields = [field for field in required_fields if field not in alert_data or not alert_data[field]]
        if missing_fields:
            raise ValueError(ErrorMessages.model["Alert.missingFields"].format(fields=", ".join(missing_fields)))

    def _validate_enum_fields(self, alert_data: dict):
        mailing_status = alert_data.get("mailing_status")
        if not isinstance(mailing_status, MailingStatus):
            raise ValueError(ErrorMessages.model["Alert.mailingStatus.invalid"])

        criticality_level = alert_data.get("criticality_level")
        if not isinstance(criticality_level, CriticalityLevel):
            raise ValueError(ErrorMessages.model["Alert.criticalityLevel.invalid"])

        alert_types = alert_data.get("alert_types", [])
        if not isinstance(alert_types, list) or not all(isinstance(item, AlertType) for item in alert_types):
            raise ValueError(ErrorMessages.model["Alert.alertTypes.invalid"])

        stakeholders = alert_data.get("stakeholders", [])
        if stakeholders and (not isinstance(stakeholders, list) or not all(isinstance(item, Stakeholders) for item in stakeholders)):
            raise ValueError(ErrorMessages.model["Alert.stakeholders.invalid"])

    def create(self, alert_data: dict) -> Alert:
        alert = Alert()
        alert.id = str(uuid.uuid4())
        self._apply_alert_data(alert, alert_data)
        return alert

    def _apply_alert_data(self, alert: Alert, alert_data: dict, skip_mailing_status: bool = False):
        if not skip_mailing_status:
            alert.mailing_status = alert_data.get("mailing_status")
        alert.delivery_datetime = alert_data.get("delivery_datetime")
        alert.alert_types = alert_data.get("alert_types")
        alert.profiles_or_portals = alert_data.get("profiles_or_portals")
        alert.urls = alert_data.get("urls")
        alert.title = alert_data.get("title")
        alert.alert_text = alert_data.get("alert_text")
        alert.criticality_level = alert_data.get("criticality_level")
        alert.critical_topic = alert_data.get("critical_topic")
        alert.press_sources = alert_data.get("press_sources")
        alert.social_media_sources = alert_data.get("social_media_sources")
        alert.stakeholders = alert_data.get("stakeholders")
        alert.social_media_engagements = alert_data.get("social_media_engagements")
        alert.repercussions = alert_data.get("repercussions")
        alert.history = alert_data.get("history")

    def delete_by_id(self, alert_id: str) -> None:
        AlertRepository.delete_by_id(alert_id)

    def get_by_id(self, alert_id: str) -> Alert | None:
        return AlertRepository.get_by_id(alert_id)

    def update_mailing_status(self, alert: Alert, mailing_status: MailingStatus) -> Optional[Alert]:
        alert.mailing_status = mailing_status
        return AlertRepository.update(alert)
