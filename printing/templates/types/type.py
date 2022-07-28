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
from printing.templates.base.base_process import *
from printing import db, photos
from printing.forms import *
from printing.utilities import *
import datetime

bp_type = Blueprint("type", __name__)


@bp_type.route("/", methods=["GET", "POST"])
@login_required
def type_main():
    form = Type_form()
    if form.validate_on_submit():
        newtype = Type()
        form.populate_obj(newtype)
        newtype.userid = current_user.id
        db.session.add(fil)
        db.session.commit()
        return redirect(url_for("type.type_main"))

    types = db.session.query(Type).all()
    context = {"user": User, "types": types, "form": form}
    return render_template("/types/type_main.html", **context)


@bp_type.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def type_edit(id):
    db_type = db.session.query(Type).filter_by(id=id).first()
    form = Type_form(obj=db_type)
    if form.validate_on_submit():
        form.populate_obj(db_type)

        db_type.userid = current_user.id

        useage = form.useage.data
        db_type.useage = useage.split(", ")

        prop = form.properties.data
        db_type.properties = prop.split(", ")

        badh = form.bed_adhesion.data
        db_type.bed_adhesion = badh.split(", ")

        db.session.add(db_type)
        db.session.commit()
        return redirect(url_for("type.type_main"))

    form.process(obj=db_type)
    form.useage.data = ", ".join(db_type.useage)
    form.properties.data = ", ".join(db_type.properties)
    form.bed_adhesion.data = ", ".join(db_type.bed_adhesion)
    context = {"user": User, "type": db_type, "form": form}
    return render_template("/types/type_edit.html", **context)
