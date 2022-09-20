from printing import db
from printing.models import *
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract, func



class timeEstimate:
    def __init__(self):
        self.totaltime = 0
        self.estimatedate = datetime.datetime.today()
        self.printTimeInDays = 0
        self.duringBizHrs = False
        self.estimatedCompletionDate = datetime.datetime.today()
        
    def getTotalTime(self):
        project = db.session.query(Project).filter(Project.active == 1).filter(Project.customerfk != 2).all()
        
        for pro in project:
            for objid in pro.objectfk:
                t = db.session.query(Printobject.h_printtime).filter(Printobject.id == objid).first()
                self.totaltime = self.totaltime + t[0]

    def EstimatePrintTime(self):
        self.getTotalTime()
        self.convertDecTime(self.totaltime)
        self.estimatedDateTimeToPrint(self.printTimeInDays)
        self.time_in_range(self.estimatedCompletionDate)
        
        if self.duringBizHrs:
            if self.estimatedCompletionDate.weekday() == 5:
                self.estimatedate = self.estimatedate + datetime.timedelta(days=2)
            elif self.estimatedCompletionDate.weekday() == 6:
                self.estimatedate = self.estimatedate + datetime.timedelta(days=1)
            else:
                self.estimatedate = self.estimatedate.date()
        else:
            if self.estimatedCompletionDate.weekday() == 5:
                self.estimatedate =  self.estimatedate + datetime.timedelta(days=2)
            else:
                self.estimatedate = self.estimatedate + datetime.timedelta(days=1)

        
    def time_in_range(self, current):
        current = current.time()
        start = db.session.query(Settings.bizstarttime).filter(Settings.id == 1).first()
        end = db.session.query(Settings.bizendtime).filter(Settings.id == 1).first()
        self.duringBizHrs = start[0].hour <= current.hour <= end[0].hour
    

    def convertDecTime(self, time):
        hours = int(time)
        minutes = (time*60) % 60
        totalmins = (hours*60)+minutes
        timeInDays = (totalmins / (14*60)) * 1.5
        self.printTimeInDays = timeInDays
    
    def estimatedDateTimeToPrint(self, printtime):
        now = datetime.datetime.now()
        delta = relativedelta(days=printtime).normalized()
        self.estimatedCompletionDate = now + delta