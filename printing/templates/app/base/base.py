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
    return render_template("app/base/base.html", user=User)


@base.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    usr = db.session.query(User).filter(User.id == flask_login.current_user.id).first()

    if request.method == "POST":
        current_user.firstname = usr.fname.data
        current_user.lastname = usr.lname.data
        current_user.username = usr.username.data
        current_user.email = usr.email.data
        current_user.address = usr.address.data
        current_user.city = usr.city.data
        current_user.state = usr.state.data
        current_user.zip = usr.zipcode.data
        current_user.city = usr.city.data
        current_user.phone = format_tel(usr.phone.data)
        current_user.dob = usr.dob.data
        db.session.commit()
        return render_template("app/base/base.html")

    # elif request.method == "GET":
        # usr.firstname.value = current_user.firstname
        # usr.lastname.value = current_user.lastname
        # usr.username.value = current_user.username
        # usr.email.value = current_user.email
        # usr.address.value = current_user.address
        # usr.city.value = current_user.city
        # usr.state.value = current_user.state
        # usr.zipcode.value = current_user.zip
        # usr.city.value = current_user.city
        # usr.phone.value = current_user.phone
        # usr.dob.value = current_user.dob

    states = db.session.query(States).all()
    return render_template(
        "app/base/profile.html", user=User, usr=usr, states=states
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
