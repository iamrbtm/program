import re, os, requests
from printing import db
from printing.models import *
from matplotlib import colors
from flask import flash

filename = "temp.log"


def format_tel(phone):
    if phone != "":
        clean_phone = re.sub("[^0-9]+", "", phone)
        formatted_phone = (
            re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1-", "%d" % int(clean_phone[:-1]))
            + clean_phone[-1]
        )
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
                "diameter": "1, 2",
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
                "diameter": "1, 2",
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
                "diameter": "1, 2",
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
                "diameter": "1, 2",
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
                "diameter": "1, 2",
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
                "diameter": "1, 2",
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
                "diameter": "1, 2",
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
                "diameter": "1, 2",
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
                "diameter": "1, 2",
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
    import requests
    import json

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
    def calc_weight(weightinm, filamentfk):
        import math

        diameter = (
            db.session.query(Filament.diameter)
            .filter(Filament.id == filamentfk)
            .scalar()
        )
        density = (
            db.session.query(Filament)
            .filter(Filament.id == filamentfk)
            .first()
            .type_rel.densitygcm3
        )
        # Volume = (length in m * 100) * pi() * ((diam/2)^2)
        filcm = weightinm * 100
        radius = (diameter / 2) / 10
        csarea = math.pi * (radius) ** 2
        volume = filcm * csarea
        weight = volume * density
        return weight

    stgs = db.session.query(Settings).first()
    Units = "Millimetres"
    import io, os, string, math, sys

    MoveDelay = 0.000014945651469
    PauseDelay = 0.0006

    f = open(filename)

    BaseTime = 15
    FeedRate = 0.0
    Material = 0.0
    MatFeed = 0.0

    DeltaX = 0.0
    DeltaY = 0.0
    DeltaZ = 0.0
    LastX = 0.0
    LastY = 0.0
    lastz = 0.0
    x = 0.0
    y = 0.0
    z = 0.0
    m = 0.0

    PauseCount = 0
    TotalMotion = 0.0
    Totaltime = 0.0
    MatTotaltime = 0.0
    Motion = 0.0
    gflag = 0
    MoveCount = 0

    LineCount = 0

    while True:
        # LineCount += 1
        # print(LineCount)
        flin = f.readline()
        if flin == "":
            break
        array1 = flin.split()

        for item in array1:
            gg = item[0]
            if item[0:3] == "G28":
                break
            elif item[0:3] == "G84":
                break
            elif gg == ";":
                break
            elif gg == "X":
                if item[1:] == "":
                    break
                else:
                    x = float(item[1:])
            elif gg == "Y":
                if item[1:] == "":
                    break
                else:
                    y = float(item[1:])
            elif gg == "Z":
                if item[1:] == "":
                    break
                else:
                    z = float(item[1:])
            elif item[0:3] == "G92":
                if MatFeed > 0:
                    Material += MatFeed
                    MatTotaltime += MatFeed / FeedRate * 2
                    PauseCount += 1
                break
            elif gg == "E":
                MatFeed = m
                m = float(item[1:])
            elif gg == "F":
                FeedRate = float(item[1:])
            elif item[0:2] == "G1":
                gflag = 1
                MoveCount += 1

        if gflag == 1:
            DeltaX = x - LastX
            DeltaY = y - LastY
            DeltaZ = z - lastz
            Motion = math.sqrt(DeltaX * DeltaX + DeltaY * DeltaY + DeltaZ * DeltaZ)
            TotalMotion += Motion
            Totaltime += Motion / FeedRate
            LastX = x
            LastY = y
            lastz = z
        gflag = 0
    f.closed

    timepad = 1 - stgs.padding_time

    printtime_in_min = float(
        (
            Totaltime
            + MoveCount * MoveDelay
            + BaseTime
            + PauseCount * PauseDelay
            + MatTotaltime
        )
        / timepad
    )

    matpad = 1 - stgs.padding_filament
    materialused_in_mm = float(Material) / matpad

    weight_in_g = calc_weight(materialused_in_mm / 1000, filamentfk)

    print(" material in mm = " + str(round(materialused_in_mm, 3)) + "mm")
    print("  material in m = " + str(round(materialused_in_mm / 1000, 3)) + "m")
    print("---------------")
    print("    time in min = " + str(round(printtime_in_min, 3)) + "min")
    print("     time in hr = " + str(round(printtime_in_min / 60, 3)) + "hrs")
    print("---------------")
    print("    weight in g = " + str(round(weight_in_g)) + "g")

    return round(printtime_in_min / 60, 3), weight_in_g/1000

class CalcCost:
    def __init__(self, id):
        self.project = db.session.query(Project).filter(Project.id == id).first()

        self.customer_disc = (
            self.project.customer_rel.discount_factor
        )  # customer specific discount
        self.customer_markup = (
            self.project.customer_rel.markup_factor
        )  # customer specific markup
        self.print_time = self.project.object_rel.h_printtime  # in hrs
        self.length_m = self.project.object_rel.kg_weight  # in KG
        self.filename = self.project.object_rel.file  # filename of object
        self.filamentid = self.project.filamentfk  # filament id
        self.diameter = self.project.filament_rel.diameter
        self.density = self.project.filament_rel.type_rel.densitygcm3
        self.kg_weight = self.project.object_rel.kg_weight
        self.h_printtime = self.project.object_rel.h_printtime
        self.cost_fil_per_g = self.project.filament_rel.priceperroll / 1000
        self.filament_kw_per_hr = self.project.filament_rel.type_rel.kW_hr
    

    def calc_m_to_g(self):
        import math

        # Volume = (length in m * 100) * pi() * ((diam/2)^2)
        filcm = self.length_m * 100
        radius = (self.diameter / 2) / 10
        csarea = math.pi * (radius) ** 2
        volume = filcm * csarea
        weight = volume * self.density
        self.weight_in_g = weight
        return weight

    def filcost(self):
        cost = (self.kg_weight * 1000) * self.cost_fil_per_g
        if cost < 0.01:
            cost = 0.01
        return cost * (1 + self.customer_markup)

    def timecost(self):
        kw_per_hr = db.session.query(Settings).first().cost_kW

        cost = self.h_printtime * kw_per_hr * self.filament_kw_per_hr
        if cost < 0.01:
            cost = 0.01
        return cost * (1 + self.customer_markup)

    def subtotal(self):
        return round(float(self.timecost() 
                + self.filcost() 
                + self.project.packaging
                + self.project.advertising
                + self.project.rent
                + self.project.extrafees
        ),2)
    def total(self):
        return (round(self.subtotal() * (1 - self.customer_disc),2)
                + self.project.shipping_rel.cost)

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
            oregonavg = float(i[:5])/100
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
        addy=f'{address.address} {address.city} {address.state} {address.postalcode}'
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
    inactives = db.session.query(People).filter(People.customer == 0).filter(People.is_employee == 0).filter(People.supplier == 0).all()
    
    for inact in inactives:
        inact.active = 0
        db.session.commit()
        
    update_kw_oregonavg()