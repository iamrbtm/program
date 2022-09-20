import json
import os
import re

import requests
from flask import flash
from matplotlib import colors

from printing import db, invgcode
from printing.gcoder import parse_gcode
from printing.models import *
from sqlalchemy.sql import func


filename = "temp.log"


def format_tel(phone):
    if phone != "":
        clean_phone = re.sub("[^0-9]+", "", phone)
        formatted_phone = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_phone[:-1])) + clean_phone[-1]
        return formatted_phone
    else:
        return ""


def get_states():
    states = [
        ["Alabama", "AL"],
        ["Alaska", "AK"],
        ["Arizona", "AZ"],
        ["Arkansas", "AR"],
        ["California", "CA"],
        ["Colorado", "CO"],
        ["Connecticut", "CT"],
        ["Delaware", "DE"],
        ["District Of Columbia", "DC"],
        ["Florida", "FL"],
        ["Georgia", "GA"],
        ["Hawaii", "HI"],
        ["Idaho", "ID"],
        ["Illinois", "IL"],
        ["Indiana", "IN"],
        ["Iowa", "IA"],
        ["Kansas", "KS"],
        ["Kentucky", "KY"],
        ["Louisiana", "LA"],
        ["Maine", "ME"],
        ["Maryland", "MD"],
        ["Massachusetts", "MA"],
        ["Michigan", "MI"],
        ["Minnesota", "MN"],
        ["Mississippi", "MS"],
        ["Missouri", "MO"],
        ["Montana", "MT"],
        ["Nebraska", "NE"],
        ["Nevada", "NV"],
        ["New Hampshire", "NH"],
        ["New Jersey", "NJ"],
        ["New Mexico", "NM"],
        ["New York", "NY"],
        ["North Carolina", "NC"],
        ["North Dakota", "ND"],
        ["Ohio", "OH"],
        ["Oklahoma", "OK"],
        ["Oregon", "OR"],
        ["Pennsylvania", "PA"],
        ["Rhode Island", "RI"],
        ["South Carolina", "SC"],
        ["South Dakota", "SD"],
        ["Tennessee", "TN"],
        ["Texas", "TX"],
        ["Utah", "UT"],
        ["Vermont", "VT"],
        ["Virginia", "VA"],
        ["Washington", "WA"],
        ["West Virginia", "WV"],
        ["Wisconsin", "WI"],
        ["Wyoming", "WY"],
    ]
    return states


