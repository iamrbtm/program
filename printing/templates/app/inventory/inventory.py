import json
import os
import datetime
import random

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    send_from_directory,
    make_response
)
from flask_login import login_required
from printing import db, invgcode
from printing.models import (
    Adjustment_log,
    Project,
    User,
    Printobject,
    Filament,
    Printer,
)
from printing.utilities import (
    calc_time_length,
    Update_Inventory_Qty,
    CalcCostInd,
    clean_inventory_uploads,
)
from sqlalchemy import distinct
from sqlalchemy.sql import func


inv = Blueprint("inventory", __name__, url_prefix="/inventory")


@inv.route("/")
@login_required
def inventory():
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active).all()
    context = {"user": User, "inventory": inventory, "action": 1}
    return render_template("app/inventory/inventory.html", **context)


@inv.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def inventory_edit(id):
    inventory = db.session.query(Project).filter(Project.id == id).first()

    if request.method == "POST":
        objectids = inventory.objectfk
        for i in range(1, 8):
            gcodename = f"gcode{i}"
            qtyname = f"qty{i}"
            if request.files[gcodename].filename != "":
                # Save uploaded file
                gcodefile = invgcode.save(request.files[gcodename])

                # process file for time and materials
                basedir = os.path.abspath(os.path.dirname(__file__))
                filepath = os.path.join(basedir, "uploads", gcodefile)

                time_in_h, weight_in_kg = calc_time_length(filepath, request.form.get("filament"))

                qty = request.form.get(qtyname)
                
                # save file to db
                newgcode = Printobject(
                    file=gcodefile,
                    h_printtime=time_in_h, 
                    kg_weight=weight_in_kg,
                    qtyperprint = qty,
                    projectid = invrentory.id,
                    )
                db.session.add(newgcode)
                db.session.commit()
                db.session.refresh(newgcode)
                objectids.append(newgcode.id)

        newval = request.form.to_dict()
        inventory.project_name = newval["name"]
        inventory.customerfk = 2
        inventory.printerfk = int(newval["printer"])
        inventory.filamentfk = int(newval["filament"])
        inventory.objectfk = objectids
        inventory.shippingfk = 3
        inventory.employeefk = 1
        inventory.packaging = float(newval["packaging"])
        inventory.advertising = float(newval["advertising"])
        inventory.rent = float(newval["rent"])
        inventory.extrafees = float(newval["other"])
        inventory.active = 1
        inventory.threshold = int(newval["threshold"])
        inventory.sale_price = float(newval["sale_price"])
        inventory.catagory = str(newval["catagory"])
        db.session.commit()

        return redirect(url_for("inventory.inventory_details", id=id))

    printers = db.session.query(Printer).filter(Printer.active).all()
    filaments = db.session.query(Filament).filter(Filament.active).all()
    objfks = inventory.objectfk
    objects = db.session.query(Printobject).filter(Printobject.id.in_(objfks)).all()

    context = {
        "user": User,
        "inventory": inventory,
        "printers": printers,
        "filaments": filaments,
        "objects": objects,
    }
    return render_template("app/inventory/inventory_edit.html", **context)


@inv.route("/adjust", methods=["GET", "POST"])
@login_required
def inventory_adjust():
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active).all()

    if request.method == "POST":
        projectid = request.form.get("item")
        newadj = Adjustment_log(
            projectfk=projectid,
            adjustment=request.form.get("adjustment"),
            description=request.form.get("desc"),
            time_created=datetime.datetime.now(),
        )
        db.session.add(newadj)
        
        for inv in inventory:
            if inv.id == int(projectid):
                qty = int(inv.current_quantity)
                inv.current_quantity = int(qty) + int(request.form.get("adjustment"))
        
        db.session.commit()

        return redirect(url_for("inventory.inventory"))

    context = {"user": User, "inventory": inventory}
    return render_template("app/inventory/inventory_adjust.html", **context)


