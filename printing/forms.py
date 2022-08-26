from flask_wtf import FlaskForm
import flask_login
from wtforms import (
    StringField,
    DateField,
    DecimalField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    SubmitField,
    FloatField,
    FileField,
    HiddenField,
    BooleanField
)
from wtforms.validators import InputRequired, Email, URL, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_sqlalchemy.orm import model_form
from printing import db
from printing.models import *


class User_form(FlaskForm):
    fname = StringField("First Name", [InputRequired()])
    lname = StringField("Last Name", [InputRequired()])
    address = StringField("Address", [])
    city = StringField("City", [])
    state = SelectField("State")
    zipcode = StringField("Zip Code", [])
    phone = StringField("Phone", [])
    email = StringField("Email Address", [InputRequired(), Email()])
    dob = DateField("Date of Birth", [InputRequired()])
    username = StringField("User Name", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    submit = SubmitField("Update Profile")

    def __init__(self):
        super(User_form, self).__init__()
        self.state.choices = [(c.abr, c.state) for c in States.query.all()]

class NewCustomer(FlaskForm):
    states = lambda: [(c.abr, c.state) for c in States.query.all()]
    fname = StringField("First Name", [InputRequired()])
    lname = StringField("Last Name", [InputRequired()])
    address = StringField("Address")
    city = StringField("City")
    state = SelectField("State", choices=states)
    postalcode = StringField("Postal Code")
    phone = StringField("Phone Number", [InputRequired()])
    markup_factor = FloatField("Mark Up", [InputRequired()])
    discount_factor = FloatField("Discount", [InputRequired()])
    active = BooleanField("Active", default="checked")
    submit = SubmitField("Submit")

# class Filament_form(FlaskForm):
#     vendor = lambda: [(c.id, c.name) for c in Vendors.query.all()]
#     types = lambda: [(c.id, c.type) for c in Type.query.all()]
#     name = StringField("Name (Internal Use only)", [InputRequired()])
#     color = StringField("Color", [InputRequired()])
#     priceperroll = FloatField(
#         "Cost of Roll", [NumberRange(min=0.01, max=9999, message="Enter numbers only")]
#     )
#     diameter = SelectField("Filament Diameter", [], coerce=int, choices=[(1, "1.75mm"), (2, "3mm")])
#     length_spool = SelectField("Length of Spool", [], coerce=int, 
#                                choices=[(1,"200g"),(2, "1kg"), (3, "2kg"),(4, "Other")])
#     url = StringField("Purchase Website", [])
#     purchasedate = DateField("Purchase Date")
#     picture = FileField("Picture",[])
#     vendorfk = SelectField("Vendor", [], choices=vendor)
#     typefk = SelectField("Type", [], choices=types)
#     referer = HiddenField()
#     submit = SubmitField("Submit")