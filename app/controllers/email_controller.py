from flask import Blueprint, render_template, request, abort
from app.services.alert_service import AlertService

email_bp = Blueprint("email", __name__)

@email_bp.route("/render/<alert_id>", methods=["GET"])
def render_alert_email(alert_id):
    alert = AlertService().get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    base_url = request.host_url.rstrip('/')
    profiles = alert.profiles_or_portals or []
    stakeholders = alert.stakeholders or []

    context = {
        "BASE_URL": base_url,
        "NIVEL": str(alert.criticality_level) if alert.criticality_level is not None else "",
        "TITULO_POSTAGEM": alert.title or "",
        "PERFIL_USUARIO": profiles[0] if isinstance(profiles, list) and profiles else "",
        "AREAS_GESTORAS": ", ".join(stakeholders) if isinstance(stakeholders, list) else "",
        "AREAS_INFORMADAS": ", ".join(profiles) if isinstance(profiles, list) else "",
        "DESCRICAO_COMPLETA": alert.alert_text or "",
        "LINK_DUVIDAS": (alert.urls[0] if isinstance(alert.urls, list) and alert.urls else "#"),
        "EMAIL_CONTATO": "",  # opcional: preencher via env ou config se disponível
        "EMAIL": "",
        "DIRECTORY": "",
        "PERFIL_USUARIO": profiles[0] if isinstance(profiles, list) and profiles else "",
        "AREAS_GESTORAS": ", ".join(stakeholders) if isinstance(stakeholders, list) else "",
        "AREAS_INFORMADAS": ", ".join(profiles) if isinstance(profiles, list) else "",
        "DESCRICAO_COMPLETA": alert.alert_text or "",
        "Historico": alert.history or ""
    }

    return render_template("email-template.html", **context)