def populate_types():
    filtypes = {
        "results": [
            {
                "properties": "Making durable parts that need to withstand higher temperatures, Easy to print with, strong plastic",
                "useage": "Legos, instruments, sports equipment, Objects that might be dropped, knife handles, car phone mounts, phone cases, toys, wedding rings",
                "extruder_temp": "210-250",
                "bed_temp": "80-100",
                "bed_adhesion": "Kapton Tape, Hairspray, Test",
                "diameter": "1.75",
                "type": "ABS",
                "densitygcm3": "1.04",
                "m_in_1kg_3": "136",
                "m_in_1kg_175": "400",
            },
            {
                "properties": "Odorless, Low-warp, Eco-Friendly, Less energy to process",
                "useage": "Food containers such as candy wrappers, biodegradable medical implants, models, proto type parts",
                "extruder_temp": "190-230",
                "bed_temp": "60-80",
                "bed_adhesion": "Blue painters tape, Hairspray",
                "diameter": "1.75",
                "type": "PLA",
                "densitygcm3": "1.24",
                "m_in_1kg_3": "114",
                "m_in_1kg_175": "335",
            },
            {
                "properties": "Non harmful, non-toxic, and environment friendly, Easily be dissolved in water under normal temperature, Easily stripping.",
                "useage": "paper adhesive, thickener, packaging film in feminine hygiene, adult incontinence products, childrens play putty or slime, freshwater sports fishing",
                "extruder_temp": "180-230",
                "bed_temp": "55-60",
                "bed_adhesion": "Blue Painters Tape",
                "diameter": "1.75",
                "type": "PVA",
                "densitygcm3": "1.23",
                "m_in_1kg_3": "115",
                "m_in_1kg_175": "338",
            },
            {
                "properties": "Extremely durable and prints without odor. Has superior impact resistance that is superior to PET. Low shrinkage, no warping and not brittle.",
                "useage": "Protective components like phone cases and mechanical parts that require flexibility. Food containers like cups and plates.",
                "extruder_temp": "220-245",
                "bed_temp": "70-75",
                "bed_adhesion": "Blue Painters Tape",
                "diameter": "1.75",
                "type": "PETG",
                "densitygcm3": "1.27",
                "m_in_1kg_3": "111",
                "m_in_1kg_175": "328",
            },
            {
                "properties": "Biodegradable, Great 3D Support material, low-cost",
                "useage": "costumes, models, miniature figurines, prototyping",
                "extruder_temp": "220-230",
                "bed_temp": "50-60",
                "bed_adhesion": "Kapton Tape, Hairspray",
                "diameter": "1.75",
                "type": "HIPS",
                "densitygcm3": "1.03",
                "m_in_1kg_3": "137",
                "m_in_1kg_175": "404",
            },
            {
                "properties": "strong, lightweight, durable, flexible, wear-resistant, 100% thermoplastic",
                "useage": "machine parts, mechanical components, structural parts, gears and bearings, dynamic load, containers, tools, consumer products and toys.",
                "extruder_temp": "210-250",
                "bed_temp": "60-80",
                "bed_adhesion": "PVA Based Glue",
                "diameter": "1.75",
                "type": "Nylon",
                "densitygcm3": "1.52",
                "m_in_1kg_3": "93",
                "m_in_1kg_175": "274",
            },
            {
                "properties": "Versatility, Real wood scent, Durability, contain real wood fibers",
                "useage": "wooden box, wooden figurine, tables, chairs, cups or the likes.",
                "extruder_temp": "200-260",
                "bed_temp": "90-110.",
                "bed_adhesion": "Blue Painters Tape",
                "diameter": "1.75",
                "type": "Wood",
                "densitygcm3": "1.28",
                "m_in_1kg_3": "111",
                "m_in_1kg_175": "325",
            },
            {
                "properties": "Highly Durable, Soluble, Low Warpage, Good layer adhesion",
                "useage": "Frames, supports, propellers, tools, mechanical parts, protective casings, shells, high durability applications",
                "extruder_temp": "195-220",
                "bed_temp": "50-50",
                "bed_adhesion": "Blue Painters Tape",
                "diameter": "1.75",
                "type": "Carbon Fiber",
                "densitygcm3": "1.3",
                "m_in_1kg_3": "109",
                "m_in_1kg_175": "320",
            },
            {
                "properties": "Flexible 3D printing material, excellent abrasion resistance, smooth feeding properties, Durability",
                "useage": "Toys, novelty items, wearable, phone cases, visual products.",
                "extruder_temp": "210-225",
                "bed_temp": "20-55",
                "bed_adhesion": "Blue Painters Tape",
                "diameter": "1.75",
                "type": "Flexible/TPE",
                "densitygcm3": "2.16",
                "m_in_1kg_3": "66",
                "m_in_1kg_175": "193",
            },
        ]
    }

    if len(filtypes["results"]) != Type.query.count():
        for fil in filtypes["results"]:
            typename = fil["type"]
            cnt = Type.query.filter(Type.type == typename).count()
            if cnt == 0:
                etemp = fil["extruder_temp"]
                bedtemp = fil["bed_temp"]
                adh = fil["bed_adhesion"]
                diam = fil["diameter"]
                use = fil["useage"]
                prop = fil["properties"]

                new = Type(
                    type=typename,
                    properties=prop,
                    useage=use,
                    extruder_temp=etemp,
                    bed_temp=bedtemp,
                    bed_adhesion=adh,
                    diameter=diam,
                    densitygcm3=fil["densitygcm3"],
                    m_in_1kg_3=fil["m_in_1kg_3"],
                    m_in_1kg_175=fil["m_in_1kg_175"],
                )
                db.session.add(new)
                db.session.commit()


def convert_color_to_hex(color: str):
    color = color.lower()
    valid, newcolor = valid_color(color)
    if valid:
        return colors.to_hex(newcolor)
    else:
        flash("No color found", category="error")
        return "000000"


