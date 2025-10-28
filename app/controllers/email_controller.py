import os

from flask import Blueprint, render_template, request, abort

from app.enums.directorate_codes import DirectorateCode
from app.services.alert_service import AlertService

email_bp = Blueprint("email", __name__)

@email_bp.route("/render/<alert_id>", methods=["GET"])
def render_alert_email(alert_id):
    alert = AlertService().get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    base_url = request.host_url.rstrip('/')
    profile = alert.profiles_or_portals[0]
    email = os.environ("EMAIL_USER")

    context = {
        "BASE_URL": base_url,
        "EMAIL": email,
        "NIVEL": str(alert.criticality_level.number),
        "TITULO_POSTAGEM": alert.title,
        "PERFIL_USUARIO": profile,
        "DESCRICAO_COMPLETA": alert.alert_text,
        "DIRECTORY": DirectorateCode.FB.name,
    }

    return render_template("email-template.html", **context)

