from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus
from app.enums.involved_variables import InvolvedVariables
from app.enums.stakeholders import Stakeholders

class AlertService:

    def save(self, alert_data: dict) -> Alert | None:
        alert = self.validate_and_create(alert_data)

        return AlertRepository.save(alert)

    def validate_and_create(self, alert_data: dict) -> Alert:
        alert = Alert()

        alert.urls = self.parse_list_field(alert_data.get("urls"))
        existing_alert = AlertRepository.get_by_urls(alert.urls)
        if existing_alert:
            raise ValueError("O alerta com a mesma lista de URLs já foi ingerido.")

        alert.title = (alert_data.get("title") or "").strip()

        delivery_datetime = alert_data.get("delivery_datetime")
        if not delivery_datetime:
            raise ValueError("O campo 'delivery_datetime' é obrigatório.")
        alert.delivery_datetime = delivery_datetime

        alert.mailing_status = MailingStatus(alert_data.get("mailing_status").strip())
        alert.criticality_level = CriticalityLevel(alert_data.get("criticality_level").strip())
        alert.alert_types = AlertType.values_csv_to_type_list(alert_data.get("alert_types").strip())

        alert.profiles_or_portals = self.parse_list_field(alert_data.get("profiles_or_portals"))

        alert_text = (alert_data.get("alert_text") or "").strip()
        if not alert_text:
            raise ValueError("O campo 'alert_text' é obrigatório.")
        alert.alert_text = alert_text

        alert.involved_variables = InvolvedVariables.values_csv_to_type_list(alert_data.get("involved_variables", ""))
        alert.stakeholders = Stakeholders.values_csv_to_type_list(alert_data.get("stakeholders", ""))

        history = alert_data.get("history")
        if history:
            alert.history = history.strip()

        return alert

    @staticmethod
    def parse_list_field(value) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [v.strip() for v in value if isinstance(v, str) and v.strip()]
        if isinstance(value, str):
            if "\r\n" in value or "\n" in value:
                parts = [p.strip() for p in value.splitlines() if p.strip()]
                if parts:
                    return parts
            return [p.strip() for p in value.split(",") if p.strip()]
        return []