def valid_color(color: str):
    valid_colors = [
        "mediumvioletred",
        "deeppink",
        "palevioletred",
        "hotpink",
        "lightpink",
        "pink",
        "darkred",
        "red",
        "firebrick",
        "crimson",
        "indianred",
        "lightcoral",
        "salmon",
        "darksalmon",
        "lightsalmon",
        "orangered",
        "tomato",
        "darkorange",
        "coral",
        "orange",
        "darkkhaki",
        "gold",
        "khaki",
        "peachpuff",
        "yellow",
        "palegoldenrod",
        "moccasin",
        "papayawhip",
        "lightgoldenrodyellow",
        "lemonchiffon",
        "lightyellow",
        "maroon",
        "brown",
        "saddlebrown",
        "sienna",
        "chocolate",
        "darkgoldenrod",
        "peru",
        "rosybrown",
        "goldenrod",
        "sandybrown",
        "tan",
        "burlywood",
        "wheat",
        "navajowhite",
        "bisque",
        "blanchedalmond",
        "cornsilk",
        "darkgreen",
        "green",
        "darkolivegreen",
        "forestgreen",
        "seagreen",
        "olive",
        "olivedrab",
        "mediumseagreen",
        "limegreen",
        "lime",
        "springgreen",
        "mediumspringgreen",
        "darkseagreen",
        "mediumaquamarine",
        "yellowgreen",
        "lawngreen",
        "chartreuse",
        "lightgreen",
        "greenyellow",
        "palegreen",
        "teal",
        "darkcyan",
        "lightseagreen",
        "cadetblue",
        "darkturquoise",
        "mediumturquoise",
        "turquoise",
        "aqua",
        "cyan",
        "aquamarine",
        "paleturquoise",
        "lightcyan",
        "navy",
        "darkblue",
        "mediumblue",
        "blue",
        "midnightblue",
        "royalblue",
        "steelblue",
        "dodgerblue",
        "deepskyblue",
        "cornflowerblue",
        "skyblue",
        "lightskyblue",
        "lightsteelblue",
        "lightblue",
        "powderblue",
        "indigo",
        "purple",
        "darkmagenta",
        "darkviolet",
        "darkslateblue",
        "blueviolet",
        "darkorchid",
        "fuchsia",
        "magenta",
        "slateblue",
        "mediumslateblue",
        "mediumorchid",
        "mediumpurple",
        "orchid",
        "violet",
        "plum",
        "thistle",
        "lavender",
        "white",
        "mistyrose",
        "antiquewhite",
        "linen",
        "beige",
        "whitesmoke",
        "lavenderblush",
        "oldlace",
        "aliceblue",
        "seashell",
        "ghostwhite",
        "honeydew",
        "floralwhite",
        "azure",
        "mintcream",
        "snow",
        "ivory",
        "white",
        "black",
        "darkslategray",
        "dimgray",
        "slategray",
        "gray",
        "lightslategray",
        "darkgray",
        "silver",
        "lightgray",
        "gainsboro",
    ]
    origcolor = color.replace(" ", "")
    colorsplit = color.split(" ")

    if origcolor in valid_colors:
        return [True, origcolor]
    elif len(colorsplit) != 1:
        for color in colorsplit:
            if color in valid_colors:
                return [True, color]
        else:
            return [False, "000000"]
    else:
        return [False, "000000"]


def shorten_url(longurl):
    url = "https://api-ssl.bitly.com/v4/shorten"
    dbtoken = db.session.query(apitoken).filter(apitoken.name == "bitley").first().token

    payload = json.dumps({"domain": "bit.ly", "long_url": f"{longurl}"})
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {dbtoken}"}

    response = requests.request("POST", url, headers=headers, data=payload)

    fulljson = json.loads(response.text)
    link = fulljson["link"]
    return link


# Calculation for Orders
def calc_time_length(filename, filamentfk):
    def calc_weight(length_in_m, filamentfk):
        import math

        fil = db.session.query(Filament).filter(Filament.id == filamentfk).first()
        diameter = fil.diameter
        density = fil.type_rel.densitygcm3

        # Volume = (length in m * 100) * pi() * ((diam/2)^2)
        filcm = length_in_m * 100
        radius = (diameter / 2) / 10
        csarea = math.pi * (radius) ** 2
        volume = filcm * csarea
        weight = volume * density
        return weight

    time_in_h, length_in_mm = parse_gcode(filename)
    weight_in_g = calc_weight(length_in_mm / 1000, filamentfk)
    return [time_in_h, weight_in_g / 1000]


def calc_total_all_print_objects(id):
    total_weight = 0.0
    total_time = 0.0

    all_files = json.loads(db.session.query(Project).filter(Project.id == id).first().objectfk)

    for file in all_files:
        printobj = db.session.query(Printobject).filter(Printobject.id == file).first()
        total_time = total_time + printobj.h_printtime
        total_weight = total_weight + printobj.kg_weight

    return total_weight, total_time


