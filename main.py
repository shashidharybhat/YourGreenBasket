import os
from flask import Flask, session
from applications.database import db
from applications.config import LocalDevelopmentConfig
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

migrate = Migrate()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    migrate.init_app(app, db)
    app.app_context().push()
    login_manager.init_app(app)
    login_manager.login_view = 'Userlogin'
    login_manager.login_message_category = 'info'
    return app


app = create_app()
bcrypt = Bcrypt(app)
from applications.controllers import *


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
