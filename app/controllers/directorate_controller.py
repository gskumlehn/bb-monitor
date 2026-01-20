from app.enums.directorate_codes import DirectorateCode
from app.services.alert_service import AlertService
from app.services.directorate_service import DirectorateService
from app.services.mailing_history_service import MailingHistoryService
from flask import abort, Blueprint, render_template, jsonify
from flask_login import login_required

directorate_bp = Blueprint("directorate", __name__, url_prefix="/directorate")

alert_service = AlertService()
directorate_service = DirectorateService()
mailing_history_service = MailingHistoryService()

@directorate_bp.route("/alert/<alert_id>", methods=["GET"])
@login_required
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
@login_required
def list_alerted_directorates(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    suggested_directorates = directorate_service.get_directorates_by_subcategories(alert.subcategories)
    
    alerted_directorates_enums = mailing_history_service.list_alerted_directorates(alert_id)
    alerted_directorates = [d.name for d in alerted_directorates_enums]

    return jsonify({
        "suggested": suggested_directorates,
        "alerted": alerted_directorates
    }), 200
