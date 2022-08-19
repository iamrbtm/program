from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from printing.models import *
from printing.forms import *
from printing.utilities import *
import requests
from sqlalchemy import distinct, and_, or_


cust = Blueprint("customer", __name__, url_prefix="/customer")


@cust.route("/")
@login_required
def customer():
    customers = (
        db.session.query(People)
        .filter(People.customer == True)
        .filter(People.active == True)
        .all()
    )
    
    context = {
        "action":1,
        "user":User, 
        "customers":customers
    }
    return render_template("app/people/customer_list.html", **context)

@cust.route("/new", methods=["GET", "POST"])
@login_required
def customer_new():
    # get default markup and discount from settings table
    setting = Settings.query.first()
    dmu = setting.default_markup
    dd = setting.default_discount

    if request.method == "POST":
        address = request.form.get("address")
        address2 = request.form.get("address2")
        company = request.form.get("company")
        city = request.form.get("city")
        state = request.form.get("state")
        postalcode = request.form.get("postalcode")

        # Create New Customer
        newcust = People(
            fname=request.form.get("fname"),
            lname=request.form.get("lname"),
            phone=format_tel(request.form.get("phone")),
            email=request.form.get("email"),
            active=True,
            customer=True,
            markup_factor=float(request.form.get("markup_factor")) / 100,
            discount_factor=float(request.form.get("discount_factor"))   / 100,
        )
        db.session.add(newcust)
        db.session.commit()
        db.session.refresh(newcust)

        # Create New Address
        newaddy = Address(
            fname=newcust.fname,
            lname=newcust.lname,
            company=company,
            address=address,
            address2=address2,
            city=city,
            state=state,
            postalcode=postalcode,
            peoplefk=newcust.id,
            type="New Address",
        )
        db.session.add(newaddy)
        db.session.commit()
        db.session.refresh(newaddy)

        # Put address.id into new cust mail and shipping address fk
        newcust.main_addressfk = (newaddy.id,)
        newcust.ship_addressfk = newaddy.id
        db.session.add(newaddy)
        db.session.commit()

        return redirect(url_for("customer.customer"))

    states = db.session.query(distinct(States.abr), States.abr, States.state).all()

    content = {"user": User, "dmu": dmu, "dd": dd, "states": states}
    return render_template("app/people/customer_new.html", **content)

@cust.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def customer_edit(id):
    customer = db.session.query(People).filter(People.id == id).first()
    states = db.session.query(distinct(States.abr),States.abr, States.state).all()
    if request.method == "POST":
        customer.fname = request.form.get('fname')
        customer.lname = request.form.get('lname')
        customer.company_name = request.form.get('company')
        customer.active = bool(request.form.get('active'))
        customer.mainaddress_rel.address = request.form.get('address')
        customer.mainaddress_rel.address2 = request.form.get('address2')
        customer.mainaddress_rel.city = request.form.get('city')
        customer.mainaddress_rel.state = request.form.get('state')
        customer.mainaddress_rel.postalcode = request.form.get('postalcode')
        customer.email = request.form.get('email')
        customer.phone = format_tel(request.form.get('phone'))
        customer.markup_factor = float(float(request.form.get('markup_factor')) / 100)
        customer.discount_factor = float(float(request.form.get('discount_factor')) / 100)
        db.session.commit()
        return redirect(url_for('customer.customer'))
    return render_template('app/people/customer_edit.html', user=User, customer=customer, states=states)

@cust.route("/details/<id>", methods=["GET"])
@login_required
def customer_details(id):
    get_log_lat(id)
    customer = db.session.query(People).filter(People.id == id).first()
    states = db.session.query(distinct(States.abr),States.abr, States.state).all()
    history = db.session.query(Project).filter(Project.customerfk == id).all()
    addresses = db.session.query(Address).filter(Address.peoplefk == id).all()

    context = {
        'user':User,
        'customer':customer,
        'history':history,
        'states':states,
        'addresses':addresses,
        'action':1
    }
    return render_template('app/people/customer_details.html', **context)

@cust.route("/archive/<id>", methods=["GET"])
@login_required
def customer_archive(id):
    cust = db.session.query(People).filter(People.id == id).first()
    cust.customer = 0
    db.session.commit()
    db_maintance()
    return redirect(url_for('customer.customer'))