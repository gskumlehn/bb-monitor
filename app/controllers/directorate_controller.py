from app.enums.directorate_codes import DirectorateCode
from app.services.alert_service import AlertService
from app.services.directorate_service import DirectorateService
from flask import abort, Blueprint, render_template, jsonify

directorate_bp = Blueprint("directorate", __name__, url_prefix="/directorate")

alert_service = AlertService()
directorate_service = DirectorateService()

@directorate_bp.route("/alert/<alert_id>", methods=["GET"])
def manage_directorates(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    return render_template(
        "assign_directorates.html",
        alert=alert,
        directorate_codes=DirectorateCode.list_excluding()
    )

@directorate_bp.route("/list_alerted_directorates/<alert_id>", methods=["POST"])
def list_alerted_directorates(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    result = directorate_service.list_categories_for_urls(alert)
    return jsonify(result), 200
