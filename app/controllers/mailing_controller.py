from flask import Blueprint, jsonify, render_template, request
from app.enums.directorate_codes import DirectorateCode
from app.services.mailing_service import MailingService
from app.controllers.decorators import role_required

mailing_bp = Blueprint("mailing", __name__)

mailing_service = MailingService()

@mailing_bp.get("/ui")
@role_required(["client"])
def index():
    directorate_codes = {code.name: code.value for code in DirectorateCode}
    return render_template("mailing.html", directorate_codes=directorate_codes)

@mailing_bp.post("/")
@role_required(["client"])
def save():
    try:
        payload = request.get_json(silent=True) or {}
        email = payload.get("email", "")
        code = payload.get("directorate_code", "")

        mailing_service.save(email, code)
        return jsonify({"ok": True})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Falha ao salvar e-mail", "detail": str(e)}), 500

@mailing_bp.delete("/")
@role_required(["client"])
def delete():
    try:
        payload = request.get_json(silent=True) or {}
        email = payload.get("email", "")
        code = payload.get("directorate_code", "")

        deleted = mailing_service.delete(email, code)
        if deleted:
            return jsonify({"ok": True})
        else:
            return jsonify({"error": "E-mail não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Erro ao remover o e-mail", "detail": str(e)}), 500

@mailing_bp.get("/list")
@role_required(["client"])
def list_emails():
    try:
        code = request.args.get("directorate_code", "")
        emails = mailing_service.list_by_directorate(code)
        return jsonify({"emails": emails})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mailing_bp.get("/list_directorates")
@role_required(["client"])
def list_directorates():
    try:
        email = request.args.get("email", "")
        directorates = mailing_service.list_directorates_by_email(email)
        return jsonify({"directorates": directorates})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
