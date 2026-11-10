import os

from flask import Flask, abort, send_from_directory
from flask_cors import CORS

from config import Config

from .extension import (
    db,
    migrate,
    jwt
)

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)
    # flask-jwt-extended needs a key even though nothing issues tokens yet
    app.config["JWT_SECRET_KEY"] = app.config.get("JWT_SECRET_KEY") or app.config["SECRET_KEY"]

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    from . import models

    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    from app.routes.health import health_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(health_bp)

    # Serve the static frontend too, so `python run.py` works on its own.
    # (In Docker only the nginx frontend serves these files.)
    if os.path.isdir(FRONTEND_DIR):
        @app.route("/")
        def index():
            return send_from_directory(FRONTEND_DIR, "landing_page.html")

        @app.route("/<path:filename>")
        def frontend(filename):
            path = os.path.join(FRONTEND_DIR, filename)
            if os.path.isfile(path):
                return send_from_directory(FRONTEND_DIR, filename)
            abort(404)

    return app
