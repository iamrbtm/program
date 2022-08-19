from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import flask_login
from sqlalchemy.orm import session
from printing.models import *
from printing import db
from printing.utilities import *
import datetime, random

stg = Blueprint("settings", __name__, url_prefix="/settings")

#TODO: make settingslog table
#TODO: Create trigger for settingslog

@stg.route("/", methods=['GET','POST'])
@login_required
def settings():
    stgs = Settings.query.first()
    
    if request.method == "POST":
        stgs.cost_kW = float(request.form.get('cost_kW'))
        stgs.default_markup = float(request.form.get('default_markup'))/100
        stgs.default_discount = float(request.form.get('default_discount'))/100
        stgs.padding_time = float(request.form.get('padding_time'))/100
        stgs.padding_filament = float(request.form.get('padding_filament'))/100
        db.session.commit()
        return redirect(url_for('settings.settings'))
    return render_template("/app/settings/settings.html", user=User, settings=stgs)


# DONE: make settings page with all the options in the settings table in the db
# DONE: change route from dashboard to settings page once made


@stg.route("/updatecostkw")
def updatecostkw():
    update_kw_oregonavg()
    return redirect(url_for('settings.settings'))
