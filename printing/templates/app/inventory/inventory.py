from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, make_response
from flask_login import login_required, current_user
import flask_login
from sqlalchemy import distinct, and_
from sqlalchemy.orm import session
from printing.models import *
from printing import db, invgcode
from printing.utilities import *
import datetime, random, json

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


@inv.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def inventory_edit(id):
    inventory = db.session.query(Project).filter(Project.id == id).first()
    
    if request.method == "POST":
        objectids = json.loads(inventory.objectfk)
        for i in range(1,7):
            gcodename = f"gcode{i}"
            if request.files[gcodename].filename != '':
                #Save uploaded file
                gcodefile = invgcode.save(request.files[gcodename])
                
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
                objectids.append(newgcode.id)
                    
        newval = request.form.to_dict()
        inventory.project_name = newval['name']
        inventory.customerfk = 2
        inventory.printerfk = int(newval['printer'])
        inventory.filamentfk = int(newval['filament'])
        inventory.objectfk = json.dumps(objectids)
        inventory.shippingfk = 3
        inventory.employeefk = 1
        inventory.packaging = float(newval['packaging'])
        inventory.advertising = float(newval['advertising'])
        inventory.rent = float(newval['rent'])
        inventory.extrafees = float(newval['other'])
        inventory.active = 1
        inventory.sale_price = float(newval['sale_price'])
        inventory.qtyperprint = int(newval['qtyperprint'])
        inventory.catagory = str(newval['catagory'])
        db.session.commit()
        
        return redirect(url_for('inventory.inventory_details', id=id))
    
    printers = db.session.query(Printer).filter(Printer.active == True).all()
    filaments = db.session.query(Filament).filter(Filament.active == True).all()
    objfks = json.loads(inventory.objectfk)
    objects = db.session.query(Printobject).filter(Printobject.id.in_(objfks)).all()
    
    context = {
        "user":User,
        "inventory":inventory,
        "printers":printers,
        "filaments":filaments,
        "objects":objects
    }
    return render_template("app/inventory/inventory_edit.html", **context)


@inv.route("/adjust", methods=["GET", "POST"])
@login_required
def inventory_adjust(): 
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active == True).all()
    
    if request.method == "POST":
        newadj = Adjustment_log(
            projectfk = request.form.get('item'),
            adjustment = request.form.get('adjustment'),
            description = request.form.get('desc'),
            time_created = datetime.datetime.now()
        )
        db.session.add(newadj)
        db.session.commit()
        
        Update_Inventory_Qty()
        return redirect(url_for('inventory.inventory'))
    
    context = {
    "user":User,
    "inventory":inventory
    }
    return render_template("app/inventory/inventory_adjust.html", **context)

@inv.route("/new", methods=["GET", "POST"])
@login_required
def inventory_new():
    if request.method == "POST":
        objectids = []
        for i in range(1,6):
            gcodename = f"gcode{i}"
            if request.files[gcodename].filename != '':
                #Save uploaded file
                gcodefile = invgcode.save(request.files[gcodename])
                
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
                objectids.append(newgcode.id)
        
        
        newinv = Project(
            project_name = request.form.get('name'),
            customerfk = 2,
            printerfk = request.form.get('printer'),
            filamentfk = request.form.get('filament'),
            objectfk = json.dumps(objectids),
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
            catagory = request.form.get('catagory')
        )
        db.session.add(newinv)
        db.session.commit()
        db.session.refresh(newinv)
        
        return redirect(url_for('inventory.inventory_details', id=newinv.id))
    
    catagory = db.session.query(distinct(Project.catagory), Project.catagory).all()
    printers = db.session.query(Printer).filter(Printer.active == True).all()
    filaments = db.session.query(Filament).filter(Filament.active == True).all()
    
    context = {
        "user":User,
        "printers":printers,
        "filaments":filaments,
        "catagory":catagory
    }
    return render_template("app/inventory/inventory_new.html", **context)


@inv.route("/details/<id>")
@login_required
def inventory_details(id):
    inventory = db.session.query(Project).filter(Project.id == id).first()
    files = []
    total_cost = 0.00
    i=1
    for objectid in json.loads(inventory.objectfk):
        objclassname = f"inv{objectid}"
        objclassname = CalcCostInd(id, objectid)
        
        timecost = objclassname.timecost()
        filcost = objclassname.filcost()
        miscost = objclassname.misfees()
        
        printer = Printer.query.filter(Printer.id == objclassname.project.printerfk).first().name
        filtype = inventory.filament_rel.type_rel.type
        diameter = inventory.filament_rel.diameter
        
        file = {}
        file['filename'] = objclassname.filename
        file['print_time'] = objclassname.print_time
        file['weight_kg'] = objclassname.weight_kg
        file['timecost'] = timecost
        file['filcost'] = filcost
        file['printer'] = printer
        file['filament_type'] = filtype
        file['filament_diameter'] = diameter
        files.append(file)
        
        total_cost = total_cost + timecost + filcost
        
        i = i + 1
    
    context = {
        "user":User,
        "action":1,
        "inventory":inventory,
        "files":files,
        "total_cost":total_cost,
        'miscost':miscost
    }
    return render_template("app/inventory/inventory_details.html", **context)

@inv.route('/<filename>', methods=['GET', 'POST'])
def download(filename):
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')

    return send_from_directory(filepath, filename, as_attachment=True)

@inv.route('/clean')
def clean():
    import fnmatch
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    dbcount = Printobject.query.count()
    filecount = len(fnmatch.filter(os.listdir(filepath), '*.*'))
    if dbcount != filecount:
        clean_inventory_uploads(filepath)
    return redirect(url_for('inventory.inventory')) 

@inv.route('/low_inventory_report')
def low_inventory():
    from flask_weasyprint import HTML, render_pdf
    items = db.session.query(Project).filter((Project.threshold - Project.current_quantity) > 2).all()
    return render_template("app/inventory/low_inventory_pdf.html", items=items)

@inv.route('/threshold', methods=['GET', 'POST'])
def threshold():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
    catagory = db.session.query(distinct(Project.catagory), Project.catagory).all()
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active == True).all()
    return render_template("app/inventory/threshold.html", inventory=inventory, catagory=catagory)
