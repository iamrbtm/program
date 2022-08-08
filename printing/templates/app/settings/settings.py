from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import flask_login
from sqlalchemy.orm import session
from printing.models import *
from printing import db, uploads
from printing.utilities import *
import datetime, random

stg = Blueprint("settings", __name__, url_prefix="/settings")

@stg.route("/")
@login_required
def settings():
    return redirect(url_for("dashboard.dashboard"))

#TODO: make settings page with all the options in the settings table in the db
#TODO: change route from dashboard to settings page once made