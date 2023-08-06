from FinDate import FinDate
from FinError import FinError
from FinCalendar import FinCalendar

###############################################################################
"""
Comments

"""
###############################################################################

DaysInYear = 365.242

BASIS_ACT365 = 1
BASIS_ACT360 = 2
BASIS_30360E = 3
BASIS_30360U = 4
BASIS_ACTACT = 5

class FinBasis():

    
    def __init__(self,basisName):
        
        basisName = basisName.upper()

        self.code = 0

        if basisName == "ACT/365":
            self.code = self.BASIS_ACT365       
        elif basisName == "ACT/360":
            self.code = self.BASIS_ACT360
        elif basisName == "30/360US":
            self.code = self.BASIS_30360EU
        elif basisName == "30/360EU":
            self.code = self.BASIS_30360US
        elif basisName == "ACT/ACT":
            self.code = self.BASIS_ACTACT
        else:
            print("Error: Unknown basis type")
            
###############################################################################


class FinFlow(object):

    def __init__(self, date, amount):
        self.date = date
        self.amount = amount

    def dump(self):
        print("Date: ", self.date.string(), "Amount: ", self.amount)

###############################################################################

def datediff(d1, d2):

    diff = d2.excelDate - d1.excelDate
    return diff

###############################################################################

def isLeapYear(y):

    leapYear = ((y % 4 == 0) and (y % 100 != 0) or (y % 400 == 0))
    return leapYear

###############################################################################

def yearfrac(d1, d2, basis):

    basis = basis.upper()

    if basis == "ACT/365":

        accFactor = datediff(d1, d2) / 365.0

        return accFactor

    elif basis == "ACT/360":

        accFactor = datediff(d1, d2) / 360.0

        return accFactor

    elif basis == "30/360US":

        day2 = d2.d
        month2 = d2.m

        if day2 == 31 and day2 < 30:
            day2 = 1
            month2 = month2 + 1

        dayDiff = 360 * (d2.y-d1.y) + 30 * (month2-d1.m-1)
        + max(0, 30-d1.d) + max(30, day2)

        accFactor = dayDiff/360.0

        return accFactor

    elif basis == "30/360EU":

        dayDiff = 360 * (d2.y-d1.y) + 30 * (d2.m-d1.m1-1)
        + max(0, 30-d1.d) + max(30, d2.d)

        accFactor = dayDiff/360.0

        return accFactor

    elif basis == "ACT/ACT":

        if isLeapYear(d1.y):
            denom1 = 366
        else:
            denom1 = 365

        if isLeapYear(d2.y):
            denom2 = 366
        else:
            denom2 = 365

        # handle case in which period straddles year end
        accFactor = d2.y - d1.y - 1
        accFactor += datediff(d1, FinDate(1, 1, d1.y+1)) / denom1
        accFactor += datediff(FinDate(1, 1, d2.y), d2) / denom2

        return accFactor

    else:

        raise FinError("Basis code must be one of ACT/365, ACT/ACT,\
                        ACT/360, 30/360EU, 30/360US.")


###############################################################################

if __name__ == "__main__":

    print(DaysInYear)