class CalcCostInd:
    def __init__(self, projectid, objectid):
        self.project = db.session.query(Project).filter(Project.id == projectid).first()
        self.object = db.session.query(Printobject).filter(Printobject.id == objectid).first()

        self.customer_disc = self.project.customer_rel.discount_factor
        self.customer_markup = self.project.customer_rel.markup_factor
        self.print_time = self.object.h_printtime  # in hrs
        self.weight_kg = self.object.kg_weight  # in KG
        self.qtyperprint = self.object.qtyperprint
        self.filename = self.object.file
        self.filamentid = self.project.filamentfk  # filament id
        self.diameter = self.project.filament_rel.diameter
        self.density = self.project.filament_rel.type_rel.densitygcm3
        self.cost_fil_per_g = self.project.filament_rel.priceperroll / 1000
        self.filament_kw_per_hr = self.project.filament_rel.type_rel.kW_hr

    def calc_m_to_g(self):
        import math

        # Volume = (length in m * 100) * pi() * ((diam/2)^2)
        filcm = self.weight_kg * 100
        radius = (self.diameter / 2) / 10
        csarea = math.pi * (radius) ** 2
        volume = filcm * csarea
        weight = volume * self.density
        self.weight_in_g = weight
        return weight

    def filcost(self):
        cost = ((self.weight_kg * 1000) * self.cost_fil_per_g) * self.customer_markup 
        if cost < 0.01:
            cost = 0.01
        return cost / self.qtyperprint

    def timecost(self):
        kw_per_hr = db.session.query(Settings).first().cost_kW

        cost = (self.print_time * kw_per_hr * self.filament_kw_per_hr) * self.customer_markup 
        if cost < 0.01:
            cost = 0.01
        return cost / self.qtyperprint

    def misfees(self):
        mis = float(self.project.packaging + self.project.advertising + self.project.rent + self.project.extrafees)
        return round(mis,2)

    def subtotal(self):
        sub = float(self.timecost() + self.filcost() + self.misfees())
        return round(sub,2)

    def total(self):
        if self.customer_disc == 1:
            discount = 1
        else: discount = 1 - self.customer_disc
        return round(self.subtotal() * discount, 2) + self.project.shipping_rel.cost


# Temp Data
def write_td(data):
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, "w") as file:
        file.write(data)


def get_td():
    if os.path.exists(filename):
        with open(filename, "r") as file:
            td = file.read()
        return td
    return ""


def flush_td():
    if os.path.exists(filename):
        os.remove(filename)


def update_kw_oregonavg():
    def get_new_rate():
        from bs4 import BeautifulSoup

        URL = "https://findenergy.com/providers/pacificorp/"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "lxml")

        r = soup.find("span", class_="stats__item__data")
        for i in r:
            oregonavg = float(i[:5]) / 100
        print(oregonavg)
        return oregonavg

    stg = db.session.query(Settings).first()
    stg.cost_kW = get_new_rate()
    db.session.commit()


def get_log_lat(id):
    """Gets long and lat from addresses in the database
    the program will get the address from the id of the
    person supplied

    Args:
        id (int): represents the persons whom addresses are
                  being processed
    """
    from geopy.geocoders import Nominatim

    addresses = db.session.query(Address).filter(Address.peoplefk == id).all()
    for address in addresses:
        addy = f"{address.address} {address.city} {address.state} {address.postalcode}"
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(addy)
        address.longitude = location.longitude
        address.latitudes = location.latitude
        db.session.commit()


def db_maintance():
    """
    Author: Jeremy Guill
    Date: 8/14/22
    Summary: Various tasks for maintaining the database for the printing program
    List of Tasks: Search for Inactive Users
                   #IDEA: Check on other db's
    """
    # No customer no employee and no supplier, set active to 0
    inactives = (
        db.session.query(People)
        .filter(People.customer == 0)
        .filter(People.is_employee == 0)
        .filter(People.supplier == 0)
        .all()
    )

    for inact in inactives:
        inact.active = 0
        db.session.commit()

    update_kw_oregonavg()


