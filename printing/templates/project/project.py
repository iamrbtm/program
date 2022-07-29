from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    after_this_request,
    flash,
)
from flask_login import login_required, current_user
import flask_login
from sqlalchemy.orm import session
from printing.models import *
from printing import db, photos
from printing.forms import *
from printing.utilities import *
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

m_project = Blueprint("project", __name__)


@m_project.route("/")
@login_required
def project():
    projects = db.session.query(Project).all()
    return render_template("project/project.html", user=User, projects=projects)