from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus

class AlertService:

    def save(self, alert_data: dict) -> Alert:
        url = alert_data.get("url").strip()
        if not url:
            raise ValueError("O campo 'url' é obrigatório.")

        existing_alert = AlertRepository.get_by_url(url)
        if existing_alert:
            return existing_alert

        alert = self.validate_and_create(alert_data)
        return AlertRepository.save(alert)

    def validate_and_create(self, alert_data: dict) -> Alert:
        alert = Alert()
        alert.url = alert_data.get("url").strip()
        alert.brandwatch_id = alert_data.get("brandwatch_id")

        delivery_datetime = alert_data.get("delivery_datetime")
        if not delivery_datetime:
            raise ValueError("O campo 'delivery_datetime' é obrigatório.")
        alert.delivery_datetime = delivery_datetime

        alert.mailing_status = MailingStatus(alert_data.get("mailing_status").strip())
        alert.criticality_level = CriticalityLevel(alert_data.get("criticality_level").strip())
        alert.alert_types = AlertType.values_csv_to_type_list(alert_data.get("alert_types").strip())

        profile_or_portal = alert_data.get("profile_or_portal").strip()
        if not profile_or_portal:
            raise ValueError("O campo 'profile_or_portal' é obrigatório.")
        alert.profile_or_portal = profile_or_portal

        title = alert_data.get("title").strip()
        if not title:
            raise ValueError("O campo 'title' é obrigatório.")
        alert.title = title

        alert_text = alert_data.get("alert_text").strip()
        if not alert_text:
            raise ValueError("O campo 'alert_text' é obrigatório.")
        alert.alert_text = alert_text

        involved_variables = alert_data.get("involved_variables")
        if involved_variables:
            alert.involved_variables = [var.strip() for var in involved_variables.splitlines()]

        stakeholders = alert_data.get("stakeholders")
        if stakeholders:
            alert.stakeholders = [stakeholder.strip() for stakeholder in stakeholders.splitlines()]

        history = alert_data.get("history")
        if history:
            alert.history = history.strip()

        return alert
