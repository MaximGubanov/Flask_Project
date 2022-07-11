from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_Gubanov_project.config import Config
from flask_bcrypt import Bcrypt
from flask_mail import Mail


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_app():

    app = Flask(__name__)
    db.init_app(app)

    from flask_Gubanov_project.main.routes import main
    app.register_blueprint(main)

    app.config.from_object(Config)
    login_manager.init_app(app)
    bcrypt = Bcrypt()

    from flask_Gubanov_project.users.routes import users
    app.register_blueprint(users)

    from flask_Gubanov_project.posts.routes import posts
    app.register_blueprint(posts)

    from flask_Gubanov_project.errors.handlers import errors
    app.register_blueprint(errors)

    mail.init_app(app)

    return app
