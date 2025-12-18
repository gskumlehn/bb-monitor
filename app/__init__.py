from app.controllers.alert_controller import alert_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.directorate_controller import directorate_bp
from app.controllers.email_controller import email_bp
from app.controllers.ingestion_controller import ingestion_bp
from app.controllers.mailing_controller import mailing_bp
from app.controllers.root_controller import root_bp
from app.database import db, login_manager
from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import secrets

from app.infra.environment import Environment


def create_app():
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # AWS RDS CONFIG
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    ADMIN_DB_NAME = os.getenv('ADMIN_DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{ADMIN_DB_NAME}"

    if Environment.is_development():
        secret = secrets.token_hex(32)
    else:
        secret = os.getenv('SECRET_KEY')

    app.config['SECRET_KEY'] = secret

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config['JSON_AS_ASCII'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models.user import User, Roles

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(ingestion_bp, url_prefix="/ingestion")
    app.register_blueprint(root_bp, url_prefix="/")
    app.register_blueprint(mailing_bp, url_prefix="/mailing")
    app.register_blueprint(email_bp, url_prefix="/email")
    app.register_blueprint(alert_bp, url_prefix="/alert")
    app.register_blueprint(directorate_bp, url_prefix="/directorate")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()

    return app
