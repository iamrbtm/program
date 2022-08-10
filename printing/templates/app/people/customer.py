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
    return render_template("app/people/customer.html", user=User, customers=customers)


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
            markup_factor=request.form.get("markup_factor") / 100,
            discount_factor=request.form.get("discount_factor") / 100,
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


@cust.get("/zipcodelist")
def zipcodelist():
    city = request.args.get("city")
    if city:
        print("incity")
        console.log("incity")
        postalcodes = (
            db.session.query(States)
            .filter(and_(States.abr == state, States.city == city))
            .all()
        )
        zipcodes = []
        for postal in postalcodes:
            zipcodes.append(postal.zipcode)
        flush_td()
        return render_template(
            "app/people/people_zipcodelist.html", zipcodes=zipcodes
        )
    else:
        print("notincity")
        console.log("notincity")
        return ""
