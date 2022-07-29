from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()

db = SQLAlchemy()
photos = UploadSet("photos", IMAGES)
uploads = UploadSet("uploads", ALL)
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Flask-Uploads & Static
    if os.environ.get("UPLOADS_USE") == "True":
        app.config["UPLOADED_PHOTOS_DEST"] = "printing/static/images"
        app.config["UPLOADED_UPLOADS_DEST"] = "printing/static/uploads"
        configure_uploads(app, photos)
        configure_uploads(app, uploads)

    app._static_folder = "static"

    # Secrete Key
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    db.init_app(app)

    # Database Setup
    result = choose_database(app)
    if result[0]:
        print("Connected to database!")
        app.config["SQLALCHEMY_DATABASE_URI"] = result[2]
    else:
        print(result[1])
        abort(403)

    # Migration for Database
    Migrate(app, db)

    # Mail Setup
    config_mail(app)

    # Debug Toolbar
    if os.environ.get("TOOLBAR_USE") == "True":
        if not os.environ.get("SECRET_KEY") == "":
            toolbar = DebugToolbarExtension(app)
            app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
        else:
            print("Please set secret key before proceeding")
            abort(0)

    # Blueprints
    from printing.templates.base.base import base
    from printing.templates.project.project import m_project
    from printing.auth import auth

    app.register_blueprint(base, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(m_project, url_prefix="/project")

    from printing.models import User

    db.create_all(app=app)
    
    # User Manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def choose_database(app):
    stopper = True
    errorlist = []
    if os.environ.get("DB_SQLITE") == "True":
        fields = ["DB_SQLLIGHT_NAME"]

        for field in fields:
            if field not in os.environ:
                msg = f"{field} not configured"
                errorlist.append(msg)
                stopper = False
            if os.environ.get(field) == "":
                msg = f"value for {field} not set"
                errorlist.append(msg)
                stopper = False
        if stopper:
            connectstring = f'sqlite:///{os.environ.get("DB_SQLLIGHT_NAME")}'

    elif os.environ.get("DB_MYSQL") == "True":
        fields = [
            "DB_HOST",
            "DB_USERNAME",
            "DB_USERNAME",
            "DB_PASSWORD",
            "DB_PORT",
            "DB_NAME",
        ]
        for field in fields:
            if field not in os.environ:
                msg = f"{field} not configured"
                errorlist.append(msg)
                stopper = False
            if os.environ.get(field) == "":
                msg = f"value for {field} not set"
                errorlist.append(msg)
                stopper = False
        if stopper:
            connectstring = f"mysql://{os.environ.get('DB_USERNAME')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"

    return [stopper, errorlist, connectstring]


def config_mail(app):
    stopper = True
    errorlist = []
    if os.environ.get("MAIL_USE") == "True":
        fields = [
            "MAIL_SERVER",
            "MAIL_PORT",
            "MAIL_USERNAME",
            "MAIL_PASSWORD",
            "MAIL_USE_TLS",
            "MAIL_USE_SSL",
            "MAIL_DEFAULT_SENDER",
        ]

        for field in fields:
            if field not in os.environ:
                msg = f"{field} not configured"
                errorlist.append(msg)
                stopper = False
            if os.environ.get(field) == "":
                msg = f"value for {field} not set"
                errorlist.append(msg)
                stopper = False
            if stopper:
                app.config[field] = os.environ.get(field)

        if stopper:
            mail.init_app(app)
        else:
            print("DID NOT INIT MAIL... ")
            print(errorlist)
