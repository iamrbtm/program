from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from printing.models import *
from printing.forms import *

cust = Blueprint("customer", __name__, url_prefix='/customer')


@cust.route("/")
@login_required
def customer():
    customers = (
        db.session.query(People)
        .filter(People.customer == True)
        .filter(People.active == True)
        .all()
    )
    return render_template("people/customer.html", user=User, customers=customers)

@cust.route("/new", methods=['GET','POST'])
@login_required
def new_customer():
    #get default markup and discount from settings table
    stgs = Settings.query.first()
    muf = stgs.default_markup
    df = stgs.default_discount
    
    form = NewCustomer()
    form.markup_factor.default = muf
    form.discount_factor.default = df
    form.process()
    if request.method == 'POST':
        if form.is_submitted():
            print ("Form successfully submitted")
            newcust = People(
                fname = request.form.get('fname'),
                lname = request.form.get('lname'),
                address = request.form.get('address'),
                city = request.form.get('city'),
                state = request.form.get('state'),
                postalcode = request.form.get('postalcode'),
                active = request.form.get('active'),
                customer = True,
                markup_factor = request.form.get('markup_factor'),
                discount_factor = request.form.get('discount_factor')
            )
            db.session.add(newcust)
            db.session.commit()
            return redirect(url_for('customer.customer'))
        
    return render_template("people/customer_new.html", user=User, form=form)
