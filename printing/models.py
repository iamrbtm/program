from printing import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime, os
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey


# Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    address = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(2))
    postalcode = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(150), unique=True)
    dob = db.Column(db.Date)
    avatar_filename = db.Column(db.Text)
    avatar_url = db.Column(db.String(250))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class apitoken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    token = db.Column(db.String(200))
    url = db.Column(db.String(250))


class States(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(50))
    abr = db.Column(db.String(2))

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    address = db.Column(db.String(75))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    postalcode = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    customer = db.Column(db.Boolean, default=True)
    markup_factor = db.Column(db.Float)
    discount_factor = db.Column(db.Float)
    employee = db.Column(db.Boolean)
    employee_wage = db.Column(db.Float)
    employee_design = db.Column(db.Float)
    supplier = db.Column(db.Boolean)
    company_name = db.Column(db.String(50))
    url = db.Column(db.String(250))

class Printer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    cost = db.Column(db.Float)
    cost_kW = db.Column(db.Float)
    purchase_date = db.Column(db.Date)
    
    