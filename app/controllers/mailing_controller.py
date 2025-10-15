# app/controllers/mailing_controller.py
from flask import Blueprint, jsonify, request, render_template, current_app as app
from app.services.mailing_service import MailingService

mailing_bp = Blueprint("mailing", __name__)
mailing_bp.strict_slashes = False

@mailing_bp.get("/ui")
def ui():
    return render_template("mailing.html")

@mailing_bp.get("/")
def list_all():
    try:
        svc = MailingService()
        data = svc.list_all()
        return jsonify(data)
    except Exception as e:
        app.logger.exception("Erro no GET /mailing")
        return jsonify({"error": "Falha ao listar e-mails", "detail": str(e)}), 500

@mailing_bp.post("/")
def add():
    try:
        payload = request.get_json(silent=True) or {}
        email = (payload.get("email") or "").strip()
        code = (payload.get("directorate_code") or "").strip()
        if not email or not code:
            return jsonify({"error": "email e directorate_code são obrigatórios"}), 400

        svc = MailingService()
        svc.add(email, code)
        return jsonify({"ok": True})
    except Exception as e:
        app.logger.exception("Erro no POST /mailing")
        return jsonify({"error": "Falha ao adicionar e-mail", "detail": str(e)}), 500

@mailing_bp.delete("/")
def remove():
    try:
        email = (request.args.get("email") or "").strip()
        code  = (request.args.get("directorate_code") or "").strip()
        if not email or not code:
            return jsonify({"error": "email e directorate_code são obrigatórios"}), 400

        svc = MailingService()
        removed = svc.remove(email, code)
        return jsonify({"removed": removed})
    except Exception as e:
        app.logger.exception("Erro no DELETE /mailing")
        return jsonify({"error": "Falha ao remover e-mail", "detail": str(e)}), 500
