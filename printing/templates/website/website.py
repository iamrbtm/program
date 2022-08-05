from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    after_this_request,
    flash,
)

site = Blueprint("website", __name__)

@site.route("/")
def home():
    return render_template("/website/index.html")