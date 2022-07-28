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

base = Blueprint("base", __name__)


@base.route("/")
@base.route("/home")
@login_required
def home():
    return render_template("base/home.html", user=User)


@base.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = User_form()
    if form.is_submitted():
        current_user.firstname = form.fname.data
        current_user.lastname = form.lname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.zip = form.zipcode.data
        current_user.city = form.city.data
        current_user.phone = format_tel(form.phone.data)
        current_user.dob = form.dob.data
        db.session.commit()
        return render_template("base/home.html")

    elif request.method == "GET":
        form.fname.data = current_user.firstname
        form.lname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.zipcode.data = current_user.zip
        form.city.data = current_user.city
        form.phone.data = current_user.phone
        form.dob.data = current_user.dob

    states = db.session.query(States).all()
    usr = db.session.query(User).filter(User.id == flask_login.current_user.id).first()
    return render_template(
        "base/profile.html", user=User, usr=usr, states=states, form=form
    )

@base.route("/stateimport")
@login_required
def stateimport():
    populate_states()
    return redirect(url_for("base.home"))


@base.route("/typeimport")
@login_required
def typeimport():
    populate_types()
    return redirect(url_for("base.home"))