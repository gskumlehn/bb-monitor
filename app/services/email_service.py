import os
import re
from flask import render_template
from markupsafe import Markup
from app.enums.directorate_codes import DirectorateCode
from app.infra.email_manager import EmailManager

class EmailService:

    def linkify(self, text: str) -> Markup:
        if not text:
            return Markup("")

        a_tags = {}
        def _protect_a(m):
            key = f"__A_TAG_{len(a_tags)}__"
            a_tags[key] = m.group(0)
            return key
        protected = re.sub(r'<a\b[^>]*?>.*?</a>', _protect_a, text, flags=re.IGNORECASE | re.DOTALL)

        url_re = re.compile(r'(?P<open>[\(\[\{])?(?P<url>https?://[^\s<\)\]\}\>,;:]+)(?P<mid>\s*)?(?P<close>[\)\]\}])?')

        def _replace(m):
            open_ch = m.group('open') or ""
            url = m.group('url')
            mid = m.group('mid') or ""
            close_ch = m.group('close') or ""
            if open_ch or close_ch:
                visible = f"{open_ch}{url}{close_ch}"
                return f'<a href="{url}" style="display: inline-block;">{visible}</a>'
            else:
                return f'<a href="{url}" style="display: inline-block;">{url}</a>{mid}'

        linked = url_re.sub(_replace, protected)

        for key, val in a_tags.items():
            linked = linked.replace(key, val)

        return Markup(linked)

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

        return {"message": "Email enviado com sucesso", "to": to_address}
