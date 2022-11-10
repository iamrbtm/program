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

    context = {"user": User, "inventory": inventory, "sales": newsale, "new":True}
    return render_template("app/sales/sales.html", **context)

@sale.route("/active/<ordernum>", methods=["GET","POST"])
@login_required
def sales_active(ordernum):
    #Get all inventory
    inventory = (
        db.session.query(Project)
        .filter(Project.customerfk == 2)
        .filter(Project.active == True)
        .group_by(Project.catagory, Project.project_name)
        .all()
    )
    sales = db.session.query(Sales).filter(Sales.)
    items = 

    



    
    context = {"user": User, "inventory": inventory, "sales": sales, "new":False, "items":items}
    return render_template("app/sales/sales.html", **context)
    

@sale.route("/add/<ordernum>/<itemid>", methods=["POST"])
@login_required
def add_item(ordernum, itemid):
    def get_price(projectfk):
        price = db.session.query(Project),filter(Project.id == projectfk).first().sale_price
        return price
    
    def getqty(ordernum,itemid):
        item = db.session.query(Sales_lineitems).filter(Sales_lineitems.ordernumfk == ordernum).filter(Sales_lineitems.projectfk == itemid).first()
        if len(item) == 0:
            qty = 1
        else:
            qty = len(item) + 1
        return qty
    
    def add_to_db(ordernum, itemid, qty):
        newitem = Sales_lineitems(
            projectfk = itemid,
            price = get_price(itemid),
            ordernumfk = ordernum,
            qty = qty
        )
        db.session.add(newitem)
        db.session.commit()
        
    def update_db(ordernum, itemid, qty):
        item = db.session.query(Sales_lineitems).filter(Sales_lineitems.ordernumfk == ordernum).filter(Sales_lineitems.projectfk == itemid).first()
        item.qty = qty
        item.price = get_price(itemid) * qty
        db.session.commit()
    
    def update_total(ordernum):
        total = db.session.query(func.sum(Sales_lineitems.price)).filter(Sales_lineitems.ordernumfk == ordernum).scalar()
        
        sale = db.session.query(Sales).filter(Sales.ordernum == ordernum).first()
        
        sale.total = total
        db.session.commit()
    
    
    qty = getqty(ordernum, itemid),

    
    if qty == 1:
        add_to_db(ordernum, itemid, qty)
    else:
        update_db(ordernum, itemid, qty)
    
    update_total()
    
    return redirect(url_for("sales.sales", ordernum = ordernum))