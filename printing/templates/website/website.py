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
from printing import db
from printing.models import Events

site = Blueprint("website", __name__)

@site.route("/")
def home():
    events = db.session.query(Events).filter(Events.start_date >= datetime.now()).filter(Events.publish == 1).order_by(Events.start_date).limit(5)
    return render_template("/website/index.html", events=events)