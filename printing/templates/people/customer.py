from flask import Blueprint, render_template
from flask_login import login_required, current_user
from printing.models import *

cust = Blueprint("customer", __name__, url_prefix='/customer')


@cust.route("/")
@login_required
def customer():
    customers = (
        db.session.query(People)
        .filter(People.customer == True)
        .filter(People.active == True)
        .all()
    )
    return render_template("people/customer.html", user=User, customers=customers)
