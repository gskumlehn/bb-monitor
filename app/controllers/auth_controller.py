from flask import Blueprint, jsonify, request, redirect, url_for, flash, render_template, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.database import db
from app.controllers.decorators import role_required
from app.infra.email_manager import EmailManager
import random
import string

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

@auth_bp.route("/admin", methods=["GET", "POST"])
@role_required(["admin"])
def admin():
    if request.method == "GET":
        return render_template("admin.html")

    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        role = data.get("role")

        if not email or not username or not password or not confirm_password or not role:
            return jsonify({"status": "error", "message": "Todos os campos são obrigatórios."}), 400

        if password != confirm_password:
            return jsonify({"status": "error", "message": "As senhas não coincidem."}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"status": "error", "message": "Já existe um usuário com este email."}), 400

        new_user = User(email=email, username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status": "success", "message": "Usuário criado com sucesso!"}), 201

@auth_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("change_password.html")

    data = request.get_json()
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_password or not new_password:
        return jsonify({"status": "error", "message": "Todos os campos são obrigatórios."}), 400

    if not current_user.check_password(current_password):
        return jsonify({"status": "error", "message": "Senha atual incorreta."}), 400

    current_user.set_password(new_password)
    db.session.commit()
    return jsonify({"status": "success", "message": "Senha alterada com sucesso!"}), 200

@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")

    email = request.form.get("email")
    if not email:
        return jsonify({"status": "error", "message": "O email é obrigatório."}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"status": "error", "message": "Usuário não encontrado."}), 404

    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    user.set_password(temp_password)
    db.session.commit()

    subject = "Redefinição de Senha"
    body = (
        f"Olá {user.username},\n\n"
        f"Uma senha temporária foi gerada para sua conta: {temp_password}\n\n"
        f"Recomendamos que você altere sua senha imediatamente. "
        f"Para isso, clique no link abaixo:\n"
        f"{url_for('auth.change_password', _external=True)}\n\n"
    )

    email_service = EmailManager()
    email_service.send_email([user.email], subject, body)

    return jsonify({"status": "success", "message": "Uma senha temporária foi enviada para o seu email."}), 200