@inv.route("/new", methods=["GET", "POST"])
@login_required
def inventory_new():
    if request.method == "POST":
        objectids = []
        
        newinv = Project(
            project_name=request.form.get("name"),
            customerfk=2,
            printerfk=request.form.get("printer"),
            filamentfk=request.form.get("filament"),
            shippingfk=3,
            employeefk=1,
            packaging=request.form.get("packaging"),
            advertising=request.form.get("advertising"),
            rent=request.form.get("rent"),
            extrafees=request.form.get("other"),
            ordernum=int(str("22" + str(random.randint(1000, 9999)))),
            active=1,
            threshold = request.form.get('threshold'),
            sale_price=request.form.get("sale_price"),
            current_quantity=0,
            catagory=request.form.get("catagory"),
        )
        db.session.add(newinv)
        db.session.commit()
        db.session.refresh(newinv)
        
        for i in range(1, 8):
            gcodename = f"gcode{i}"
            qtyname = f"qty{i}"
            if request.files[gcodename].filename != "":
                # Save uploaded file
                gcodefile = invgcode.save(request.files[gcodename])

                # process file for time and materials
                basedir = os.path.abspath(os.path.dirname(__file__))
                filepath = os.path.join(basedir, "uploads", gcodefile)

                time_in_h, weight_in_kg = calc_time_length(filepath, request.form.get("filament"))

                # save file to db
                newgcode = Printobject(
                    file=gcodefile, 
                    h_printtime=time_in_h, 
                    kg_weight=weight_in_kg,
                    qtyperprint = request.form.get(qtyname),
                    projectid = newinv.id
                    )
                db.session.add(newgcode)
                db.session.commit()
                db.session.refresh(newgcode)
                objectids.append(newgcode.id)

        newinv.objectfk = objectids
        db.session.commit()

        

        return redirect(url_for("inventory.inventory_details", id=newinv.id))

    catagory = db.session.query(distinct(Project.catagory), Project.catagory).all()
    printers = db.session.query(Printer).filter(Printer.active).all()
    filaments = db.session.query(Filament).filter(Filament.active).all()

    context = {
        "user": User,
        "printers": printers,
        "filaments": filaments,
        "catagory": catagory,
    }
    return render_template("app/inventory/inventory_new.html", **context)


@inv.route("/details/<id>")
@login_required
def inventory_details(id):
    inventory = db.session.query(Project).filter(Project.id == id).first()
    objects = db.session.query(Printobject).filter(Printobject.projectid == id).all()

    files = []
    totalcost = 0
    for obj in objects:
        printobj = CalcCostInd(id, obj.id)
        
        filcost = printobj.filcost()
        timecost = printobj.timecost()
        miscost = printobj.misfees()
        
        thing = {}
        thing['weight_kg'] = obj.kg_weight
        thing['print_time'] = obj.h_printtime
        thing['filename'] = obj.file
        thing['qtyperprint'] = obj.qtyperprint
        thing['filcost'] = filcost
        thing['timecost'] = timecost
        thing['printer'] = inventory.printer_rel.name
        thing['filament_diameter'] = inventory.filament_rel.diameter
        thing['filament_type'] = inventory.filament_rel.type_rel.type
        files.append(thing)

        if obj == objects[-1]:
            totalcost = totalcost + filcost + timecost + miscost
        else:
            totalcost = totalcost + filcost + timecost
    
    context = {
        "user": User,
        "action": 1,
        "inventory": inventory,
        "files": files,
        "total_cost": totalcost,
        "miscost": miscost,
    }
    return render_template("app/inventory/inventory_details.html", **context)


@inv.route("/<filename>", methods=["GET", "POST"])
def download(filename):
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "uploads")

    return send_from_directory(filepath, filename, as_attachment=True)


@inv.route("/clean")
def clean():
    import fnmatch

    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "uploads")
    dbcount = Printobject.query.count()
    filecount = len(fnmatch.filter(os.listdir(filepath), "*.*"))
    if dbcount != filecount:
        clean_inventory_uploads(filepath)
    return redirect(url_for("inventory.inventory"))


@inv.route("/low_inventory_report")
def low_inventory():
    items = db.session.query(Project).all()
    
    current_inv_sum = Project.query.with_entities(func.sum(Project.current_quantity).label('CurrentInventory')).first()
    threshold_sum = Project.query.with_entities(func.sum(Project.threshold).label('Threshold')).first()
    
    context = {"items":items,"curinv":int(current_inv_sum[0]),"threshold":int(threshold_sum[0])}
    
    return render_template("app/inventory/low_inventory_pdf.html", **context)


@inv.route("/threshold", methods=["GET", "POST"])
def threshold():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
    catagory = db.session.query(distinct(Project.catagory), Project.catagory).all()
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active).all()
    return render_template("app/inventory/threshold.html", inventory=inventory, catagory=catagory)


@inv.route("/print_time_report")
def print_time_report():
    items = db.session.query(Project).all()
    
    printtimes = []
    totalprinttime = 0
    for item in items:
        printtime = 0
        for obj in item.objectfk:
            ptime = Printobject.query.filter(Printobject.id == obj).first().h_printtime
            totaltime = printtime + ptime
        printtime = ((item.threshold - item.current_quantity)/ item.qtyperprint)* totaltime
        this = {}
        this['printtime'] = printtime
        this["id"] = item.id
        printtimes.append(this)
        totalprinttime = totalprinttime + printtime
    
    
    context = {"printtimes":printtimes, "items":items, "totalprinttime":totalprinttime}
    
    return render_template("app/inventory/print_time_report.html", **context)

@inv.route("/update")
def update():
    Update_Inventory_Qty()
    return redirect(url_for("inventory.inventory"))