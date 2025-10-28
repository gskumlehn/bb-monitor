from flask import Blueprint, redirect, url_for, jsonify

root_bp = Blueprint("root", __name__)

@root_bp.get("/")
def index():
    return redirect(url_for("ingestion.index"))

@root_bp.get("/healthz")
def healthz():
    return jsonify(ok=True), 200
