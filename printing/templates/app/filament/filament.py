from flask import Blueprint, render_template
from flask_login import login_required, current_user
from printing.models import *

fil = Blueprint("filament", __name__, url_prefix="/filament")


@fil.route("/")
@login_required
def filament():
    filaments = db.session.query(Filament).filter(Filament.active == True).all()
    context = {"user": User, "filaments": filaments}
    return render_template("app/filament/filament.html", **context)


@fil.route("/new")
@login_required
def filament_new():
    context = {"user": User}
    return render_template("app/filament/filament_new.html", **context)


@fil.route("/type")
@login_required
def type():
    types = db.session.query(Type).filter(Type.active == True).all()

    context = {"user": User, "types": types}
    return render_template("app/filament/type.html", **context)
