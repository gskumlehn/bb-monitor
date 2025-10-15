# app/controllers/mailing_controller.py
from flask import Blueprint, request, jsonify, render_template

from app.services.mailing_service import MailingService

mailing_bp = Blueprint("mailing", __name__, url_prefix="/mailing")
svc = MailingService()

@mailing_bp.get("/")
def list_all():
    data = svc.list_all()
    return jsonify(data)

@mailing_bp.post("/")
def add():
    if request.is_json:
        email = (request.json.get("email") or "").strip()
        code  = (request.json.get("directorate_code") or "").strip()
    else:
        email = (request.form.get("email") or "").strip()
        code  = (request.form.get("directorate_code") or "").strip()

    if not email or not code:
        return jsonify({"error": "Informe email e directorate_code"}), 400

    svc.add(email, code)
    return jsonify({"ok": True})

@mailing_bp.delete("/")
def remove():
    email = (request.args.get("email") or "").strip()
    code  = (request.args.get("directorate_code") or "").strip()

    if not email or not code:
        return jsonify({"error": "Informe email e directorate_code"}), 400

    deleted = svc.remove(email, code)
    return jsonify({"deleted": deleted})

@mailing_bp.get("/ui")
def ui():
    return render_template("mailing.html")
