from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import distinct
from printing.models import *
from printing.utilities import *
from printing import filamentpics
from datetime import datetime

evt = Blueprint("event", __name__, url_prefix="/event")

# DONE: make new event page
# TODO: make delete mehtod to delete an event


def unpublish_past_events():
    events = (
        db.session.query(Events)
        .filter(Events.start_date < datetime.now())
        .filter(Events.publish == 1)
        .all()
    )
    for event in events:
        event.publish = 0
        db.session.commit()


@evt.before_request
def before_request_callback():
    unpublish_past_events()


@evt.route("/")
@login_required
def event():
    events = db.session.query(Events).order_by(Events.start_date).all()
    return render_template("/app/events/event.html", user=User, events=events, action=1)


@evt.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def event_edit(id):
    events = db.session.query(Events).filter(Events.id == id).first()
    inv = db.session.query(Event_inventory).filter(Event_inventory.eventid == id).all()
    if request.method == "POST":
        events.title = request.form.get("title")
        events.start_date = request.form.get("start_date")
        events.start_time = request.form.get("start_time")
        events.location = request.form.get("location")
        events.end_time = request.form.get("end_time")
        events.end_date = request.form.get("end_date")
        events.publish = int(request.form.get("publish"))
        events.mapsurl = request.form.get("mapsurl")
        events.description = request.form.get("desc")
        db.session.commit()
        return redirect(url_for("event.event"))

    return render_template(
        "/app/events/event_edit.html", user=User, inv=inv, events=events
    )


@evt.route("/deleterecord/<id>/<projid>")
@login_required
def delete_record(id, projid):
    inv = db.session.query(Event_inventory).filter(Event_inventory.id == id).first()
    db.session.delete(inv)
    db.session.commit()
    return redirect(url_for("event.event_edit", id=projid))


@evt.route("/updateqty/<eventid>", methods=["POST"])
@login_required
def update_qty(eventid):
    data = request.form.to_dict()
    update = (
        db.session.query(Event_inventory)
        .filter(Event_inventory.eventid == eventid)
        .filter(Event_inventory.projectid == projid)
        .first()
    )
    update.qty = request.form.get("qty")
    db.session.commit()


@evt.route("/new", methods=["GET", "POST"])
@login_required
def event_new():
    inv = db.session.query(Project).all()
    contacts = db.session.query(People).filter(People.bazaar == 1).all()
    if request.method == "POST":
        newevent = Events(
            title=request.form.get("title"),
            start_date=request.form.get("start_date"),
            start_time=request.form.get("start_time"),
            location=request.form.get("location"),
            end_time=request.form.get("end_time"),
            end_date=request.form.get("end_date"),
            publish=int(request.form.get("publish")),
            mapsurl=request.form.get("mapsurl"),
            description=request.form.get("desc"),
            dos_contact_person=request.form.get("dos_contact"),
        )
        db.session.add(newevent)
        db.session.commit()
        db.session.refresh(newevent)

        inventorylist = request.form.getlist("inventory")

        if len(inventorylist) > 0:
            write_event_inv_to_db(inventorylist, newevent.id)
            return redirect(url_for("event.event_edit", id=newevent.id))
        else:
            return redirect(url_for("event.event"))
    return render_template(
        "app/events/event_new.html", user=User, inv=inv, contacts=contacts
    )


def write_event_inv_to_db(projectids, eventid):
    for proj in projectids:
        newevent = Event_inventory(eventid=eventid, projectid=proj)
        db.session.add(newevent)
        db.session.commit()
