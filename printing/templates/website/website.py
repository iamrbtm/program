from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    after_this_request,
    flash,
)
from datetime import datetime
from printing import db, mail
from printing.models import Events, Testimonials, Contact
from printing.utilities import format_tel
from sqlalchemy.sql.expression import func
from flask_mail import Message

site = Blueprint("website", __name__)

@site.route("/")
def home():
    events = db.session.query(Events).filter(Events.start_date >= datetime.now()).filter(Events.publish == 1).order_by(Events.start_date).limit(5)
    testimony = db.session.query(Testimonials).filter(Testimonials.active == True).order_by(func.random()).limit(3).all()
    return render_template("/website/index.html", events=events, testimony=testimony)

@site.route("/contactform", methods=['POST'])
def contactform():
    if request.method == "POST":
        #save to db
        data = request.form.to_dict()
        contactfrm = Contact(
            name = data['name'],
            phone = format_tel(data['phone']),
            email = data['email'],
            message = data['message']
        )
        db.session.add(contactfrm)
        db.session.commit()
        db.session.refresh(contactfrm)
        
        #send email to customer
        msg = Message(subject='Thank you for contacting us!',sender=('Dude Fish Printing', 'customer_service@dudefishprinting.com'), recipients=[data['email']])
        msg.html = render_template('/emails/contact_form_customer.html', data=data)
        mail.send(msg)
        
        #send email to admin
        msg = Message(subject='New Contact Us Form',sender=('Dude Fish Printing', 'customer_service@dudefishprinting.com'), recipients=['jeremy@dudefishprinting.com', 'damian@dudefishprinting.com'])
        msg.html = render_template('/emails/contact_form_admin.html', data=data, dt=contactfrm.dt_created)
        mail.send(msg)
        
    return redirect(url_for('website.home'))