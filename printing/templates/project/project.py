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
import datetime

proj = Blueprint("project", __name__)


@proj.route("/project/")
@login_required
def project():
    projects = db.session.query(Project).all()
    return render_template("project/project.html", user=User, projects=projects)


@proj.route("/projectdetails/<int:id>")
@login_required
def projectdetails(id):
    projects = db.session.query(Project).filter(Project.id == id).first()

    timelength = calc_time_length(
        "/Volumes/PTS/program/printing/static/uploads/Califlower.gcode"
    )
    printtime = timelength[0]
    materialused = calculate_weight(timelength[1] / 1000, projects.filamentfk)

    costelectricity = timecost(printtime, projects.filamentfk)

    costfilament = filamentcost(materialused, projects.filamentfk)

    return render_template(
        "project/project_details.html",
        user=User,
        projects=projects,
        materialused=materialused,
        printtime=printtime,
        timecost=costelectricity,
        filcost=costfilament,
    )
