import datetime
import json
import os
import random
import secrets

import flask_login
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_mail import Mail, Message
from printing import db, gcode, mail
from printing.models import *
from printing.utilities import *
from sqlalchemy import distinct
from sqlalchemy.orm import session

sale = Blueprint("sales", __name__, url_prefix="/sales")

# TODO: working on the emails that go to customers and admin when an order is placed
# TODO: working on setting up the square button to make purchases - NEED HELP

@sale.route("/", methods=["GET","POST"])
@login_required
def sales():
    return render_template("app/sales/sales_dashboard.html")

@sale.route("/new", methods=["GET","POST"])
@login_required
def sales_new():
    #Get all inventory
    inventory = (
        db.session.query(Project)
        .filter(Project.customerfk == 2)
        .filter(Project.active == True)
        .group_by(Project.catagory, Project.project_name)
        .all()
    )
    #Generate a new order number and see if it is already in the database 
    exists = True
    while exists == True:
        ordernumber = int(str("2022" + str(random.randint(100, 9999))))
        exists = db.session.query(
            db.exists().where(Sales.ordernum == ordernumber)
        ).scalar()

    newsale = Sales(
        employeefk = 1,
        customerfk = 23,
        ordernum = ordernumber,
        date_time_created = datetime.datetime.now(),
        total = 0,
    )
    db.session.add(newsale)
    db.session.commit()
    db.session.refresh(newsale)

    context = {"user": User, "inventory": inventory, "sales": newsale}
    return render_template("app/sales/sales.html", **context)


@sale.route("/add/<ordernum>/<itemid>", methods=["POST"])
@login_required
def add_item(ordernum, itemid):
    
    
    def get_price(projectfk):
        pass
    
    projectfk = itemid,
    qty = 1,
    price = get_price(itemid)
    ordernumfk = ordernum
    
    return redirect(url_for("sales.sales"))