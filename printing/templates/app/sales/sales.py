from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import flask_login
from sqlalchemy import distinct
from sqlalchemy.orm import session
from printing.models import *
from printing import db, gcode
from printing.utilities import *
import datetime, random, json

sale = Blueprint("sales", __name__, url_prefix="/sales")


@sale.route("/")
@login_required
def sales():
    inventory = (
        db.session.query(Project)
        .filter(Project.customerfk == 2)
        .filter(Project.active == True)
        .all()
    )
    receiptrnum = int(str("2022" + str(random.randint(100, 999))))

    employee = f"{current_user.firstname} {current_user.lastname}"
    dt = datetime.datetime.now().strftime("%m-%d-%y %I:%M %p")
    receipt = [str(receiptrnum), dt, employee]
    context = {
        "user": User,
        "inventory": inventory,
        "receipt": receipt,
        "numdic":0
    }
    return render_template("app/sales/sales.html", **context)


def add_to_list(receipt, itemid):
    inventoryitem = db.session.query(Project).filter(Project.id == itemid).first()
    receipt = list(eval(receipt))
    res = len([ele for ele in receipt if isinstance(ele, dict)])
    cnt = res+1
    # IDEA: change quantity and price if item is already in list, ie: the customer purchases more than one of the same item.
    receipt_new = {}
    receipt_new[cnt] = {}
    receipt_new[cnt]["itemid"] = inventoryitem.id
    receipt_new[cnt]["item"] = inventoryitem.project_name
    receipt_new[cnt]["qty"] = 1
    receipt_new[cnt]["price"] = inventoryitem.sale_price

    receipt.append(receipt_new)
    return receipt


@sale.route("/add/<receipt>/<itemid>", methods=["POST"])
@login_required
def add_item(receipt, itemid):
    receipt_new = add_to_list(receipt, itemid)
    inventory = (
        db.session.query(Project)
        .filter(Project.customerfk == 2)
        .filter(Project.active == True)
        .all()
    )

    context = {
        "user": User,
        "inventory": inventory,
        "receipt": receipt_new,
    }
    return render_template("app/sales/sales.html", **context)
