from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import flask_login
from sqlalchemy import distinct
from sqlalchemy.orm import session
from printing.models import *
from printing import db, gcode
from printing.utilities import *
import datetime, random

sale = Blueprint("sales", __name__, url_prefix="/sales")

@sale.route("/")
@login_required
def sales():
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active == True).all()
    context = {
        "user":User,
        "inventory":inventory,
    }
    return render_template("app/sales/sales.html", **context)
