from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import flask_login
from sqlalchemy.orm import session
from printing.models import *
from printing import db, uploads
from printing.utilities import *
import datetime

proj = Blueprint("project", __name__, url_prefix="/project")

# TODO: new project
# TODO: from open projects, click on the name of the project to take to details page


@proj.route("/")
@login_required
def project():
    allorders = db.session.query(Project).all()
    return render_template("app/project/project.html", user=User, projects=allorders)


@proj.route("/details/<int:id>")
@login_required
def projectdetails(id):
    project1 = CalcCost(id)
    project = db.session.query(Project).filter(Project.id == id).first()

    # timelength = calc_time_length(2,id)

    return render_template(
        "app/project/project_details.html",
        user=User,
        projects=project,
        newproject=project1,
        materialused=project1.kg_weight * 1000,
        printtime=project1.h_printtime,
        timecost=project1.timecost(),
        filcost=project1.filcost(),
        total=project1.total()
    )


@proj.route("/open_orders")
@login_required
def open_orders():
    openorders = db.session.query(Project).filter(Project.active == True).all()
    return render_template(
        "app/project/open_orders.html", user=User, projects=openorders
    )
