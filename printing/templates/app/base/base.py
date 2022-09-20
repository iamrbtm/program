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
from printing import db, photos, avatar
from printing.forms import *
from printing.utilities import *
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from printing.time_estimate import *

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
        if request.form.get("where") == "picture":
            filename = avatar.save(request.files['picture'])
            path = '/app/img/avatars'
            
            # Save to db
            current_user.avatar_filename = filename
            current_user.avatar_url = os.path.join(path,filename)
        
        elif request.form.get("where") == "contact":
            current_user.firstname = request.form.get("firstname")
            current_user.lastname = request.form.get("lastname")
            current_user.address = request.form.get("address")
            current_user.city = request.form.get("city")
            current_user.state = request.form.get("state")
            current_user.postalcode = request.form.get("postalcode")
            current_user.phone = format_tel(request.form.get("phone"))
            current_user.dob = request.form.get("dob")

        elif request.form.get("where") == "user":
            current_user.username = request.form.get('username')
            current_user.email = request.form.get('email')

        db.session.commit()
        flash("Information Saved")
        return redirect(url_for("base.profile"))

    states = db.session.query(States).all()
    return render_template("app/base/profile.html", user=User, states=states)


@base.route("/stateimport")
@login_required
def stateimport():
    populate_states()
    return redirect(url_for("base.home"))


@base.route("/typeimport")
@login_required
def typeimport():
    populate_types()
    return redirect(url_for("dashboard.dashboard"))

@base.route("/dbmaint")
@login_required
def dbmaint():
    db_maintance()
    return redirect(url_for("dashboard.dashboard"))

@base.route("/evat", methods=["GET", "POST"])
@login_required
def evat():
    if request.method == "POST":
        act = get_sec(request.form.get('actual'))
        calculate_est_vs_act_time(request.form.get('file'), act)
        return redirect(url_for('dashboard.dashboard'))
    
    files = Printobject.query.all()
    return render_template("app/base/est_vs_act_time.html", user=User, files=files)
    
@base.route("/test")
@login_required
def test():
    t = timeEstimate()
    t.EstimatePrintTime()
    print(t.estimatedCompletionDate)
    return redirect(url_for("dashboard.dashboard"))