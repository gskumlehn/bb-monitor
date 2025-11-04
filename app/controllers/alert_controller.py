from flask import Blueprint, jsonify, render_template, request
from app.services.alert_service import AlertService
from flask import Blueprint, jsonify, render_template, request

alert_bp = Blueprint("alert", __name__)

alert_service = AlertService()

@alert_bp.get("/ui")
def ui():
    try:
        return render_template("alert_list.html")
    except Exception as e:
        return jsonify({"error": "Erro ao carregar a página de listagem de alertas", "detail": str(e)}), 500

@alert_bp.get("/list")
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
        if not alert:
            return jsonify({"error": "Alerta não encontrado"}), 404
        return render_template("involved_variables.html", alert=alert)
    except Exception as e:
        return jsonify({"error": "Erro ao buscar variáveis envolvidas", "detail": str(e)}), 500

