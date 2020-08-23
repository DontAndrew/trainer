from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from apptest.config import Config

# instantiate the SQLAlchemy to "db" which is the database
db = SQLAlchemy()

# instantiate Bcrypt, basically has hashing function
bcrypt = Bcrypt()

# hands all the login function of the app
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    # instantiate the flask module into the "app" variable
    app = Flask(__name__)

    # the .config imported from config.py
    app.config.from_object(Config)

    # TODO: read the flask documentation!, about creating app inside function
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # imports the packages here to avoid circular import
    # dirName=apptest, package="main"
    from apptest.main.routes import main
    from apptest.users.routes import users
    from apptest.projects.routes import projects

    # error handler
    from apptest.errors.handlers import errors

    # blueprint function, TODO: read the documentation
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(projects)
    app.register_blueprint(errors)

    return app

