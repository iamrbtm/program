from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import flask_login
from flask_mail import Mail, Message
from sqlalchemy import distinct
from sqlalchemy.orm import session
from printing.models import *
from printing import db, gcode, mail
from printing.utilities import *
import datetime, random, json, secrets, os

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
    exists = True
    while exists == True:
        receiptrnum = int(str("2022" + str(random.randint(100, 999))))
        exists = db.session.query(
            db.exists().where(Sales.ordernum == receiptrnum)
        ).scalar()

    employee = f"{current_user.firstname} {current_user.lastname}"
    dt = datetime.datetime.now().strftime("%m-%d-%y %I:%M %p")
    receipt = [{"data": {"receiptnum": receiptrnum, "dt": dt, "employee": employee}}]
    context = {"user": User, "inventory": inventory, "receipt": receipt, "numdic": 0}
    return render_template("app/sales/sales.html", **context)


def add_to_list(receipt, itemid):
    inventoryitem = db.session.query(Project).filter(Project.id == itemid).first()
    receipt = list(eval(receipt))
    cnt = len([ele for ele in receipt if isinstance(ele, dict)])
    # WORKING: change quantity and price if item is already in list, ie: the customer purchases more than one of the same item.

    i = 1
    receipt_new = {}
    receipt_new[cnt] = {}
    receipt_new[cnt]["lineitemnum"] = cnt
    receipt_new[cnt]["itemid"] = inventoryitem.id
    receipt_new[cnt]["item"] = inventoryitem.project_name
    receipt_new[cnt]["qty"] = 1
    receipt_new[cnt]["price"] = inventoryitem.sale_price

    receipt.append(receipt_new)
    return receipt


def see_if_dup(receipt, itemid):
    results = False
    receipt = list(eval(receipt))
    i = 1
    for dic in receipt:
        if dic.get("data") == None:
            if int(itemid) == int(dic[i]["itemid"]):
                price = (
                    db.session.query(Project)
                    .filter(Project.id == itemid)
                    .first()
                    .sale_price
                )
                qty = dic[i]["qty"]
                dic[i]["qty"] = qty + 1
                dic[i]["price"] = price * (qty + 1)
                i = i + 1
                results = True
            else:
                i = i + 1
    return results, receipt


def send_email(receipt, emailaddy):
    receipt = list(eval(receipt))
    total = calc_total(receipt)

    ordernum = receipt[0]["data"]["receiptnum"]

    msg = Message(
        "testing",
        sender=("Dudefish Printing", "customer_service@dudefishprinting.com"),
        recipients=[emailaddy],
    )
    msg.html = render_template(
        "/emails/sales/receipt_customer.html", receipt=receipt, total=total
    )
    mail.send(msg)


def add_to_db(receipt, customerid, idempotency_key):
    receipt = list(eval(receipt))

    employee = receipt[0]["data"]["employee"].split()
    employeeid = (
        db.session.query(User)
        .filter(User.firstname == employee[0])
        .filter(User.lastname == employee[1])
        .first()
        .id
    )

    ordernum = receipt[0]["data"]["receiptnum"]

    dt = datetime.datetime.strptime(receipt[0]["data"]["dt"], "%m-%d-%y %I:%M %p")

    newSale = Sales(
        employeefk=employeeid,
        customerfk=2,
        ordernum=ordernum,
        date_time_created=dt,
        total=calc_total(receipt),
        sq_idempotency_key=idempotency_key,
    )
    db.session.add(newSale)
    db.session.commit()

    i = 1
    for dic in receipt:
        if dic.get("data") == None:
            newline = Sales_lineitems(
                projectfk=dic[i]["itemid"],
                qty=dic[i]["qty"],
                price=dic[i]["price"],
                ordernumfk=ordernum,
            )
            db.session.add(newline)
            db.session.commit()
            i = i + 1


def cash(receipt, customerid=2):
    add_to_db(receipt, customerid, idempotency_key="CASH")
    emailaddy = db.session.query(People).filter(People.id == 1).first().email
    if emailaddy:
        send_email(receipt, emailaddy)


def card(receipt, customerid, token):
    from square.client import Client

    client = Client(
        access_token=os.getenv("square_sb_access_token"), environment="sandbox"
    )

    receipt = list(eval(receipt))
    customer = db.session.query(People).filter(People.id == customerid).first()

    sq_idempotency_key = secrets.token_hex(15).upper()
    sq_amount_money = int(calc_total(receipt) * 100)
    sq_reference_id = int(receipt[0]["data"]["receiptnum"])
    sq_buyer_email_address = customer.email
    sq_note = (
        str(receipt[0]["data"]["receiptnum"]) + "/" + str(receipt[0]["data"]["dt"])
    )

    body = {}
    body["amount_money"] = {}
    body["amount_money"]["amount"] = int(sq_amount_money)
    body["amount_money"]["currency"] = "USD"
    body["autocomplete"] = True
    body["idempotency_key"] = f"{sq_idempotency_key}"
    body["reference_id"] = f"{sq_reference_id}"
    body["buyer_email_address"] = f"{sq_buyer_email_address}"
    body["note"] = f"{sq_note}"
    body["source_id"] = f"{token}"
    
    result = client.payments.create_payment(body)

    if result.is_success():
        print(result.body)
    elif result.is_error():
        print(result.errors)


def account():
    pass


def add_customer(name, email, postalcode):
    name = name.split()
    city, state = get_city_state_from_postalcoide(int(postalcode))
    newcust = People(
        fname=name[0],
        lname=name[1],
        email=email,
    )
    db.session.add(newcust)
    db.session.commit()
    db.session.refresh(newcust)

    newaddy = Address(
        type="Home",
        fname=name[0],
        lname=name[1],
        peoplefk=newcust.id,
        postalcode=postalcode,
        state=state,
        city=city,
    )
    db.session.add(newaddy)
    db.session.commit()
    db.session.refresh(newaddy)

    newcust.main_address = newaddy.id
    db.session.commit()

    return newcust.id

@sale.post("/process-payment")
def create_payment():
    logging.info("Creating payment")
    # Charge the customer's card
    create_payment_response = client.payments.create_payment(
        body={
            "source_id": payment.token,
            "idempotency_key": str(uuid.uuid4()),
            "amount_money": {
                "amount": 100,  # $1.00 charge
                "currency": ACCOUNT_CURRENCY,
            },
        }
    )

    logging.info("Payment created")
    if create_payment_response.is_success():
        return create_payment_response.body
    elif create_payment_response.is_error():
        return create_payment_response


@sale.route("/finalize/<receipt>", methods=["POST"])
@login_required
def finalize_transaction(receipt, token=""):
    if request.form.get("cashbtn"):
        cash(receipt)
    elif request.form.get("cardbtn"):
        name = request.form.get("name")
        email = request.form.get("email")
        postalcode = request.form.get("postalcode")

        customer = add_customer(name, email, postalcode)
        card(receipt, customer, token)
    elif request.form.get("accountbtn"):
        account()

    return redirect(url_for("sales.sales"))


def calc_total(receipt_new):
    i = 1
    sum = 0.0
    for dic in receipt_new:
        if dic.get("data") == None:
            sum = sum + float(dic[i]["price"])
            i = i + 1
    return sum


@sale.route("/add/<receipt>/<itemid>", methods=["POST"])
@login_required
def add_item(receipt, itemid):
    results, receipt_new = see_if_dup(receipt, itemid)
    if not results:
        receipt_new = add_to_list(receipt, itemid)

    total = calc_total(receipt_new)

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
        "total": total,
    }
    return render_template("app/sales/sales.html", **context)