def Update_Inventory_Qty():
    inventory = db.session.query(Project).filter(Project.customerfk == 2).filter(Project.active == True).all()

    for item in inventory:
        adjustments = (
            Adjustment_log.query.with_entities(func.sum(Adjustment_log.adjustment).label("inv"))
            .filter(Adjustment_log.projectfk == item.id)
            .first()
            .inv
        )
        salesqty = (
            Sales_lineitems.query.with_entities(func.sum(Sales_lineitems.qty).label("salessum"))
            .filter(Sales_lineitems.projectfk == item.id)
            .first()
            .salessum
        )
        if adjustments == None and salesqty == None:
            item.current_quantity = 0
        elif adjustments == None and salesqty != None:
            item.current_quantity = salesqty * -1
        elif adjustments != None and salesqty == None:
            item.current_quantity = adjustments
        else:
            item.current_quantity = adjustments - salesqty
        db.session.commit()


def upload_store_gcode_file(gcodefile, path, filamentfk, project_link=0):
    """Uploads the given file to the /template/app/inventory(or project)/upload directory.  Then saves the record to the object_project table in the db

    Args:
        gcodefile (file): pass in the file from the form request.files['gcode']
        path (string): the path where the file is stored. Default is<<>>
        filamentfk (int): pass in the filament from the form. request.form.get('filamentfk')
        project_link (int, optional): The project numbner of the linked project if needed to link.  If you dont put any number in this postion, you will not link the file to any project. Defaults to 0.
    """
    # Save uploaded file
    gcodefile = invgcode.save(gcodefile)

    # process file for time and materials
    basepath = os.path.join(path, "uploads", gcodefile)
    if project_link == 0:
        filepath = base
    else:
        filepath = os.makedirs(os.path.join(base, project_link))
        os.rename(os.path.join(bath, gcodefile), os.path.join(filepath, gcodefile))

    time_in_h, weight_in_kg = calc_time_length(filepath, filamentfk)

    # save file to db
    newgcode = Printobject(file=gcodefile, print_time=time_in_h, weight_kg=weight_in_kg)
    db.session.add(newgcode)
    db.session.commit()

    if project_link != 0:
        db.session.refresh(newgcode)
        project = db.session.query(Project).filter(Project.id == project_link).first()
        objectfklist = json.loads(project.objectfk)
        objectfklist.append(newgcode.id)
        project.objectfk = objectfklist
        db.session.commit()


def get_city_state_from_postalcoide(postalcode):
    reqUrl = f"http://api.zippopotam.us/us/{postalcode}"

    response = requests.request("GET", reqUrl)

    response = json.loads(response.text)
    state = response["places"][0]["state abbreviation"]
    city = response["places"][0]["place name"]
    return city, state


def clean_inventory_uploads(path):
    import os

    filestokeep = []
    dbfiles = db.session.query(Printobject.file).all()
    for file in dbfiles:
        filestokeep.append(file[0])

    ext = ".gcode"
    for files in os.listdir(path):
        if files.endswith(ext):
            if files in filestokeep:
                continue
            else:
                os.remove(os.path.join(path, files))
        else:
            os.remove(os.path.join(path, files))


def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def convert_HHH_to_HMS(dec_string):
    hours = int(dec_string)
    minutes = (dec_string * 60) % 60
    seconds = (dec_string * 3600) % 60

    time = "%d:%02d:%02d" % (hours, minutes, seconds)
    return get_sec(time)


def calculate_est_vs_act_time(fileid, actual_time):
    est_time = convert_HHH_to_HMS(Printobject.query.filter(Printobject.id == fileid).first().h_printtime)
    project = db.session.query(Project).filter(Project.objectfk.contains(fileid)).first()
    # Save new data to the database
    newentry = Estimate_vs_actual_time(
        printerfk=project.printerfk, estimated_time_in_s=est_time, actual_time_in_s=actual_time
    )
    db.session.add(newentry)
    db.session.commit()

    # Calculate the average of all entries for the given machine
    printers = Printer.query.filter(Printer.active == True).all()

    for printer in printers:
        est = (
            Estimate_vs_actual_time.query.with_entities(
                func.sum(Estimate_vs_actual_time.estimated_time_in_s).label("EstTime")
            )
            .filter(Estimate_vs_actual_time.printerfk == printer.id)
            .first()
        )
        act = (
            Estimate_vs_actual_time.query.with_entities(
                func.sum(Estimate_vs_actual_time.actual_time_in_s).label("ActTime")
            )
            .filter(Estimate_vs_actual_time.printerfk == printer.id)
            .first()
        )

        avg = (act[0] / est[0]) * 100
        print(f"Printer {printer.id}: {avg}")

        # save the average to the database in the printer table
        printer.correction_percentage = avg
        db.session.commit()
