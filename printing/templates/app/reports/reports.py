from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from printing.models import *
from printing import db
from sqlalchemy import extract, func
from datetime import datetime


rep = Blueprint("report", __name__, url_prefix="/report")


@rep.route("/")
@login_required
def report():
    return render_template("app/reports/reports.html", user=User)


@rep.route("/low_inventory_report")
@login_required
def low_inventory():
    items = db.session.query(Project).all()

    current_inv_sum = Project.query.with_entities(func.sum(Project.current_quantity).label("CurrentInventory")).first()
    threshold_sum = Project.query.with_entities(func.sum(Project.threshold).label("Threshold")).first()

    context = {"items": items, "curinv": int(current_inv_sum[0]), "threshold": int(threshold_sum[0])}

    return render_template("app/reports/low_inventory_pdf.html", **context)


@rep.route("/threshold", methods=["GET", "POST"])
@login_required
def threshold():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
    catagory = db.session.query(distinct(Project.catagory), Project.catagory).all()
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active).all()
    return render_template("app/reports/threshold.html", inventory=inventory, catagory=catagory)


@rep.route("/print_time_report")
@login_required
def print_time_report():
    items = db.session.query(Project).all()

    printtimes = []
    totalprinttime = 0
    for item in items:
        printtime = 0
        for obj in item.objectfk:
            ptime = Printobject.query.filter(Printobject.id == obj).first().h_printtime
            totaltime = printtime + ptime
        printtime = ((item.threshold - item.current_quantity) / item.qtyperprint) * totaltime
        this = {}
        this["printtime"] = printtime
        this["id"] = item.id
        printtimes.append(this)
        totalprinttime = totalprinttime + printtime

    context = {"printtimes": printtimes, "items": items, "totalprinttime": totalprinttime}

    return render_template("app/reports/print_time_report.html", **context)


@rep.route("/profit_split_pre")
@login_required
def split_profit_pre():
    context = {"user": User}
    return render_template("/app/reports/profit_split_pre.html", **context)


@rep.route("/profit_split", methods=["POST"])
@login_required
def split_profit():
    if request.method == "POST":
        start = datetime.strptime(request.form.get("start"),"%Y-%m-%d")
        end = datetime.strptime(request.form.get("end"),"%Y-%m-%d")
        start_date = datetime(start.year, start.month, start.day)
        end_date = datetime(end.year, end.month, end.day)

        list_of_items_sold = (
            db.session.query(Sales_lineitems)
            .filter(Sales_lineitems.date_created.between(start_date, end_date))
            .all()
        )
    return 1