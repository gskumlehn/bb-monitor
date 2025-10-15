from flask import Flask
from dotenv import load_dotenv
from .controllers.mailing_controller import mailing_bp

load_dotenv()

def create_app():

    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.register_blueprint(mailing_bp, url_prefix="/mailing")

    return app