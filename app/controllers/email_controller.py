from flask import Blueprint, request, abort, jsonify
from app.services.alert_service import AlertService
from app.services.email_service import EmailService

email_bp = Blueprint("email", __name__)

@email_bp.route("/render/<alert_id>", methods=["GET"])
def render_alert_email(alert_id):
    alert = AlertService().get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    base_url = request.host_url.rstrip('/')

    rendered = EmailService().render_alert_html(alert, base_url)
    return rendered

@email_bp.route("/send/<alert_id>", methods=["POST"])
def send_alert_email(alert_id):
    alert = AlertService().get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    base_url = request.host_url.rstrip('/')

    try:
        result = EmailService().send_alert_email(alert, base_url)
        return jsonify(result), 200
    except Exception as e:
        abort(500, description=f"Falha ao enviar email: {str(e)}")
