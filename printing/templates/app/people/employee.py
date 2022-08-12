from flask import Blueprint, render_template
from flask_login import login_required, current_user
from printing.models import *

emp = Blueprint("employee", __name__, url_prefix='/employee')

@emp.route("/")
@login_required
def employee():
    employees = (
        db.session.query(People)
        .filter(People.is_employee == True)
        .filter(People.active == True)
        .all()
    )
    
    context = {"user":User, "employees":employees}
    return render_template("app/people/employee.html", **context)
