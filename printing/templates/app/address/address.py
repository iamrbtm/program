from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import flask_login
from sqlalchemy import distinct
from sqlalchemy.orm import session
from printing.models import *
from printing import db, uploads
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
    return 'something'