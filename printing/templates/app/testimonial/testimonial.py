from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from printing.models import Testimonials, User
from printing import db


testimony = Blueprint("testimonial", __name__, url_prefix="/testimonial")

#DONE: Make new page for testimonials

@testimony.route("/")
@login_required
def testimonial():
    testimonials = db.session.query(Testimonials).filter(Testimonials.active).all()
    return render_template('app/testimonial/testimonial.html', user=User, testimonials=testimonials, action=1)

@testimony.route("/edit/<id>", methods=['GET','POST'])
@login_required
def testimonial_edit(id):
    testimony = db.session.query(Testimonials).filter(Testimonials.id == id).first()
    if request.method == 'POST':
        testimony.name = request.form.get('name')
        testimony.testimonial = request.form.get('testimonial')
        testimony.fulltext = request.form.get('fulltext')
        testimony.date_created = request.form.get('date_created')
        testimony.active = bool(request.form.get('active'))
        db.session.commit()
        return redirect(url_for('testimonial.testimonial'))
    return render_template('app/testimonial/testimonial_edit.html', user=User, testimony=testimony)

@testimony.route("/new", methods=['GET','POST'])
@login_required
def testimonial_new():
    if request.method == "POST":
        data = request.form.to_dict()
        
        newtest = Testimonials(
            name = data['name'],
            testimonial = data['testimonial'],
            fulltext = data['fulltext'],
            active = bool(data['active']),
            date_created = datetime.now(),
        )
        db.session.add(newtest)
        db.session.commit()
        return redirect(url_for('testimonial.testimonial'))
    return render_template('app/testimonial/testimonial_new.html', user=User)
