from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import flask_login
from sqlalchemy.orm import session
from printing.models import *
from printing import db
from printing.utilities import *
import datetime

proj = Blueprint("project", __name__, url_prefix='/project')


@proj.route("/")
@login_required
def project():
    allactive = db.session.query(Project).all()
    return render_template("project/project.html", user=User, projects=allactive)


@proj.route("/projectdetails/<int:id>")
@login_required
def projectdetails(id):
    project = db.session.query(Project).filter(Project.id == id).first()

    timelength = calc_time_length(
        "/Volumes/PTS/program/printing/static/uploads/Califlower.gcode"
    )
    printtime = timelength[0]
    materialused = calculate_weight(timelength[1] / 1000, project.filamentfk)

    costelectricity = timecost(printtime, project.filamentfk)

    costfilament = filamentcost(materialused, project.filamentfk)

    return render_template(
        "project/project_details.html",
        user=User,
        projects=project,
        materialused=materialused,
        printtime=printtime,
        timecost=costelectricity,
        filcost=costfilament
    )
