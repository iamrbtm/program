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
def new_customer():
    # get default markup and discount from settings table
    setting = Settings.query.first()
    dmu = setting.default_markup
    dd = setting.default_discount

    if request.method == "POST":
        if form.is_submitted():
            print("Form successfully submitted")
            newcust = People(
                fname=request.form.get("fname"),
                lname=request.form.get("lname"),
                address=request.form.get("address"),
                city=request.form.get("city"),
                state=request.form.get("state"),
                postalcode=request.form.get("postalcode"),
                phone=request.form.get("phone"),
                email=request.form.get("email"),
                active=request.form.get("active"),
                customer=True,
                markup_factor=request.form.get("markup_factor"),
                discount_factor=request.form.get("discount_factor"),
            )
            db.session.add(newcust)
            db.session.commit()
            return redirect(url_for("customer.customer"))

    content = {"user": User, "dmu": dmu, "dd": dd}
    return render_template("app/people/customer_new.html", **content)


@cust.get("/statelist")
def statelist():
    city = request.args.get("city")
    if city:
        write_td(city)
        r = db.session.query(distinct(States.abr)).filter(States.city.like(city)).all()
        statelist = []
        for state in r:
            statelist.append(state._data[0])
        return render_template("app/people/people_statelist.html", statelist=statelist)
    return ""


@cust.get("/zipcodelist")
def zipcodelist():
    city = get_td()
    state = request.args.get("state")
    if city:
        if state:
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
        return ""
    return ""
