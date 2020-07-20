from flask import Flask
from api.database import db
from .views.user import user
import config


def create_app():

    app = Flask(__name__)

    # DB設定を読み込む
    app.config.from_object('config.Config')
    db.init_app(app)

    app.register_blueprint(user, url_prefix='/user')

    return app


app = create_app()
