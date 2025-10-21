from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.enums.alert_type import AlertType
from app.enums.criticality_level import CriticalityLevel
from app.enums.mailing_status import MailingStatus

class AlertService:

    def save(self, alert_data: dict) -> Alert:
        alert_data = self.validate_and_parse(alert_data)
        alert = self.create_alert(alert_data)
        AlertRepository.save(alert)

        return alert

    def validate_and_parse(self, alert_data: dict) -> dict:
        if not alert_data.get("brandwatch_id"):
            raise ValueError("O campo 'brandwatch_id' é obrigatório.")

        if not alert_data.get("delivery_datetime"):
            raise ValueError("O campo 'delivery_datetime' é obrigatório.")

        alert_data["mailing_status"] = MailingStatus(alert_data.get("mailing_status"))
        alert_data["criticality_level"] = CriticalityLevel(alert_data.get("criticality_level"))
        alert_data["alert_types"] = AlertType.values_csv_to_type_list(alert_data.get("alert_types"))

        if not alert_data.get("profile_or_portal"):
            raise ValueError("O campo 'profile_or_portal' é obrigatório.")
        if not alert_data.get("title"):
            raise ValueError("O campo 'title' é obrigatório.")
        if not alert_data.get("alert_text"):
            raise ValueError("O campo 'alert_text' é obrigatório.")
        if not alert_data.get("url"):
            raise ValueError("O campo 'url' é obrigatório.")

        involved_variables = alert_data.get("involved_variables")
        if involved_variables:
            alert_data["involved_variables"] = [var.strip() for var in involved_variables.split("\r\n")]

        stakeholders = alert_data.get("stakeholders")
        if stakeholders:
            alert_data["stakeholders"] = [stakeholder.strip() for stakeholder in stakeholders.split("\r\n")]

        return alert_data

    def create_alert(self, alert_data: dict) -> Alert:
        alert = Alert()
        alert.brandwatch_id = alert_data.get("brandwatch_id")
        alert.delivery_datetime = alert_data.get("delivery_datetime")
        alert.mailing_status = alert_data.get("mailing_status")
        alert.criticality_level = alert_data.get("criticality_level")
        alert.alert_types = alert_data.get("alert_types")
        alert.profile_or_portal = alert_data.get("profile_or_portal")
        alert.title = alert_data.get("title")
        alert.alert_text = alert_data.get("alert_text")
        alert.url = alert_data.get("url")
        alert.involved_variables = alert_data.get("involved_variables")
        alert.stakeholders = alert_data.get("stakeholders")
        alert.history = alert_data.get("history")

        return alert
