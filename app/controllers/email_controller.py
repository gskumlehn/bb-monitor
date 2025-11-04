from flask import Blueprint, abort, jsonify
from app.services.alert_service import AlertService
from app.services.email_service import EmailService

email_bp = Blueprint("email", __name__)

alert_service = AlertService()
email_service = EmailService()

@email_bp.route("/render/<alert_id>", methods=["GET"])
def render_alert_email(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    return email_service.render_alert_html(alert)

@email_bp.route("/send/<alert_id>", methods=["POST"])
def send_alert_email(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    try:
        result = email_service.send_alert_email(alert)
        return jsonify(result), 200
    except Exception as e:
        abort(500, description=f"Falha ao enviar email: {str(e)}")

@email_bp.route("/validate/<alert_id>", methods=["GET"])
def validate_recipients_for_alert(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    result = email_service.validate_send(alert)
    return jsonify(result), 200
