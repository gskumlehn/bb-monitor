from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from werkzeug.security import check_password_hash
from app.database import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("root.index"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        next_url = request.args.get("next")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(next_url or url_for("root.index"))
        else:
            flash("Credenciais inválidas. Tente novamente.", "danger")

    next_url = request.args.get("next")  # Pass the `next` parameter to the template
    return render_template("login.html", next=next_url)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))
