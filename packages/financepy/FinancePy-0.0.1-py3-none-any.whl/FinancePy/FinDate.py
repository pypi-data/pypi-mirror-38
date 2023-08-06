# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 07:26:46 2016

@author: Dominic
"""

import datetime

dayNames = ['MON','TUES','WED','THURS','FRI']

monthNames = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

###############################################################################
###############################################################################

class FinDate(object):

    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6

    """ Use a wrapper class for dates in case we wish to change implementation later """

    def __init__(self, d, m, y):
        self.d = d
        self.m = m
        self.y = y
        self.refresh()

    def refresh(self):
        dt = datetime.date(self.y, self.m, self.d)
        delta = dt - datetime.date(1900, 1, 1)
        self.excelDate = delta.days
        self.weekday = dt.weekday()

    def excelDate(self):
        return self.excelDate

    def isWeekend(self):
        if self.weekday == FinDate.SAT or self.weekday == FinDate.SUN:
            return True

        return False

    def addDays(self, numDays):
        dt = datetime.date(self.y, self.m, self.d)
        dt = dt + datetime.timedelta(days=numDays)

        d = dt.day
        m = dt.month
        y = dt.year

        newDt = FinDate(d, m, y)
        return newDt
    
    def addMonths(self, months):
        m = self.m + months
        y = self.y
        d = self.d

        while m > 12:
            m -= 12
            y += 1

        while m < 1:
            m += 12
            y -= 1

        newDt = FinDate(d, m, y)
        return newDt

    def string(self):
        dateStr = ""

        if self.weekday == FinDate.MON:
            dateStr += "Mon"
        elif self.weekday == FinDate.TUE:
            dateStr += "Tue"
        elif self.weekday == FinDate.WED:
            dateStr += "Wed"
        elif self.weekday == FinDate.THU:
            dateStr += "Thu"
        elif self.weekday == FinDate.FRI:
            dateStr += "Fri"
        elif self.weekday == FinDate.SAT:
            dateStr += "Sat"
        elif self.weekday == FinDate.SUN:
            dateStr += "Sun"

        dateStr += " " + str(self.d) + " "

        if self.m == 1:
            dateStr += "Jan"
        elif self.m == 2:
            dateStr += "Feb"
        elif self.m == 3:
            dateStr += "Mar"
        elif self.m == 4:
            dateStr += "Apr"
        elif self.m == 5:
            dateStr += "May"
        elif self.m == 6:
            dateStr += "Jun"
        elif self.m == 7:
            dateStr += "Jul"
        elif self.m == 8:
            dateStr += "Aug"
        elif self.m == 9:
            dateStr += "Sep"
        elif self.m == 10:
            dateStr += "Oct"
        elif self.m == 11:
            dateStr += "Nov"
        elif self.m == 12:
            dateStr += "Dec"

        dateStr += " " + str(self.y) + " "
        return dateStr
