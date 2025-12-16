from flask import Blueprint, jsonify, request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("root.index"))
        next_url = request.args.get("next", "")
        return render_template("login.html", next=next_url)

    email = request.form.get("email")
    password = request.form.get("password")
    next_url = request.form.get("next")

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"status": "success", "redirect": next_url or url_for("root.index")}), 200
    else:
        return jsonify({"status": "error", "message": "Credenciais inválidas. Tente novamente."}), 401

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))
