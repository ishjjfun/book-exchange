from flask import Flask
from flask_mail import Mail

from app.models.base import db
from flask_login import LoginManager

mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'web.login'
login_manager.login_message = '请先登录'


def creat_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from app.web.test import web
    app.register_blueprint(web)

