from flask import Flask
from .controllers.image_controller import image_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.register_blueprint(image_bp, url_prefix="/images")

    return app
