from flask import Blueprint, render_template
from flask_login import login_required, current_user
from printing.models import *

vendor = Blueprint("supplier", __name__, url_prefix='/supplier')


@vendor.route("/")
@login_required
def supplier():
    suppliers = (
        db.session.query(People)
        .filter(People.supplier == True)
        .filter(People.active == True)
        .all()
    )
    return render_template("people/supplier.html", user=User, suppliers=suppliers)
