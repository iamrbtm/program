from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_uploads import UploadSet, configure_uploads, IMAGES, ALL
from dotenv import load_dotenv
from flask_mail import Mail


load_dotenv()

db = SQLAlchemy()
photos = UploadSet("photos", IMAGES)
filamentpics = UploadSet("filamentpics", IMAGES)
gcode = UploadSet("gcode", ALL)
invgcode = UploadSet("invgcode", ALL)
avatar = UploadSet("avatar", IMAGES)
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Flask-Uploads & Static
    app.config["UPLOADED_PHOTOS_DEST"] = "printing/static/app/images"
    app.config["UPLOADED_GCODE_DEST"] = "printing/templates/app/project/uploads"
    app.config["UPLOADED_INVGCODE_DEST"] = "printing/templates/app/inventory/uploads"
    app.config["UPLOADED_FILAMENTPICS_DEST"] = "printing/static/app/img/filament"
    app.config["UPLOADED_AVATAR_DEST"] = "printing/static/app/img/avatars"
    configure_uploads(app, photos)
    configure_uploads(app, gcode)
    configure_uploads(app, invgcode)
    configure_uploads(app, filamentpics)
    configure_uploads(app, avatar)

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
    app.config['MAIL_SERVER'] = 'mail.dudefishprinting.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'customer_service@dudefishprinting.com'
    app.config['MAIL_PASSWORD'] = 'Braces4me##'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = ('Dudefish Printing', 'customer_service@dudefishprinting.com')

    mail.init_app(app)

    # Blueprints
    #website
    from printing.templates.website.website import site 
    from printing.auth import auth
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(site, url_prefix='/')
   
    #app
    from printing.templates.app.base.base import base
    from printing.templates.app.project.project import proj
    from printing.templates.app.people.customer import cust
    from printing.templates.app.people.employee import emp
    from printing.templates.app.people.supplier import vendor
    from printing.templates.app.dashboard.dashboard import dash
    from printing.templates.app.settings.settings import stg
    from printing.templates.app.address.address import addy
    from printing.templates.app.filament.filament import fil
    from printing.templates.app.events.events import evt
    from printing.templates.app.testimonial.testimonial import testimony
    from printing.templates.app.inventory.inventory import inv
    from printing.templates.app.sales.sales import sale
    
    app.register_blueprint(base, url_prefix='/')
    app.register_blueprint(proj)
    app.register_blueprint(emp)
    app.register_blueprint(vendor)
    app.register_blueprint(cust)
    app.register_blueprint(dash)
    app.register_blueprint(stg)
    app.register_blueprint(addy)
    app.register_blueprint(fil)
    app.register_blueprint(evt)
    app.register_blueprint(testimony)
    app.register_blueprint(inv)
    app.register_blueprint(sale)

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
            connectstring = f"mysql+pymysql://{os.environ.get('DB_USERNAME')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"

    return [stopper, errorlist, connectstring]

