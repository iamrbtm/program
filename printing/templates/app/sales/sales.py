import random

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from flask_mail import Message

from printing import mail
from printing.utilities import *

sale = Blueprint("sales", __name__, url_prefix="/sales")


# IDEA: use picture of the object rather than buttons on the pos system
# TODO: working on the emails that go to customers and admin when an order is placed
# TODO: working on setting up the square button to make purchases - NEED HELP


def update_total(ordernum):
    total = (
        db.session.query(func.sum(Sales_lineitems.price))
        .filter(Sales_lineitems.ordernumfk == ordernum)
        .scalar()
    )

    sale = db.session.query(Sales).filter(Sales.ordernum == ordernum).first()

    sale.total = total
    db.session.commit()


def update_balance(ordernum):
    total = (
        db.session.query(func.sum(Sales_lineitems.price))
        .filter(Sales_lineitems.ordernumfk == ordernum)
        .scalar()
    )

    sale = db.session.query(Sales).filter(Sales.ordernum == ordernum).first()

    pmts = sale.cash + sale.check + sale.card + sale.other

    sale.balance = total - pmts
    db.session.commit()


@sale.route("/", methods=["GET", "POST"])
@login_required
def sales():
    return render_template("app/sales/sales_dashboard.html")


@sale.route("/new", methods=["GET", "POST"])
@login_required
def sales_new():
    # Get all inventory
    inventory = (
        db.session.query(Project)
        .filter(Project.customerfk == 2)
        .filter(Project.active == True)
        .group_by(Project.catagory, Project.project_name)
        .all()
    )
    # Generate a new order number and see if it is already in the database
    exists = True
    while exists:
        ordernumber = int(str("2022" + str(random.randint(100, 9999))))
        exists = db.session.query(
            db.exists().where(Sales.ordernum == ordernumber)
        ).scalar()

    newsale = Sales(
        employeefk=1,
        customerfk=23,
        ordernum=ordernumber,
        date_time_created=datetime.datetime.now(),
        total=0,
    )
    db.session.add(newsale)
    db.session.commit()
    db.session.refresh(newsale)

    context = {"user": User, "inventory": inventory, "sales": newsale, "new": True}
    return render_template("app/sales/sales.html", **context)


@sale.route("/active/<ordernum>", methods=["GET", "POST"])
@login_required
def sales_active(ordernum):
    # Get all inventory
    inventory = (
        db.session.query(Project)
        .filter(Project.customerfk == 2)
        .filter(Project.active == True)
        .group_by(Project.catagory, Project.project_name)
        .all()
    )
    sales = db.session.query(Sales).filter(Sales.ordernum == ordernum).first()
    items = (
        db.session.query(Sales_lineitems)
        .filter(Sales_lineitems.ordernumfk == ordernum)
        .all()
    )
    update_balance(ordernum)

    context = {
        "user": User,
        "inventory": inventory,
        "sales": sales,
        "new": False,
        "items": items,
    }
    return render_template("app/sales/sales.html", **context)


@sale.route("/add/<ordernum>/<itemid>", methods=["POST"])
@login_required
def add_item(ordernum, itemid):
    def get_price(projectfk):
        proj = db.session.query(Project).filter(Project.id == projectfk).first()
        return float(proj.sale_price)

    def getqty(ordernum, itemid):
        item = (
            db.session.query(Sales_lineitems)
            .filter(Sales_lineitems.ordernumfk == ordernum)
            .filter(Sales_lineitems.projectfk == itemid)
            .first()
        )
        if item == None:
            qty = 1
        else:
            qty = item.qty + 1
        return qty

    def add_to_db(ordernum, itemid, qty):
        newitem = Sales_lineitems(
            projectfk=itemid, price=get_price(itemid), ordernumfk=ordernum, qty=qty
        )
        db.session.add(newitem)
        db.session.commit()

    def update_db(ordernum, itemid, qty):
        item = (
            db.session.query(Sales_lineitems)
            .filter(Sales_lineitems.ordernumfk == ordernum)
            .filter(Sales_lineitems.projectfk == itemid)
            .first()
        )
        item.qty = qty
        item.price = get_price(itemid) * qty
        db.session.commit()

    qty = getqty(ordernum, itemid)

    if qty == 1:
        add_to_db(ordernum, itemid, qty)
    else:
        update_db(ordernum, itemid, qty)

    update_total(ordernum)

    return redirect(url_for("sales.sales_active", ordernum=ordernum))


@sale.route("/finalize/split/<ordernum>", methods=["GET", "POST"])
@login_required
def split(ordernum):
    sale = db.session.query(Sales).filter(Sales.ordernum == ordernum).first()
    if request.method == "POST":
        sale.cash = float(request.form.get('cashamount'))
        sale.check = float(request.form.get('checkamount'))
        if sale.check != 0:
            sale.checknum = int(request.form.get('checknum'))
        sale.account = float(request.form.get('accountamount'))
        sale.card = float(request.form.get('cardamount'))
        sale.other = float(request.form.get('otheramount'))
        db.session.commit()
        return redirect(url_for("sales.sales_active", ordernum=ordernum))

    context = {"user": User, "sale": sale}
    return render_template("app/sales/split.html", **context)


@sale.route("/finalize/<ordernum>", methods=["POST"])
@login_required
def sales_finalize(ordernum):
    def cash(sale):
        if sale.cash == 0:
            sale.cash = float(sale.balance)
        else:
            sale.cash = sale.cash + float(sale.balance)
        db.session.commit()

    def account(sale):
        if sale.account == 0:
            sale.account = float(sale.balance)
        else:
            sale.account = sale.account + float(sale.balance)
        db.session.commit()

    def card(sale):
        if sale.card == 0:
            sale.card = float(sale.balance)
        else:
            sale.card = sale.card + float(sale.balance)
        db.session.commit()

    def other(sale):
        if sale.other == 0:
            sale.other = float(sale.balance)
        else:
            sale.other = sale.other + float(sale.balance)
        db.session.commit()

    def send_email(sale, subject, template_name='receipt_customer.html'):
        items = db.session.query(Sales_lineitems).filter(Sales_lineitems.ordernumfk == sale.ordernum).all()
        total = sale.total

        ordernum = sale.ordernum

        msg = Message(
            subject,
            sender=("Dudefish Printing", "customer_service@dudefishprinting.com"),
            recipients=sale.customer_rel.email,
        )
        msg.html = render_template(f"emails/sales/{template_name}", items=items, total=total)
        mail.send(msg)

    if request.method == "POST":
        sale = db.session.query(Sales).filter(Sales.ordernum == ordernum).first()

        if request.form["submitbtn"] == "Cash":
            cash(sale)
        elif request.form["submitbtn"] == "Account":
            account(sale)
        elif request.form["submitbtn"] == "Check":
            return redirect(url_for("sales.split", ordernum=ordernum))
        elif request.form["submitbtn"] == "Card":
            card(sale)
        elif request.form["submitbtn"] == "Other":
            other(sale)
        elif request.form["submitbtn"] == "Split":
            return redirect(url_for("sales.split", ordernum=ordernum))

    update_balance(ordernum)

    if sale.balance == 0:
        # FIXME: SEND EMAIL RECEIPT ~ send_email(sale, "Receipt from Dudefish Printing")
        return redirect(url_for("sales.sales"))
    else:
        return redirect(url_for("sales.sales_active", ordernum=ordernum))
