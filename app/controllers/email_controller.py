from app.controllers.decorators import role_required
from app.enums.directorate_codes import DirectorateCode
from app.services.alert_service import AlertService
from app.services.directorate_service import DirectorateService
from app.services.email_service import EmailService
from datetime import datetime
from flask import Blueprint, abort, jsonify, request
import os

email_bp = Blueprint("email", __name__)

alert_service = AlertService()
email_service = EmailService()
directorate_service = DirectorateService()

@email_bp.route("/render/<alert_id>", methods=["GET"])
def render_alert_email(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado.")

    return email_service.render_alert_html(alert)

@email_bp.route("/send/<alert_id>", methods=["POST"])
@role_required(["monitoring"])
def send_alert_email(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado.")

    if datetime.now().year > 2025:
        alert = alert_service.assign_sequential_code(alert)

    try:
        automatic_mailing = os.getenv("AUTOMATIC_MAILING") == "true"
        if automatic_mailing:
            directorates = [DirectorateCode.from_name(directorate) for directorate in directorate_service.get_directorates_by_subcategories(alert.subcategories)]
            result = email_service.send_alert_to_directorates(alert, directorates)
        else:
            result = email_service.send_alert_email(alert)
        return jsonify(result), 200
    except Exception:
        abort(500, description="Falha ao enviar e-mail.")

@email_bp.route("/validate/<alert_id>", methods=["GET"])
@role_required(["monitoring"])
def validate_recipients_for_alert(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado.")

    result = email_service.validate_send(alert)
    return jsonify(result), 200

@email_bp.route("/send_to_directorates/<alert_id>", methods=["POST"])
# @role_required(["client"])
def send_alert_to_directorates(alert_id):
    payload = request.get_json(silent=True) or {}
    dir_names = payload.get("directorates") or []
    if not isinstance(dir_names, list):
        abort(400, description="O campo 'directorates' deve ser uma lista de nomes de diretorias.")

    try:
        directorates = [DirectorateCode.from_name(name) for name in dir_names]
    except ValueError:
        abort(400, description="Um ou mais nomes de diretorias são inválidos.")

    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado.")

    try:
        result = email_service.send_alert_to_directorates(alert, directorates)
        return jsonify(result), 200
    except Exception:
        abort(500, description="Falha ao enviar e-mails para as diretorias.")

@email_bp.route("/validate_sent_mailing/<alert_id>", methods=["POST"])
# @role_required(["client"])
def validate_sent_mailing(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado.")

    try:
        result = email_service.validate_sent_mailing(alert)
        return jsonify(result), 200
    except Exception as e:
        print(f"Erro ao validar envio de mailing: {e}")  # Log para depuração
        abort(500, description="Falha ao validar os dados para envio às diretorias.")
