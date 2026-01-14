from flask import Blueprint, redirect, url_for
from flask_login import current_user

root_bp = Blueprint("root", __name__)

@root_bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    role = getattr(current_user, "role", None)
    if role == "monitoring":
        return redirect(url_for("ingestion.index"))
    if role == "admin":
        return redirect(url_for("mailing.index"))
    return redirect(url_for("alert.index"))
