from flask import Flask
from flask_cors import CORS

from config import Config

from .extension import (
    db,
    migrate
)



def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from . import models

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)


    return app