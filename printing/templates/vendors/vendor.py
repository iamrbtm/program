from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    after_this_request,
    flash,
)
from flask_login import login_required, current_user
import flask_login
from sqlalchemy.orm import session
from printing.models import *
from printing.templates.base.base_process import *
from printing import db, photos
from printing.forms import *
from printing.utilities import *
import datetime

bp_vendor = Blueprint("vendor", __name__)


@bp_vendor.route("/", methods=["GET", "POST"])
@login_required
def vendor_main():
    form = Vendor_form()
    if form.validate_on_submit():
        newvendor = Vendors()
        form.populate_obj(newvendor)
        newvendor.userid = current_user.id
        db.session.add(newvendor)
        db.session.commit()
        return redirect(url_for("vendor.vendor_main"))
    
    vendors = Vendors.query.all()
    context = {"user": User, "vendors": vendors, 'form':form}
    return render_template("/vendors/vendor_main.html", **context)

@bp_vendor.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def vendor_edit(id):
    db_vendor = db.session.query(Vendors).filter_by(id = id).first()
    form = Vendor_form(obj=db_vendor)
    if form.validate_on_submit():
        form.populate_obj(db_vendor)
        db_vendor.userid = current_user.id
        db.session.add(db_vendor)
        db.session.commit()
        return redirect(form.referer.data)
    
    form.process(obj=db_vendor)
    form.referer.data = request.referrer
   
    vendor = Vendors.query.order_by(Vendors.name).all()
    context = {'user': User, 'vendors':vendor, 'form':form, 'vendor':db_vendor}
    return render_template("/vendors/vendor_edit.html", **context)