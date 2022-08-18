from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import flask_login
from sqlalchemy import distinct
from sqlalchemy.orm import session
from printing.models import *
from printing import db, gcode
from printing.utilities import *
import datetime, random

inv = Blueprint("inventory", __name__, url_prefix="/inventory")

@inv.route("/")
@login_required
def inventory():
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active == True).all()
    context = {
        "user":User,
        "inventory":inventory
    }
    return render_template("app/inventory/inventory.html", **context)


@inv.route("/details/<id>")
@login_required
def inventory_details(id):
    context = {
        "user":User,
    }
    return render_template("app/inventory/inventory_details.html", **context)