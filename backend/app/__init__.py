from flask import Flask
from flask_cors import CORS

from config import Config

from .extension import (
    db,
    migrate,
    jwt
)

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

    return app
