from flask import Blueprint, jsonify, render_template, request
from app.enums.directorate_codes import DirectorateCode
from app.services.mailing_service import MailingService
from app.controllers.decorators import role_required

mailing_bp = Blueprint("mailing", __name__)

mailing_service = MailingService()

@mailing_bp.get("/ui")
@role_required(["client"])
def ui():
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

@mailing_bp.get("/delete-ui")
@role_required(["client"])
def delete_ui():
    try:
        email = request.args.get("email", "")
        code = request.args.get("directorate_code", "")

        deleted = mailing_service.delete(email, code)
        if deleted:
            return render_template("message.html", message=f"O e-mail '{email}' foi removido com sucesso do diretório '{code}'.")
        else:
            return render_template("message.html", message=f"O e-mail '{email}' não foi encontrado no diretório '{code}'.")
    except Exception as e:
        return render_template("message.html", message=f"Erro ao remover o e-mail: {str(e)}"), 500
