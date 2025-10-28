import os
import re
from flask import render_template
from app.enums.directorate_codes import DirectorateCode
from app.infra.email_manager import EmailManager

class EmailService:

    def linkify(self, text: str) -> str:
        if not text:
            return ""
        parts = text.split(" ")
        pattern = re.compile(r'(https?://[^\s\)\]\}\,;:]+)')
        for i, token in enumerate(parts):
            if "http://" in token or "https://" in token:
                m = pattern.search(token)
                if not m:
                    continue
                url = m.group(1)
                parts[i] = f'<a href="{url}" style="display: inline-block;">{token}</a>'
        return " ".join(parts)

    def render_alert_html(self, alert, base_url: str = None) -> str:
        profile = alert.profiles_or_portals[0]
        email = os.getenv("EMAIL_USER")
        base_url_env = os.getenv("BASE_URL", "")  # sempre usar BASE_URL do env

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

    def send_alert_email(self, alert, base_url: str = None) -> dict:
        to_address = os.getenv("EMAIL_USER")

        subject = f"[RISCO DE REPUTAÇÃO BB] – Alerta de Repercussão Nível {str(alert.criticality_level.number)} - {alert.title}"
        rendered_html = self.render_alert_html(alert)  # render usa BASE_URL do env

        email_manager = EmailManager()
        try:
            email_manager.send_email(to_address, subject, rendered_html)
        except Exception:
            raise

        return {"message": "Email enviado com sucesso", "to": to_address}
