from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)