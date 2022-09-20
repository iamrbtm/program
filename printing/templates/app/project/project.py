from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import flask_login
from sqlalchemy import distinct
from sqlalchemy.orm import session
from printing.models import *
from printing import db, gcode
from printing.utilities import *
import datetime, random

proj = Blueprint("project", __name__, url_prefix="/project")

#DONE: Complete new project page

@proj.route("/")
@login_required
def project():
    context = {
        "user":User,
    }
    return redirect(url_for("project.open_orders"), **context)


@proj.route("/details/<int:id>")
@login_required
def projectdetails(id):
    project = db.session.query(Project).filter(Project.id == id).first()
    objects = db.session.query(Printobject).filter(Printobject.projectid == id).all()

    files = []
    totalcost = 0
    subtotal = 0
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
        thing['printer'] = project.printer_rel.name
        thing['filament_diameter'] = project.filament_rel.diameter
        thing['filament_type'] = project.filament_rel.type_rel.type
        files.append(thing)

        subtotal = round((subtotal + filcost + timecost),2)

        if obj == objects[-1]:
            totalcost = round(((project.threshold * subtotal) + miscost + project.shipping_rel.cost),2)
    
    histrecs = (db.session.query(Project).filter(Project.customerfk == project.customerfk).all())

    context = {
        "user": User,
        "action": 1,
        "project": project,
        "files": files,
        "subtotal": subtotal,
        "totalcost": totalcost,
        "misfees": miscost,
        "history": histrecs,
    }
    return render_template("app/project/project_details.html", **context)


@proj.route("/open_orders")
@login_required
def open_orders():
    # DONE: from open projects, click on the name of the project to take to details page
    openorders = db.session.query(Project).filter(Project.customerfk != 2).filter(Project.active == True).all()
    context = {
        "user":User,
        "action":1,
        "projects":openorders
    }
    return render_template("app/project/open_orders.html", **context)


# DONE: new project
@proj.route("/new", methods=["GET", "POST"])
@login_required
def new_project():
    ordernumber = int(str("22" + str(random.randint(1000, 9999))))
    existingcust = db.session.query(People).filter(People.customer == True).filter(People.active == True).all()
    pastcust = db.session.query(People).filter(People.customer == True).filter(People.active == False).all()
    employees = db.session.query(People).filter(People.is_employee == True).filter(People.active == True).all()
    states = db.session.query(distinct(States.abr),States.abr, States.state).all()
    addresses = db.session.query(Address).all()
    shippingcost = db.session.query(Shipping).all()
    filaments = db.session.query(Filament).filter(Filament.active == True).all()
    printers = db.session.query(Printer).filter(Printer.active == True).all()
    
    if request.method == "POST":
        objectids = []
        
        newproj = Project(
            project_name=request.form.get("projectname"),
            customerfk= request.form.get("customer"),
            printerfk=request.form.get("printer"),
            filamentfk=request.form.get("filamentfk"),
            shippingfk=request.form.get("shippingcost"),
            employeefk=request.form.get("employee"),
            packaging=request.form.get("packaging"),
            advertising=request.form.get("advertising"),
            rent=request.form.get("rent"),
            extrafees=request.form.get("other"),
            ordernum=int(str("22" + str(random.randint(1000, 9999)))),
            active=1,
            threshold = request.form.get("qty"),
            priority = request.form.get("priority"),
            current_quantity=0
        )
        db.session.add(newproj)
        db.session.commit()
        db.session.refresh(newproj)
        
        for i in range(1, 8):
            gcodename = f"gcode{i}"
            qtyname = f"qty{i}"
            if request.files[gcodename].filename != "":
                # Save uploaded file
                gcodefile = gcode.save(request.files[gcodename])

                # process file for time and materials
                basedir = os.path.abspath(os.path.dirname(__file__))
                filepath = os.path.join(basedir, "uploads", gcodefile)

                time_in_h, weight_in_kg = calc_time_length(filepath, request.form.get("filamentfk"))

                # save file to db
                newgcode = Printobject(
                    file=gcodefile, 
                    h_printtime=time_in_h, 
                    kg_weight=weight_in_kg,
                    qtyperprint = request.form.get(qtyname),
                    projectid = newproj.id
                    )
                db.session.add(newgcode)
                db.session.commit()
                db.session.refresh(newgcode)
                objectids.append(newgcode.id)

        newproj.objectfk = objectids
        db.session.commit()
        
        #redirect to project details
        return redirect(url_for('project.projectdetails', id=newproj.id))
    
    
    content = {"user": User, "ordernumber":ordernumber,
               "customers":existingcust,
               "pastcusts":pastcust,
               "states":states,
               "shipping":addresses,
               'ordernumber':ordernumber,
               "employees":employees,
               'time':datetime.datetime.now().strftime("%H:%M:%S"),
               'date':datetime.datetime.now().strftime("%Y-%m-%d"),
               "shippingcost":shippingcost,
               
               "filaments":filaments,
               "printers":printers,
               
               }
    return render_template("/app/project/project_new.html", **content)

@proj.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    if request.method == "POST":
        gcodefile = gcode.save(request.files['gcode'])
        newgcode = Printobject(
            file = gcodefile
        )
        db.session.add(newgcode)
        db.session.commit()
        db.session.refresh(newgcode)
        
        basedir = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(basedir, 'uploads', gcodefile)

        time_in_h, weight_in_kg = calc_time_length(filepath,request.form.get('filamentfk'))
        
        newgcode.h_printtime = time_in_h
        newgcode.kg_weight = weight_in_kg
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    
    filaments = db.session.query(Filament).filter(Filament.active == True).order_by(Filament.typefk).all()
    context={
        "user":User,
        "filaments":filaments
    }
    return render_template('app/project/upload_gcode.html', **context)
        
@proj.route('/clean')
def clean():
    import fnmatch
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    clean_inventory_uploads(filepath)
    return redirect(url_for('project.open_orders')) 