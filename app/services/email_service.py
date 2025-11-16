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

    def get_recipients_for_alert(self, directorate_code=None) -> dict:
        env = os.getenv("ENV", "").strip().upper()

        if env == "DEV":
            email_user = os.getenv("EMAIL_USER")
            bw_email = os.getenv("BW_EMAIL")
            to_list = [email_user] if email_user else []
            cc_list = [bw_email] if bw_email else []
            return {"to": to_list, "cc": cc_list}

        mailing_service = MailingService()

        if directorate_code:
            to_list = mailing_service.get_emails_by_directorates([directorate_code]) or []
            cc_list = mailing_service.get_emails_by_directorates([DirectorateCode.DIMAC_MARKETING_COM_PRIORITARIO, DirectorateCode.FB]) or []
        else:
            to_list = mailing_service.get_emails_by_directorates([DirectorateCode.DIMAC_MARKETING_COM_PRIORITARIO]) or []
            cc_list = mailing_service.get_emails_by_directorates([DirectorateCode.FB]) or []

        return {"to": to_list, "cc": cc_list}

    def format_description(self, text: str) -> Markup:
        linked_text = EmailUtils.linkify(text)
        boldified_text = EmailUtils.boldify(linked_text)
        return boldified_text

    def render_alert_html(self, alert) -> str:
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
            "is_repercussion": alert.is_repercussion
        }

        return render_template("email-template.html", **context)

    def send_alert_email(self, alert) -> dict:
        recipients = self.get_recipients_for_alert()
        to_list = recipients["to"]
        cc_list = recipients["cc"]

        subject = f"[RISCO DE REPUTAÇÃO BB] – Alerta{' de Repercussão' if alert.is_repercussion else ''} Nível {str(alert.criticality_level.number)} - {alert.title}"
        rendered_html = self.render_alert_html(alert)

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
        results = []

        rendered_html = self.render_alert_html(alert)
        subject_template = f"[RISCO DE REPUTAÇÃO BB] – Alerta{' de Repercussão' if alert.is_repercussion else ''} Nível {str(alert.criticality_level.number)} - {alert.title}"

        if env == "DEV":
            recipients = self.get_recipients_for_alert()
            to_list = recipients["to"]
            cc_list = recipients["cc"]
            directorates_str = ", ".join([d.name for d in directorates])
            subject = f"{subject_template} | Diretorias: {directorates_str}"

            try:
                email_manager.send_email(to_list, subject, rendered_html, cc=cc_list)
                results.append({"directorates": directorates_str, "to": to_list, "cc": cc_list, "status": "sent"})
            except Exception as e:
                results.append({"directorates": directorates_str, "to": to_list, "cc": cc_list, "status": "error", "error": str(e)})

            return {"results": results}

        for directorate in directorates:
            recipients = self.get_recipients_for_alert(directorate_code=directorate)
            to_list = recipients["to"]
            cc_list = recipients["cc"]

            try:
                email_manager.send_email(to_list, subject_template, rendered_html, cc=cc_list)
                results.append({"directorate": directorate.value, "to": to_list, "cc": cc_list, "status": "sent"})

                history_data = {
                    "alert_id": alert.id,
                    "primary_directorate": directorate,
                    "to_emails": to_list,
                    "cc_emails": cc_list,
                    "sender_email": os.getenv("EMAIL_USER"),
                }
                MailingHistoryService().save(history_data)
            except Exception as e:
                results.append({"directorate": directorate.value, "to": to_list, "cc": cc_list, "status": "error", "error": str(e)})
        return {"results": results}
