import os
import re
from flask import render_template
from markupsafe import Markup
from app.enums.directorate_codes import DirectorateCode
from app.enums.mailing_status import MailingStatus
from app.infra.email_manager import EmailManager
from app.services.alert_service import AlertService
from app.services.mailing_service import MailingService

class EmailService:

    def get_recipients_for_alert(self, alert) -> dict:
        env = os.getenv("ENV", "").strip().upper()

        if env == "DEV":
            email_user = os.getenv("EMAIL_USER")
            bw_email = os.getenv("BW_EMAIL")
            to_list = [email_user] if email_user else []
            cc_list = [bw_email] if bw_email else []
            return {"to": to_list, "cc": cc_list}

        mailing_service = MailingService()
        to_list = mailing_service.get_emails_by_directorates([DirectorateCode.DIMAC_MARKETING_COM]) or []
        cc_list = mailing_service.get_emails_by_directorates([DirectorateCode.FB]) or []

        return {"to": to_list, "cc": cc_list}

    def format_description(self, text: str) -> Markup:
        linked_text = self.linkify(text)
        boldified_text = self.boldify(linked_text)
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
            "DESCRICAO_COMPLETA": self.format_description(alert.alert_text),  # Updated to use format_description
            "DIRECTORY": DirectorateCode.FB.name,
            "should_render_mailing_cancelation": False,
            "is_repercussion": False
        }

        return render_template("email-template.html", **context)

    def send_alert_email(self, alert) -> dict:
        recipients = self.get_recipients_for_alert(alert)
        to_list = recipients["to"]
        cc_list = recipients["cc"]

        is_repercussion = False
        subject = f"[RISCO DE REPUTAÇÃO BB] – Alerta{' de Repercussão' if is_repercussion else ''} Nível {str(alert.criticality_level.number)} - {alert.title}"
        rendered_html = self.render_alert_html(alert)

        email_manager = EmailManager()
        try:
            email_manager.send_email(to_list, subject, rendered_html, cc=cc_list)
        except Exception:
            raise

        AlertService().update_mailing_status(alert, MailingStatus.EMAIL_SENT)

        return {"message": "Email enviado com sucesso", "to": to_list, "cc": cc_list}

    def validate_send(self, alert) -> dict:
        recipients = self.get_recipients_for_alert(alert)
        return {"status": alert.mailing_status.name, "recipients": recipients["to"], "cc": recipients["cc"]}

    def linkify(self, text: str) -> Markup:
        if not text:
            return Markup("")

        s = text.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\\r', '\n')

        a_tags = {}
        def _protect_a(m):
            key = f"__A_TAG_{len(a_tags)}__"
            a_tags[key] = m.group(0)
            return key
        protected = re.sub(r'<a\b[^>]*?>.*?</a>', _protect_a, s, flags=re.IGNORECASE | re.DOTALL)

        url_pattern = re.compile(r'https?://[^\s<>()\[\]{}]+', flags=re.IGNORECASE)

        result_parts = []
        last_idx = 0
        for m in url_pattern.finditer(protected):
            start, end = m.start(), m.end()

            consume_start = start
            consume_end = end

            open_ch = ""
            if start - 1 >= 0 and protected[start - 1] in "([{":
                open_ch = protected[start - 1]
                consume_start = start - 1

            close_ch = ""
            if end < len(protected) and protected[end] in ")]}":
                close_ch = protected[end]
                consume_end = end + 1

            result_parts.append(protected[last_idx:consume_start])

            url = m.group(0)
            visible = f"{open_ch}{url}{close_ch}"
            anchor = f'<a href="{url}" style="display: inline-block;">{visible}</a>'
            result_parts.append(anchor)

            last_idx = consume_end

        result_parts.append(protected[last_idx:])
        linked = "".join(result_parts)

        for key, val in a_tags.items():
            linked = linked.replace(key, val)

        wrapped = f'<div style="white-space: pre-wrap;">{linked}</div>'
        return Markup(wrapped)

    def boldify(self, text: str) -> Markup:
        pattern = re.compile(r'(\*{1,2})(.+?)\1', flags=re.DOTALL)

        def replace_bold(match):
            content = match.group(2)
            return f"<b>{content}</b>"

        result = re.sub(pattern, replace_bold, text)
        return Markup(result)
