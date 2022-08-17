from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import flask_login
from sqlalchemy import distinct
from sqlalchemy.orm import session
from printing.models import *
from printing import db
from printing.utilities import *
import datetime, random

addy = Blueprint("address", __name__, url_prefix="/address")

@addy.route("/")
@login_required
def address():
    return redirect(url_for("customer.customer"))

@addy.route("/new", methods=['POST','GET'])
@login_required
def address_new():
    if request.method == "POST":
        from geopy.geocoders import Nominatim
        
        addy=f"{request.form.get('address')} {request.form.get('city')}, {request.form.get('state')} {request.form.get('postalcode')}"
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(addy)
        newaddress = Address(
            type = request.form.get('type'),
            fname = request.form.get('fname'),
            lname = request.form.get('lname'),
            company = request.form.get('company'),
            address = request.form.get('address'),
            address2 = request.form.get('address2'),
            city = request.form.get('city'),
            state = request.form.get('state'),
            postalcode = request.form.get('postalcode'),
            peoplefk = request.form.get('peoplefk'),
            longitude = location.longitude,
            latitudes = location.latitude
        )
        db.session.add(newaddress)
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    
    people = db.session.query(People).filter(People.active == True).order_by(People.lname).all()
    types = db.session.query(distinct(Address.type), Address.type).all()
    
    context = {
        'user':User,
        'people':people,
        'types':types
    }
    return render_template('/app/address/address_new.html', **context)