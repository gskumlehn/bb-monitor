from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app.controllers.mailing_controller import mailing_bp
from app.controllers.root_controller import root_bp
from app.controllers.ingestion_controller import ingestion_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config['JSON_AS_ASCII'] = False

    app.register_blueprint(mailing_bp, url_prefix="/mailing")
    app.register_blueprint(root_bp, url_prefix="/")
    app.register_blueprint(ingestion_bp, url_prefix="/ingestion")

    return app
