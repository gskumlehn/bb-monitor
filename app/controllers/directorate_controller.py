from flask import abort, Blueprint, render_template

from app.enums.directorate_codes import DirectorateCode
from app.services.alert_service import AlertService

directorate_bp = Blueprint("directorate", __name__, url_prefix="/directorates")

alert_service = AlertService()

@directorate_bp.route("/alerts/<alert_id>", methods=["GET"])
def manage_directorates(alert_id):
    alert = alert_service.get_by_id(alert_id)
    if not alert:
        abort(404, description="Alerta não encontrado")

    return render_template(
        "assign_directorates.html",
        alert=alert,
        directorate_codes=DirectorateCode.list_excluding()
    )
