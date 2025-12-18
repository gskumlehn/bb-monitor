import os
from flask_login import login_required
from app.services.alert_service import AlertService
from app.services.mailing_history_service import MailingHistoryService
from flask import Blueprint, jsonify, render_template, request
import os

alert_bp = Blueprint("alert", __name__)

alert_service = AlertService()
mailing_history_service = MailingHistoryService()

@alert_bp.get("/ui")
@login_required
def index():
    try:
        base_url = os.getenv("BASE_URL")
        return render_template("alert_list.html", base_url=base_url)
    except Exception as e:
        return jsonify({"error": "Erro ao carregar a página de listagem de alertas", "detail": str(e)}), 500

@alert_bp.get("/list")
@login_required
def list():
    try:
        month = request.args.get("month", type=int)
        year = request.args.get("year", type=int)

        if not month or not year:
            return jsonify({"error": "Mês e ano são obrigatórios"}), 400

        alerts = alert_service.list_by_month_year(month, year)
        return jsonify([alert.to_dict_list() for alert in alerts])
    except Exception as e:
        return jsonify({"error": "Erro ao listar alertas", "detail": str(e)}), 500

@alert_bp.get("/<alert_id>/involved_variables")
def involved_variables(alert_id):
    try:
        alert = alert_service.get_by_id(alert_id)
        alerted_directorates = mailing_history_service.list_alerted_directorates(alert_id)
        if not alert:
            return jsonify({"error": "Alerta não encontrado"}), 404
        return render_template("involved_variables.html", alert=alert, alerted_directorates=alerted_directorates)
    except Exception as e:
        return jsonify({"error": "Erro ao buscar variáveis envolvidas", "detail": str(e)}), 500
