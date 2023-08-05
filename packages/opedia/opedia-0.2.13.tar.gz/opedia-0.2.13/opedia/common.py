import sys
sys.dont_write_bytecode = True
import os
sys.path.append(os.path.dirname(__file__))
import db
import numpy as np
from datetime import date, datetime, timedelta




def PiscesDates_Offline(startDate=date(2011, 12, 31), endDate=date(2017, 12, 9)):
    delta = endDate - startDate
    dates = [(startDate + timedelta(days=x)) for x in range(0, delta.days+1, 7)]
    return dates



def nearestDate(dates, dt):
    return min(dates, key=lambda d: abs(d - dt))




def timesBetween(calTable, startDate, endDate):
    query = "SELECT [time] FROM %s WHERE " % calTable
    query += "[time] BETWEEN '%s' AND '%s' " % (startDate, endDate)
    df = db.dbFetch(query)
    return np.array(df['time'])



def temporalRes(table):
    table = table.lower()
    dt = 1                  # default temporal resolution = 1 day
    #if table.find('tblPisces'.lower()) != -1:
    #    dt = 7
    return dt