import re, os
from printing import db
from printing.models import *
from matplotlib import colors
from flask import flash

filename = 'temp.log'
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


def populate_states():
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

    if len(states) != States.query.count():
        for st in states:
            abr = st[1]
            state = st[0]

            cnt = States.query.filter(States.abr == abr).count()
            if cnt == 0:
                new = States(abr=abr, state=state)
                db.session.add(new)
                db.session.commit()


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
                    m_in_1kg_175=fil["m_in_1kg_175"]
                )
                db.session.add(new)
                db.session.commit()


def convert_color_to_hex(color: str):
    valid, newcolor = valid_color(color)
    if valid:
        return colors.to_hex(newcolor)
    else:
        flash("No color found", category="error")
        return "000000"


def valid_color(color: str):
    valid_colors = [
        "MediumVioletRed",
        "DeepPink",
        "PaleVioletRed",
        "HotPink",
        "LightPink",
        "Pink",
        "DarkRed",
        "Red",
        "Firebrick",
        "Crimson",
        "IndianRed",
        "LightCoral",
        "Salmon",
        "DarkSalmon",
        "LightSalmon",
        "OrangeRed",
        "Tomato",
        "DarkOrange",
        "Coral",
        "Orange",
        "DarkKhaki",
        "Gold",
        "Khaki",
        "PeachPuff",
        "Yellow",
        "PaleGoldenrod",
        "Moccasin",
        "PapayaWhip",
        "LightGoldenrodYellow",
        "LemonChiffon",
        "LightYellow",
        "Maroon",
        "Brown",
        "SaddleBrown",
        "Sienna",
        "Chocolate",
        "DarkGoldenrod",
        "Peru",
        "RosyBrown",
        "Goldenrod",
        "SandyBrown",
        "Tan",
        "Burlywood",
        "Wheat",
        "NavajoWhite",
        "Bisque",
        "BlanchedAlmond",
        "Cornsilk",
        "DarkGreen",
        "Green",
        "DarkOliveGreen",
        "ForestGreen",
        "SeaGreen",
        "Olive",
        "OliveDrab",
        "MediumSeaGreen",
        "LimeGreen",
        "Lime",
        "SpringGreen",
        "MediumSpringGreen",
        "DarkSeaGreen",
        "MediumAquamarine",
        "YellowGreen",
        "LawnGreen",
        "Chartreuse",
        "LightGreen",
        "GreenYellow",
        "PaleGreen",
        "Teal",
        "DarkCyan",
        "LightSeaGreen",
        "CadetBlue",
        "DarkTurquoise",
        "MediumTurquoise",
        "Turquoise",
        "Aqua",
        "Cyan",
        "Aquamarine",
        "PaleTurquoise",
        "LightCyan",
        "Navy",
        "DarkBlue",
        "MediumBlue",
        "Blue",
        "MidnightBlue",
        "RoyalBlue",
        "SteelBlue",
        "DodgerBlue",
        "DeepSkyBlue",
        "CornflowerBlue",
        "SkyBlue",
        "LightSkyBlue",
        "LightSteelBlue",
        "LightBlue",
        "PowderBlue",
        "Indigo",
        "Purple",
        "DarkMagenta",
        "DarkViolet",
        "DarkSlateBlue",
        "BlueViolet",
        "DarkOrchid",
        "Fuchsia",
        "Magenta",
        "SlateBlue",
        "MediumSlateBlue",
        "MediumOrchid",
        "MediumPurple",
        "Orchid",
        "Violet",
        "Plum",
        "Thistle",
        "Lavender",
        "White",
        "MistyRose",
        "AntiqueWhite",
        "Linen",
        "Beige",
        "WhiteSmoke",
        "LavenderBlush",
        "OldLace",
        "AliceBlue",
        "Seashell",
        "GhostWhite",
        "Honeydew",
        "FloralWhite",
        "Azure",
        "MintCream",
        "Snow",
        "Ivory",
        "White",
        "Black",
        "DarkSlateGray",
        "DimGray",
        "SlateGray",
        "Gray",
        "LightSlateGray",
        "DarkGray",
        "Silver",
        "LightGray",
        "Gainsboro",
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


def calc_time_length(FileName):
    Units = "Millimetres"

    import io, os, string, math, sys

    MoveDelay = 0.000014945651469
    PauseDelay = 0.0006

    f = open(FileName)

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

    printtime = float(
        Totaltime
        + MoveCount * MoveDelay
        + BaseTime
        + PauseCount * PauseDelay
        + MatTotaltime
    )
    materialused = float(Material)

    print("material = " + str(materialused))
    print("    time = " + str(printtime))
    
    return printtime,materialused

def calculate_weight(weightinm, filament):
    import math

    diameter = db.session.query(Filament.diameter).filter(Filament.id == filament).scalar()
    density = db.session.query(Filament).filter(Filament.id==filament).first().type_rel.densitygcm3
    # Volume = (length in m * 100) * pi() * ((diam/2)^2)
    filcm = weightinm * 100
    radius = (diameter / 2) / 10
    csarea = math.pi * (radius) ** 2
    volume = filcm * csarea
    weight = volume * density
    return weight

def timecost(time_in_min, filament):
    time_in_hr = time_in_min / 60
    kw_per_hr = db.session.query(Settings).first().cost_kW
    filament_kw_per_hr = db.session.query(Filament).filter(Filament.id == filament).first().type_rel.kW_hr
    
    cost = time_in_hr*kw_per_hr*filament_kw_per_hr
    if cost < .01: cost = .01
    return cost

def filamentcost(weight_in_g, filamentfk):
    fil_cost_per_g = (db.session.query(Filament).filter(Filament.id == filamentfk).first().priceperroll)/1000
    
    cost = weight_in_g * fil_cost_per_g
    if cost < .01: cost = .01
    
    return cost

def write_td(data):
    if os.path.exists(filename):
        os.remove(filename)
    
    with open(filename, 'w') as file:
            file.write(data)

def get_td():
    if os.path.exists(filename):
        with open(filename,'r') as file:
            td = file.read()
        return td
    return ''

def flush_td():
    if os.path.exists(filename):
      os.remove(filename)