from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus
from app.enums.involved_variables import InvolvedVariables
from app.enums.stakeholders import Stakeholders
from app.constants.error_messages import ErrorMessages
import uuid

class AlertService:

    def save(self, alert_data: dict) -> Alert | None:
        urls = alert_data.get("urls")
        if urls:
            existing_alert = AlertRepository.get_by_urls(urls)
            if existing_alert:
                return existing_alert

        self.validate_alert_data(alert_data)
        alert = self.create(alert_data)

        return AlertRepository.save(alert)

    def validate_alert_data(self, alert_data: dict):
        self._validate_required_fields(alert_data)
        self._validate_enum_fields(alert_data)

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

        involved_variables = alert_data.get("involved_variables", [])
        if involved_variables and (not isinstance(involved_variables, list) or not all(isinstance(item, InvolvedVariables) for item in involved_variables)):
            raise ValueError(ErrorMessages.model["Alert.involvedVariables.invalid"])

        stakeholders = alert_data.get("stakeholders", [])
        if stakeholders and (not isinstance(stakeholders, list) or not all(isinstance(item, Stakeholders) for item in stakeholders)):
            raise ValueError(ErrorMessages.model["Alert.stakeholders.invalid"])

    def create(self, alert_data: dict) -> Alert:
        alert = Alert()

        alert.id = str(uuid.uuid4())
        alert.title = alert_data.get("title")
        alert.delivery_datetime = alert_data.get("delivery_datetime")
        alert.mailing_status = alert_data.get("mailing_status")
        alert.criticality_level = alert_data.get("criticality_level")
        alert.alert_types = alert_data.get("alert_types")
        alert.profiles_or_portals = alert_data.get("profiles_or_portals")
        alert.alert_text = alert_data.get("alert_text")
        alert.involved_variables = alert_data.get("involved_variables")
        alert.stakeholders = alert_data.get("stakeholders")
        alert.history = alert_data.get("history")
        alert.urls = alert_data.get("urls")

        return alert

    def delete_by_id(self, alert_id: str) -> None:
        AlertRepository.delete_by_id(alert_id)

    def get_by_id(self, alert_id: str) -> Alert | None:
        return AlertRepository.get_by_id(alert_id)
