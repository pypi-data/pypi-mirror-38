# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 07:26:46 2016

@author: Dominic
"""
from FinDate import FinDate
from FinError import FinError

class FinCalendar(object):

    def __init__(self, name):

        if name != "TARGET" and name!= "US" and name != "UK" and name != "NONE" and name!= "WEEKEND":
            FinError("Invalid Calendar ", name)
            return
            
            
        self.name = name
        FinCalendar.easterMondayDay = [98, 90, 103, 95, 114, 106, 91, 111, 102, 87,
                                107, 99, 83, 103, 95, 115, 99, 91, 111, 96, 87,
                                107, 92, 112, 103, 95, 108, 100, 91,
                                111, 96, 88, 107, 92, 112, 104, 88, 108, 100,
                                85, 104, 96, 116, 101, 92, 112, 97, 89, 108,
                                100, 85, 105, 96, 109, 101, 93, 112, 97, 89,
                                109, 93, 113, 105, 90, 109, 101, 86, 106, 97,
                                89, 102, 94, 113, 105, 90, 110, 101, 86, 106,
                                98, 110, 102, 94, 114, 98, 90, 110, 95, 86,
                                106, 91, 111, 102, 94, 107, 99, 90, 103, 95,
                                115, 106, 91, 111, 103, 87, 107, 99, 84, 103,
                                95, 115, 100, 91, 111, 96, 88, 107, 92, 112,
                                104, 95, 108, 100, 92, 111, 96, 88, 108, 92,
                                112, 104, 89, 108, 100, 85, 105, 96, 116, 101,
                                93, 112, 97, 89, 109, 100, 85, 105, 97, 109,
                                101, 93, 113, 97, 89, 109, 94, 113, 105, 90,
                                110, 101, 86, 106, 98, 89, 102, 94, 114, 105,
                                90, 110, 102, 86, 106, 98, 111, 102, 94, 114,
                                99, 90, 110, 95, 87, 106, 91, 111, 103, 94,
                                107, 99, 91, 103, 95, 115, 107, 91, 111, 103,
                                88, 108, 100, 85, 105, 96, 109, 101, 93, 112,
                                97, 89, 109, 93, 113, 105, 90, 109, 101, 86,
                                106, 97, 89, 102, 94, 113, 105, 90, 110, 101,
                                86, 106, 98, 110, 102, 94, 114, 98, 90, 110,
                                95, 86, 106, 91, 111, 102, 94, 107, 99, 90,
                                103, 95, 115, 106, 91, 111, 103, 87, 107, 99,
                                84, 103, 95, 115, 100, 91, 111, 96, 88, 107,
                                92, 112, 104, 95, 108, 100, 92, 111, 96, 88,
                                108, 92, 112, 104, 89, 108, 100, 85, 105, 96,
                                116, 101, 93, 112, 97, 89, 109, 100, 85, 105]

    def adjust(self, dt, convention):

        m = dt.m

        if convention == "UNADJUSTED":
        
            return dt
        
        elif convention == "FOLLOWING":

            while self.isBusinessDay(dt) is False:
                dt = dt.addDays(1)

            return dt

        elif convention == "MODIFIED_FOLLOWING":

            while self.isBusinessDay(dt) is False:
                dt = dt.addDays(1)

            if dt.m != m:
                while self.isBusinessDay(dt) is False:
                    dt.addDays(-1)

            return dt

        elif convention == "PRECEDING":

            while self.isBusinessDay(dt) is False:
                dt.addDays(-1)

            return dt

        elif convention == "MODIFIED_PRECEDING":

            while self.isBusinessDay(dt) is False:
                dt.addDays(-1)

            return dt

        elif convention == "MODIFIED_PRECEDING":

            while self.isBusinessDay(dt) is False:
                dt.addDays(-1)

            if dt.m != m:
                while self.isBusinessDay(dt) is False:
                    dt.addDays(+1)

            return dt

        else:
            print("Unknown adjustment convention")

        return dt

###############################################################################

    def isBusinessDay(self, dt):

        y = dt.y
        m = dt.m
        d = dt.d

        startDate = FinDate(1, 1, y)

        dd = dt.excelDate - startDate.excelDate

        weekday = dt.weekday

        em = self.easterMondayDay[y-1901]

        if dt.isWeekend() is True:
            return False

        if self.name == "NONE":
            return dt
        
        if self.name == "WEEKEND":
            return True

        if self.name == "UK":

            if m == 1 and d == 1:  # new years day
                return False

            if dd == em:
                return False

            if dd == em - 3:  # good friday
                return False

            if m == 5 and d <= 7 and weekday == FinDate.MON:
                return False

            if m == 5 and d >= 25 and weekday == FinDate.MON:
                return False

            if m == 8 and d <= 7 and weekday == FinDate.MON:
                return False

            if m == 12 and d == 25:  # Xmas
                return False

            if m == 12 and d == 26:  # Boxing day
                return False

            if m == 12 and d == 27 and weekday == FinDate.MON:  # Xmas
                return False

            if m == 12 and d == 27 and weekday == FinDate.TUE:  # Xmas
                return False

            if m == 12 and d == 28 and weekday == FinDate.MON:  # Xmas
                return False

            if m == 12 and d == 28 and weekday == FinDate.TUE:  # Xmas
                return False

            return True

        elif self.name == "US":

            if m == 1 and d == 1:  # NYD
                return False

            if m == 12 and d == 31 and weekday == FinDate.FRI:  # NYE
                return False

            if dd == em:
                return False

            if dd == em - 3:
                return False

            if m == 1 and d >= 15 and weekday == FinDate.MON:
                return False

            if m == 2 and d >= 15 and d <= 21 and weekday == FinDate.MON:
                return False

            if m == 5 and d >= 25 and d <= 21 and weekday == FinDate.MON:
                return False

            if m == 7 and d == 4:  # Indep day
                return False

            if m == 7 and d == 5 and weekday == FinDate.MON:  # Indep day
                return False

            if m == 7 and d == 3 and weekday == FinDate.FRI:  # Indep day
                return False

            if m == 9 and d >= 8 and d <= 14 and weekday == FinDate.MON:
                return False

            if m == 11 and d == 11:  # Veterans day
                return False

            if m == 11 and d == 12 and weekday == FinDate.MON:  # Columbus day
                return False

            if m == 11 and d == 10 and weekday == FinDate.FRI:  # Columbus day
                return False

            if m == 11 and d >= 22 and d <= 28 and weekday == FinDate.THU:
                return False

            if m == 12 and d == 25:  # Xmas holiday
                return False

            if m == 12 and d == 26 and weekday == FinDate.MON:
                return False

            if m == 12 and d == 24 and weekday == FinDate.FRI:
                return False

            return True

        elif self.name == "TARGET":

            if m == 1 and d == 1:  # new years day
                return False

            if m == 5 and d == 1:  # May day
                return False

            if dd == em:  # Easter monday holiday
                return False

            if m == 12 and d == 25:  # Xmas bank holiday
                return False

            if m == 12 and d == 26:  # Xmas bank holiday
                return False

            if m == 12 and d == 31:  # NYD bank holiday
                return False

            return True


###############################################################################
###############################################################################
###############################################################################

    def easterMonday(self, y):

        easterMonday = self.easterMondayArray(y - 1901)

        return easterMonday
