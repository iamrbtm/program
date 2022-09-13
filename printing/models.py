import datetime
import os

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

from printing import db


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
    zipcode = db.Column(db.Integer)
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    abr = db.Column(db.String(2))


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    main_addressfk = db.Column(db.Integer, db.ForeignKey("address.id"))
    ship_addressfk = db.Column(db.Integer, db.ForeignKey("address.id"))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    customer = db.Column(db.Boolean, default=True)
    markup_factor = db.Column(db.Float)
    discount_factor = db.Column(db.Float)
    is_employee = db.Column(db.Boolean)
    employee_wage = db.Column(db.Float)
    employee_design = db.Column(db.Float)
    supplier = db.Column(db.Boolean)
    company_name = db.Column(db.String(50))
    url = db.Column(db.String(250))
    active = db.Column(db.Boolean)
    mainaddress_rel = db.relationship(
        "Address", back_populates="main_address", foreign_keys=[main_addressfk]
    )
    shippingaddress_rel = db.relationship(
        "Address", back_populates="shipping_address", foreign_keys=[ship_addressfk]
    )
    employee = db.relationship(
        "Project", foreign_keys="Project.employeefk", back_populates="employee_rel"
    )
    customers = db.relationship(
        "Project", foreign_keys="Project.customerfk", back_populates="customer_rel"
    )
    address = db.relationship(
        "Address", foreign_keys="Address.peoplefk", back_populates="people_rel"
    )
    filament = db.relationship(
        "Filament", foreign_keys="Filament.supplierfk", back_populates="supplier_rel"
    )


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    company = db.Column(db.String(50))
    address = db.Column(db.String(75))
    address2 = db.Column(db.String(75))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    postalcode = db.Column(db.String(20))
    longitude = db.Column(db.DECIMAL(11, 8))
    latitudes = db.Column(db.DECIMAL(10, 8))
    peoplefk = db.Column(db.Integer, db.ForeignKey("people.id"))
    shipping_address = db.relationship(
        "People",
        foreign_keys="People.ship_addressfk",
        back_populates="shippingaddress_rel",
    )
    main_address = db.relationship(
        "People", foreign_keys="People.main_addressfk", back_populates="mainaddress_rel"
    )
    people_rel = db.relationship(
        "People", back_populates="address", foreign_keys=[peoplefk]
    )


class Printer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    cost = db.Column(db.Float)
    purchase_date = db.Column(db.Date)
    picture = db.Column(db.Text)
    correction_percentage = db.Column(db.Float)
    active = db.Column(db.Boolean)


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
    active = db.Column(db.Boolean, default=True)
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
    supplierfk = db.Column(db.Integer, db.ForeignKey("people.id"))
    active = db.Column(db.Boolean)
    type_rel = db.relationship("Type", backref="filament", overlaps="filament_rel,type")
    supplier_rel = db.relationship(
        "People", back_populates="filament", foreign_keys=[supplierfk]
    )


class Printobject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(250))
    h_printtime = db.Column(db.Float)
    kg_weight = db.Column(db.Float)
    qtyperprint = db.Column(db.Integer)
    projectid = db.Column(db.Integer, db.ForeignKey("project.id"))
    project_rel = db.relationship("Project", backref="printobject", foreign_keys=[projectid])


class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50))
    cost = db.Column(db.Float)
    service = db.Column(db.Text)


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
    shippingfk = db.Column(
        db.Integer, db.ForeignKey("shipping.id", ondelete="CASCADE"), nullable=False
    )
    employeefk = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)
    objectfk = db.Column(db.JSON)
    packaging = db.Column(db.Float)
    advertising = db.Column(db.Float)
    rent = db.Column(db.Float)
    overhead = db.Column(db.Float)
    extrafees = db.Column(db.Float)
    discount = db.Column(db.Float)
    tracking = db.Column(db.Text)
    ordernum = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    sale_price = db.Column(db.Float)
    cost = db.Column(db.Float)
    current_quantity = db.Column(db.Integer)
    threshold = db.Column(db.Integer)
    qtyperprint = db.Column(db.Integer)
    catagory = db.Column(db.String(50))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    employee_rel = db.relationship(
        "People", back_populates="employee", foreign_keys=[employeefk]
    )
    customer_rel = db.relationship(
        "People", back_populates="customers", foreign_keys=[customerfk]
    )
    printer_rel = db.relationship("Printer", backref="project")
    filament_rel = db.relationship("Filament", backref="project")
    shipping_rel = db.relationship("Shipping", backref="project")


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost_kW = db.Column(db.Float)
    default_markup = db.Column(db.Float)
    default_discount = db.Column(db.Float)
    padding_time = db.Column(db.Float)
    padding_filament = db.Column(db.Float)


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    location = db.Column(db.String(100))
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    mapsurl = db.Column(db.Text)
    publish = db.Column(db.Boolean, default=True)


class Testimonials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    testimonial = db.Column(db.String(200))
    fulltext = db.Column(db.Text)
    active = db.Column(db.Boolean)
    date_created = db.Column(db.Date, default=func.now())


class Adjustment_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adjustment = db.Column(db.Integer)
    description = db.Column(db.Text)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    projectfk = db.Column(db.Integer, db.ForeignKey("project.id"))
    project_rel = db.relationship("Project", backref="adjustment_log")


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employeefk = db.Column(db.Integer, db.ForeignKey("people.id"))
    customerfk = db.Column(db.Integer, db.ForeignKey("people.id"))
    ordernum = db.Column(db.Integer)
    date_time_created = db.Column(db.DateTime)
    total = db.Column(db.Float)
    sq_idempotency_key = db.Column(db.String(50))
    customer_rel = db.relationship("People", backref="sales", foreign_keys=[customerfk])


class Sales_lineitems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectfk = db.Column(db.Integer, db.ForeignKey("project.id"))
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)
    ordernumfk = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    project_rel = db.relationship("Project", backref="sales", foreign_keys=[projectfk])


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)
    dt_created = db.Column(db.DateTime(timezone=True), default=func.now())


class Estimate_vs_actual_time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    printerfk = db.Column(db.Integer, db.ForeignKey("printer.id"))
    estimated_time_in_s = db.Column(db.Integer)
    actual_time_in_s = db.Column(db.Integer)
    dt_created = db.Column(db.DateTime(timezone=True), default=func.now())
