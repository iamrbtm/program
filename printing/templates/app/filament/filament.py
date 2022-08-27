from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import distinct
from printing.models import *
from printing.utilities import *
from printing import filamentpics, gcode
from os.path import abspath, join, dirname

fil = Blueprint("filament", __name__, url_prefix="/filament")


@fil.route("/")
@login_required
def filament():
    filaments = db.session.query(Filament).filter(Filament.active == True).all()
    context = {"user": User, "action":1, "filaments": filaments}
    return render_template("app/filament/filament.html", **context)


@fil.route("/new", methods=['GET','POST'])
@login_required
def filament_new():
    if request.method == "POST":
        if request.files['picture'].filename == '':
            filpic = None
        else:
            filpic = filamentpics.save(request.files['picture'])
            
        newfil = Filament(
            name = request.form.get('name'),
            active = bool(request.form.get('active')),
            color = request.form.get('color'),
            colorhex = convert_color_to_hex(request.form.get('color')),
            typefk = request.form.get('typefk'),
            priceperroll = request.form.get('priceperroll'),
            length_spool = request.form.get('length_spool'),
            diameter = request.form.get('diameter'),
            url = request.form.get('url'),
            purchasedate = request.form.get('purchasedate'),
            picture = filpic,
            supplierfk = request.form.get('supplierfk')
            )
        db.session.add(newfil)
        db.session.commit()
        return redirect(url_for('filament.filament'))
    else:
        diameters = db.session.query(distinct(Type.diameter)).all()
        types = db.session.query(Type).all()
        suppliers = (
            db.session.query(People)
            .filter(People.supplier == True)
            .filter(People.active == True)
            .all()
        )
        context = {
            "user": User,
            "diameter": diameters,
            "types": types,
            "suppliers": suppliers,
        }
        return render_template("app/filament/filament_new.html", **context)


@fil.route("/type")
@login_required
def type():
    types = db.session.query(Type).filter(Type.active == True).all()

    context = {"user": User, "types": types}
    return render_template("app/filament/type.html", **context)

