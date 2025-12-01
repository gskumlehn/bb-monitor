import os
from flask import render_template
from markupsafe import Markup
from app.enums.directorate_codes import DirectorateCode
from app.enums.mailing_status import MailingStatus
from app.infra.email_manager import EmailManager
from app.services.alert_service import AlertService
from app.services.mailing_service import MailingService
from app.services.mailing_history_service import MailingHistoryService
from app.utils.email_utils import EmailUtils

class EmailService:

    mailing_service = MailingService()

    TO_DIRECTORATE = DirectorateCode.DIMAC_PRIORITARIO
    CC_DIRECTORATE = DirectorateCode.FB

    def get_recipients_for_alert(self, directorates: list[DirectorateCode] = None) -> dict:
        env = os.getenv("ENV", "").strip().upper()

        if env == "DEV":
            email_user = os.getenv("EMAIL_USER")
            bw_email = os.getenv("BW_EMAIL")
            to_list = [email_user] if email_user else []
            cc_list = [bw_email] if bw_email else []
            bcc_list = ["gskumlehn@gmail.com"]
        else:
            to_list = self.mailing_service.get_emails_by_directorates([self.TO_DIRECTORATE]) or []
            cc_list = self.mailing_service.get_emails_by_directorates([self.CC_DIRECTORATE]) or []
            bcc_list = self.mailing_service.get_emails_by_directorates(directorates) if directorates else []

        return {"to": to_list, "cc": cc_list, "bcc": bcc_list}

    def format_description(self, text: str) -> Markup:
        linked_text = EmailUtils.linkify(text)
        boldified_text = EmailUtils.boldify(linked_text)
        return boldified_text

    def render_alert_html(self, alert, should_manage_directorates = False) -> str:
        profile = alert.profiles_or_portals[0]
        email = os.getenv("EMAIL_USER")
        base_url_env = os.getenv("BASE_URL")

        context = {
            "BASE_URL": base_url_env,
            "ALERT_ID": alert.id,
            "EMAIL": email,
            "NIVEL": str(alert.criticality_level.number),
            "TITULO_POSTAGEM": alert.title,
            "PERFIL_USUARIO": profile,
            "DESCRICAO_COMPLETA": self.format_description(alert.alert_text),
            "DIRECTORY": DirectorateCode.FB.name,
            "should_render_mailing_cancelation": False,
            "should_render_manage_directorates": should_manage_directorates,
            "is_repercussion": alert.is_repercussion
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
        env = os.getenv("ENV", "").strip().upper()
        email_manager = EmailManager()

        rendered_html = self.render_alert_html(alert)
        subject = f"[RISCO DE REPUTAÇÃO BB] – Alerta{' de Repercussão' if alert.is_repercussion else ''} Nível {str(alert.criticality_level.number)} - {alert.title}"

        recipients = self.get_recipients_for_alert(directorates=directorates)
        to_list = recipients["to"]
        cc_list = recipients["cc"]
        bcc_list = recipients["bcc"]

        if env == "DEV":
            directorates_str = ", ".join([d.name for d in directorates])
            subject = f"{subject} | Diretorias: {directorates_str}"

        try:
            email_manager.send_email(to_list, subject, rendered_html, cc=cc_list, bcc=bcc_list)
            if True:
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
