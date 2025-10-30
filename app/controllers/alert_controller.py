from flask import Blueprint, jsonify, render_template
from app.services.alert_service import AlertService

alert_bp = Blueprint("alert", __name__)
alert_bp.strict_slashes = False

alert_service = AlertService()

@alert_bp.get("/<alert_id>")
def get_alert(alert_id):
    try:
        alert = alert_service.get_by_id(alert_id)
        if not alert:
            return jsonify({"error": "Alerta não encontrado"}), 404
        return jsonify(alert.to_dict())
    except Exception as e:
        return jsonify({"error": "Erro ao buscar alerta", "detail": str(e)}), 500

@alert_bp.get("/<alert_id>/involved_variables")
def involved_variables(alert_id):
    try:
        alert = alert_service.get_by_id(alert_id)
        if not alert:
            return jsonify({"error": "Alerta não encontrado"}), 404
        return render_template("involved_variables.html", alert=alert)
    except Exception as e:
        return jsonify({"error": "Erro ao buscar variáveis envolvidas", "detail": str(e)}), 500
