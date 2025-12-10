import os
from flask import render_template
from markupsafe import Markup
from app.enums.directorate_codes import DirectorateCode
from app.enums.mailing_status import MailingStatus
from app.infra.email_manager import EmailManager
from app.infra.environment import Environment
from app.repositories.alert_repository import AlertRepository
from app.services.alert_service import AlertService
from app.services.mailing_service import MailingService
from app.services.mailing_history_service import MailingHistoryService
from app.custom_utils.email_utils import EmailUtils

class EmailService:

    mailing_service = MailingService()

    TO_DIRECTORATE = DirectorateCode.DIMAC_PRIORITARIO
    CC_DIRECTORATE = DirectorateCode.FB

    def get_recipients_for_alert(self, directorates: list[DirectorateCode] = None) -> dict:
        to_list = self.mailing_service.get_emails_by_directorates([self.TO_DIRECTORATE]) or []
        cc_list = self.mailing_service.get_emails_by_directorates([self.CC_DIRECTORATE]) or []
        bcc_list = self.mailing_service.get_emails_by_directorates(directorates) if directorates else []

        return {"to": to_list, "cc": cc_list, "bcc": bcc_list}

    def format_description(self, text: str) -> Markup:
        linked_text = EmailUtils.linkify(text)
        boldified_text = EmailUtils.boldify(linked_text)
        return boldified_text

    def render_alert_html(self, alert, should_manage_directorates=False) -> str:
        profile = alert.profiles_or_portals[0]
        email = os.getenv("EMAIL_USER")
        base_url_env = os.getenv("BASE_URL")

        previous_alerts = self.format_previous_alerts_data(alert.previous_alerts_ids)

        context = {
            "BASE_URL": base_url_env,
            "ALERT_ID": alert.id,
            "EMAIL": email,
            "NIVEL": str(alert.criticality_level.number),
            "TITULO_POSTAGEM": alert.title,
            "PERFIL_USUARIO": profile,
            "DESCRICAO_COMPLETA": self.format_description(alert.alert_text),
            "DIRECTORY": DirectorateCode.FB.name,
            "IS_REPERCUSSION": alert.is_repercussion,
            "SHOULD_RENDER_MANAGE_DIRECTORATES": should_manage_directorates,
            "PREVIOUS_ALERTS": previous_alerts,
        }

        return render_template("email-template.html", **context)

    def send_alert_email(self, alert) -> dict:
        recipients = self.get_recipients_for_alert()
        to_list = recipients["to"]
        cc_list = recipients["cc"]

        subject = f"[RISCO DE REPUTAÇÃO BB] – Alerta{' de Repercussão' if alert.is_repercussion else ''} Nível {str(alert.criticality_level.number)} - {alert.title}"
        rendered_html = self.render_alert_html(alert, True)

        email_manager = EmailManager()
        try:
            email_manager.send_email(to_list, subject, rendered_html, cc=cc_list)
        except Exception:
            raise

        AlertService().update_mailing_status(alert, MailingStatus.EMAIL_SENT)

        return {"message": "Email enviado com sucesso", "to": to_list, "cc": cc_list}

    def validate_send(self, alert) -> dict:
        recipients = self.get_recipients_for_alert()
        return {"status": alert.mailing_status.name, "recipients": recipients["to"], "cc": recipients["cc"]}

    def send_alert_to_directorates(self, alert, directorates: list[DirectorateCode]) -> dict:
        email_manager = EmailManager()

        rendered_html = self.render_alert_html(alert)
        subject = f"[RISCO DE REPUTAÇÃO BB] – Alerta{' de Repercussão' if alert.is_repercussion else ''} Nível {str(alert.criticality_level.number)} - {alert.title}"

        recipients = self.get_recipients_for_alert(directorates=directorates)
        to_list = recipients["to"]
        cc_list = recipients["cc"]
        bcc_list = recipients["bcc"]

        if Environment.is_development():
            directorates_str = ", ".join([d.name for d in directorates])
            subject = f"{subject} | Diretorias: {directorates_str}"

        try:
            email_manager.send_email(to_list, subject, rendered_html, cc=cc_list, bcc=bcc_list)
            if Environment.is_production():
                history_data = {
                    "alert_id": alert.id,
                    "to_emails": to_list,
                    "cc_emails": cc_list,
                    "bcc_emails": bcc_list,
                    "sender_email": os.getenv("EMAIL_USER"),
                    "to_directorates": [self.TO_DIRECTORATE],
                    "cc_directorates": [self.CC_DIRECTORATE],
                    "bcc_directorates": directorates,
                }
                MailingHistoryService().save(history_data)
            return {"directorates": [d.value for d in directorates], "to": to_list, "cc": cc_list, "bcc": bcc_list, "status": "sent"}
        except Exception as e:
            return {"directorates": [d.value for d in directorates], "to": to_list, "cc": cc_list, "bcc": bcc_list, "status": "error", "error": str(e)}

    def validate_sent_mailing(self, alert) -> dict:
        if alert.mailing_status == MailingStatus.MAILING_SENT:
            mailing_histories = MailingHistoryService().list(alert.id)
            all_directorates = set()

            for history in mailing_histories:
                all_directorates.update(history.bcc_directorates)

            return {
                "alerted_directorates": [directorate.value for directorate in list(all_directorates)]
            }

        return {
            "alerted_directorates": [],
        }


    def format_previous_alerts_data(self, previous_alerts_ids: list) -> list:
        if not previous_alerts_ids:
            return []

        previous_alerts = sorted(AlertRepository.list_by_ids(previous_alerts_ids), key=lambda a: a.delivery_datetime)

        return [
            {
                "id": alert.id,
                "delivery_datetime": alert.delivery_datetime.strftime("%d/%m/%Y %H:%M"),
                "criticality_level": alert.criticality_level.value,
            }
            for alert in previous_alerts
        ]