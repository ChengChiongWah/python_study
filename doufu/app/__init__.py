#!/usr/bin/env python3.5
# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_seasurf import SeaSurf
from config import Config

db = SQLAlchemy()
csrf = SeaSurf()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login_view'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .main import main
    app.register_blueprint(main)

    from .recipe import recipe
    app.register_blueprint(recipe, url_prefix='/recipe')

    from .auth import auth
    app.register_blueprint(auth)

    return app
