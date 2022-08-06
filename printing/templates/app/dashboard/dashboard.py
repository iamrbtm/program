from flask import Blueprint, render_template
from flask_login import login_required, current_user
from printing.models import *

dash = Blueprint("dashboard", __name__, url_prefix='/dashboard')

@dash.route("/")
@login_required
def dashboard():
    return render_template("app/dashboard/dashboard.html")