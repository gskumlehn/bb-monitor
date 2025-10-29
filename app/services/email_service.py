import os
import re
from flask import render_template
from markupsafe import Markup
from app.enums.directorate_codes import DirectorateCode
from app.enums.mailing_status import MailingStatus
from app.infra.email_manager import EmailManager
from app.services.alert_service import AlertService

class EmailService:

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

    def render_alert_html(self, alert) -> str:
        profile = alert.profiles_or_portals[0]
        email = os.getenv("EMAIL_USER")
        base_url_env = os.getenv("BASE_URL", "")

        context = {
            "BASE_URL": base_url_env,
            "EMAIL": email,
            "NIVEL": str(alert.criticality_level.number),
            "TITULO_POSTAGEM": alert.title,
            "PERFIL_USUARIO": profile,
            "DESCRICAO_COMPLETA": self.linkify(alert.alert_text),
            "DIRECTORY": DirectorateCode.FB.name
        }

        return render_template("email-template.html", **context)

    def send_alert_email(self, alert) -> dict:
        to_address = os.getenv("EMAIL_USER")

        subject = f"[RISCO DE REPUTAÇÃO BB] – Alerta de Repercussão Nível {str(alert.criticality_level.number)} - {alert.title}"
        rendered_html = self.render_alert_html(alert)

        email_manager = EmailManager()
        try:
            email_manager.send_email(to_address, subject, rendered_html)
        except Exception:
            raise

        AlertService().update_mailing_status(alert, MailingStatus.EMAIL_SENT)

        return {"message": "Email enviado com sucesso", "to": to_address}

    def validate_send(self, alert) -> dict:
        user = os.getenv("EMAIL_USER")
        env_to = os.getenv("EMAIL_TO", "")
        recipients = [r.strip() for r in env_to.split(",") if r.strip()] if env_to else []
        if not recipients and user:
            recipients = [user]

        status = None
        try:
            status = alert.mailing_status.name
        except Exception:
            status = None

        return {"status": status, "recipients": recipients}
