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
    email = db.Column(db.String(100))
    customer = db.Column(db.Boolean, default=True)
    markup_factor = db.Column(db.Float)
    discount_factor = db.Column(db.Float)
    employee = db.Column(db.Boolean)
    employee_wage = db.Column(db.Float)
    employee_design = db.Column(db.Float)
    supplier = db.Column(db.Boolean)
    company_name = db.Column(db.String(50))
    url = db.Column(db.String(250))
    active = db.Column(db.Boolean)


class Printer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    cost = db.Column(db.Float)
    purchase_date = db.Column(db.Date)
    picture = db.Column(db.Text)


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    densitygcm3 = db.Column(db.Float)
    properties = db.Column(db.Text)
    useage = db.Column(db.Text)
    diameter = db.Column(db.Float)
    extruder_temp = db.Column(db.Text)
    bed_temp = db.Column(db.Text)
    bed_adhesion = db.Column(db.Text)
    m_in_1kg_3 = db.Column(db.Float)
    m_in_1kg_175 = db.Column(db.Float)
    kW_hr = db.Column(db.Float)
    filament_rel = db.relationship("Filament", backref="type", passive_deletes=True)


class Filament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(100))
    colorhex = db.Column(db.String(20))
    priceperroll = db.Column(db.Float)
    length_spool = db.Column(db.Integer)
    diameter = db.Column(db.Float)
    url = db.Column(db.String(200))
    purchasedate = db.Column(db.Date)
    picture = db.Column(db.String(100))
    typefk = db.Column(
        db.Integer, db.ForeignKey("type.id", ondelete="CASCADE"), nullable=False
    )
    type_rel = db.relationship("Type", backref="filament")


class Printobject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(250))
    h_printtime = db.Column(db.Float)
    kg_weight = db.Column(db.Float)


class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50))
    cost = db.Column(db.Float)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50))
    customerfk = db.Column(
        db.Integer, db.ForeignKey("people.id", ondelete="CASCADE"), nullable=False
    )
    printerfk = db.Column(
        db.Integer, db.ForeignKey("printer.id", ondelete="CASCADE"), nullable=False
    )
    filamentfk = db.Column(
        db.Integer, db.ForeignKey("filament.id", ondelete="CASCADE"), nullable=False
    )
    objectfk = db.Column(
        db.Integer, db.ForeignKey("printobject.id", ondelete="CASCADE"), nullable=False
    )
    shippingfk = db.Column(
        db.Integer, db.ForeignKey("shipping.id", ondelete="CASCADE"), nullable=False
    )
    packaging = db.Column(db.Float)
    advertising = db.Column(db.Float)
    rent = db.Column(db.Float)
    overhead = db.Column(db.Float)
    extrafees = db.Column(db.Float)
    discount = db.Column(db.Float)
    people_rel = db.relationship("People", backref="project")
    printer_rel = db.relationship("Printer", backref="project")
    filament_rel = db.relationship("Filament", backref="project")
    object_rel = db.relationship("Printobject", backref="project")
    shipping_rel = db.relationship("Shipping", backref="project")
    active = db.Column(db.Boolean)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost_kW = db.Column(db.Float)
    default_markup = db.Column(db.Float)
    default_discount = db.Column(db.Float)
