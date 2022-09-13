from flask import Blueprint, render_template
from flask_login import login_required, current_user
from printing.models import *
import datetime, calendar
from dateutil.relativedelta import relativedelta
from sqlalchemy import func, extract

dash = Blueprint("dashboard", __name__, url_prefix='/dashboard')

@dash.route("/")
@login_required
def dashboard():
    #Inventory
    topinv = (
        Sales_lineitems
        .query
        .join(Project, Sales_lineitems.projectfk == Project.id)
        .add_columns(Project.project_name, func.sum(Sales_lineitems.qty).label("sumqty"), func.sum(Sales_lineitems.price).label("sumprice"))
        .group_by(Sales_lineitems.projectfk)
        .order_by(func.sum(Sales_lineitems.qty).desc())
        .limit(3)
        .all()
    )
    
    #Sales
    my_date = datetime.date.today()
    year, weeknum, day_of_week = my_date.isocalendar()
    
    #week
    todays_week_date = f"{year}-W{weeknum}"
    start_week_date = datetime.datetime.strptime(todays_week_date + '-1', "%Y-W%W-%w")
    end_week_date = start_week_date + datetime.timedelta(days=6)
    dtc = Sales.date_time_created
    
    weekly_sales = (
        db.session
        .query(func.sum(Sales.total).label("sumtotal"))
        .filter(
            extract('month', Sales.date_time_created) >= start_week_date.month,
            extract('year', Sales.date_time_created) >= start_week_date.year,
            extract('day', Sales.date_time_created) >= start_week_date.day
        )
        .filter(
            extract('month', Sales.date_time_created) <= end_week_date.month,
            extract('year', Sales.date_time_created) <= end_week_date.year,
            extract('day', Sales.date_time_created) <= end_week_date.day
            )
        .all()
    )
    if weekly_sales[0][0] == None:
        weekly_sales = [(0,0)]
    
    weekly=[start_week_date,end_week_date,weekly_sales[0][0]]
    
    #monthly    
    start_month_date = datetime.datetime(my_date.year, my_date.month, 1)
    end_month_date = datetime.datetime(my_date.year, my_date.month, calendar.monthrange(my_date.year, my_date.month)[1])
    
    monthly_sales = (
        db.session
        .query(func.sum(Sales.total).label("sumtotal"))
        .filter(Sales.date_time_created.between(start_month_date, end_month_date))
        .all()
    )
    
    if monthly_sales[0][0] == None:
        monthly_sales = [(0,0)]
    
    monthly = [start_month_date,end_month_date,monthly_sales[0][0]]
    
    #yearly    
    start_year_date = datetime.datetime(my_date.year, 1, 1)
    end_year_date = datetime.datetime(my_date.year, 12, 31)
    
    yearly_sales = (
        db.session
        .query(func.sum(Sales.total).label("sumtotal"))
        .filter(Sales.date_time_created.between(start_year_date, end_year_date))
        .all()
    )
    
    if yearly_sales[0][0] == None:
        yearly_sales = [(0,0)]
    
    yearly = [start_year_date,end_year_date,yearly_sales[0][0]]
    content = {
        "user":User,
        "topinv":topinv,
        "weekly":weekly,
        "monthly":monthly,
        "yearly":yearly,
    }
    
    return render_template("app/dashboard/dashboard.html", **content)