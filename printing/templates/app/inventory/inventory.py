from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory
from flask_login import login_required, current_user
import flask_login
from sqlalchemy import distinct
from sqlalchemy.orm import session
from printing.models import *
from printing import db, invgcode
from printing.utilities import *
import datetime, random

inv = Blueprint("inventory", __name__, url_prefix="/inventory")

@inv.route("/")
@login_required
def inventory():
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active == True).all()
    context = {
        "user":User,
        "inventory":inventory,
        "action":1
    }
    return render_template("app/inventory/inventory.html", **context)


@inv.route("/new", methods=["GET", "POST"])
@login_required
def inventory_new():
    if request.method == "POST":
        if request.files['gcode'].filename != '':
            #Save uploaded file
            gcodefile = invgcode.save(request.files['gcode'])
            
            #process file for time and materials
            basedir = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basedir, 'uploads', gcodefile)

            time_in_h, weight_in_kg = calc_time_length(filepath,request.form.get('filament'))
            
            #save file to db
            newgcode = Printobject(
                file = gcodefile,
                h_printtime = time_in_h,
                kg_weight = weight_in_kg
            )
            db.session.add(newgcode)
            db.session.commit()
            db.session.refresh(newgcode)
        
        
        newinv = Project(
            project_name = request.form.get('name'),
            customerfk = 2,
            printerfk = request.form.get('printer'),
            filamentfk = request.form.get('filament'),
            objectfk = newgcode.id,
            shippingfk = 3,
            employeefk = 1,
            packaging = request.form.get('packaging'),
            advertising = request.form.get('advertising'),
            rent= request.form.get('rent'),
            extrafees= request.form.get('other'),
            ordernum = int(str("22" + str(random.randint(1000, 9999)))),
            active=1,
            sale_price= request.form.get('sale_price'),
            current_quantity = 0,
            qtyperprint = request.form.get('qtyperprint'),
        )
        db.session.add(newinv)
        db.session.commit()
        db.session.refresh(newinv)
        
        inv1 = CalcCost(newinv.id)
        newinv.cost = inv1.total() / newinv.qtyperprint
        db.session.commit()
        return redirect(url_for('inventory.inventory_details', id=newinv.id))
    
    
    printers = db.session.query(Printer).filter(Printer.active == True).all()
    filaments = db.session.query(Filament).filter(Filament.active == True).all()
    
    context = {
        "user":User,
        "printers":printers,
        "filaments":filaments
    }
    return render_template("app/inventory/inventory_new.html", **context)


@inv.route("/details/<id>")
@login_required
def inventory_details(id):
    inventory = db.session.query(Project).filter(Project.id == id).first()
    inv1 = CalcCost(id)
    context = {
        "user":User,
        "inventory":inventory,
        "newinventory": inv1,
        "materialused": inv1.kg_weight * 1000,
        "printtime": inv1.h_printtime,
        "filename":inventory.object_rel.file,
    }
    return render_template("app/inventory/inventory_details.html", **context)

@inv.route('/<filename>', methods=['GET', 'POST'])
def download(filename):
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')

    return send_from_directory(filepath, filename, as_attachment=True)