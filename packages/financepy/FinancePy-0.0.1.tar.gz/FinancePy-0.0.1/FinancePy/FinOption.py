# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:51:05 2016

@author: Dominic
"""

import FinUtils
from math import exp, log, sqrt
from FinDate import FinDate
from FinMath import normsdist, nprime
from scipy import optimize

###############################################################################

def f(volatility, *args):

    self = args[0]
    valueDate = args[1]
    stockPrice = args[2]
    divYield = args[3]
    interestRate = args[4]
    value = args[5]

    objFn = self.value(valueDate,stockPrice,divYield,volatility,interestRate) - value

    return objFn

###############################################################################

def vega(volatility, *args):

    self = args[0]
    valueDate = args[1]
    stockPrice = args[2]
    divYield = args[3]
    interestRate = args[4]

    fprime = self.vega(valueDate,stockPrice,divYield,volatility,interestRate)

    return fprime

###############################################################################


class Option(object):

###############################################################################

    def __init__ (self,
                  expiryDate,
                  strikePrice,
                  optionType ):

        self.expiryDate = expiryDate
        self.strikePrice = float(strikePrice)
        self.optionType = optionType.upper()

###############################################################################

    def value(self,
              valueDate,
              stockPrice,
              dividendYield,
              volatility,
              interestRate):

        t = FinUtils.datediff(valueDate,self.expiryDate)/FinUtils.DaysInYear

        lnS0k = log(float(stockPrice) / self.strikePrice)
        sqrtT = sqrt(t)

        if abs(volatility) < 0.0001:
            volatility = 0.0001

        d1 = lnS0k + (interestRate - dividendYield + volatility * volatility / 2.0) * t
        d1 = d1 / (volatility * sqrtT)

        d2 = lnS0k + (interestRate - dividendYield - volatility * volatility / 2.0) * t
        d2 = d2 / (volatility * sqrtT)

        if self.optionType == "CALL":
            v = stockPrice * exp(-dividendYield * t) * normsdist(d1)
            v = v - self.strikePrice * exp(-interestRate * t) * normsdist(d2)
        elif self.optionType == "PUT":
            v = self.strikePrice * exp(-interestRate * t) * normsdist(-d2)
            v = v - stockPrice * exp(-dividendYield * t) * normsdist(-d1)
        else:
            print("Unknown option type")

        return v

###############################################################################

    def delta(self,
              valueDate,
              stockPrice,
              dividendYield,
              volatility,
              interestRate):

        t = FinUtils.datediff(valueDate,self.expiryDate)/FinUtils.DaysInYear

        lnS0k = log(float(stockPrice) / self.strikePrice)
        sqrtT = sqrt(t)

        if abs(volatility) < 0.0001:
            volatility = 0.0001

        d1 = lnS0k + (interestRate - dividendYield + volatility * volatility / 2.0) * t
        d1 = d1 / (volatility * sqrtT)

        d2 = lnS0k + (interestRate - dividendYield - volatility * volatility / 2.0) * t
        d2 = d2 / (volatility * sqrtT)

        if self.optionType == "CALL":
            delta = exp(-dividendYield * t) * normsdist(d1)
        elif self.optionType == "PUT":
            delta = exp(-dividendYield * t) * (1.0 - normsdist(d1))
        else:
            print("Unknown option type")

        return delta

###############################################################################

    def vega(self,
              valueDate,
              stockPrice,
              divYield,
              volatility,
              interestRate):

        t = FinUtils.datediff(valueDate,self.expiryDate)/FinUtils.DaysInYear

        lnS0k = log(float(stockPrice) / self.strikePrice)
        sqrtT = sqrt(t)

        if abs(volatility) < 0.0001:
            volatility = 0.0001

        d1 = lnS0k + (interestRate - dividendYield + volatility * volatility / 2.0) * t
        d1 = d1 / (volatility * sqrtT)

        vega = stockPrice * sqrt(t) * exp(-dividendYield * t) * nprime(d1)

        return vega

###############################################################################

    def theta(self,
              valueDate,
              stockPrice,
              divYield,
              volatility,
              interestRate):

        v0 = self.value(valueDate,stockPrice,divYield,volatility,interestRate)

        nextDate = valueDate.addDays(1)

        v1 = self.value(nextDate,stockPrice,divYield,volatility,interestRate)

        dt = 1.0 / FinUtils.DaysInYear

        theta = (v1-v0)/dt

        return theta

###############################################################################


    def impliedVolatility(self,
              valueDate,
              value,
              stockPrice,
              divYield,
              interestRate):

        argtuple = (self,valueDate,stockPrice,divYield,interestRate,value)

        sigma = optimize.newton(f,x0=0.2, fprime=None, args=argtuple, tol=1e-8, maxiter=50, fprime2=None)

        sigma = optimize.newton(f,x0=0.2, fprime=vega, args=argtuple, tol=1e-8, maxiter=-50, fprime2=None)

        return sigma

###############################################################################

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    expiryDate = FinDate(1,1,2016)
    valueDate = FinDate(1,1,2015)
    stockPrice = 100
    volatility = 0.30
    interestRate = 0.05
    dividendYield = 0.0

    stockPrices = range(50,150)
    callOptionValues = []
    putOptionValues = []
    callOptionDeltas = []
    putOptionDeltas = []

    for stockPrice in stockPrices:

        callOption = Option(expiryDate, 100.0, "CALL")
        value = callOption.value(valueDate,stockPrice, dividendYield, volatility, interestRate)
        delta = callOption.delta(valueDate,stockPrice, dividendYield, volatility, interestRate)
        callOptionValues.append(value)
        callOptionDeltas.append(delta)

    for stockPrice in stockPrices:

        putOption = Option(expiryDate, 100.0, "PUT")
        value = putOption.value(valueDate,stockPrice, dividendYield, volatility, interestRate)
        delta = putOption.delta(valueDate,stockPrice, dividendYield, volatility, interestRate)
        putOptionValues.append(value)
        putOptionDeltas.append(delta)

    plt.figure()
    plt.plot(stockPrices, callOptionValues, color = 'b', label="Call Option")
    plt.plot(stockPrices, putOptionValues, color = 'r', label = "Put Option")
    plt.xlabel("Stock Price")
    plt.legend(loc='best')

    plt.figure()
    plt.plot(stockPrices, callOptionDeltas, color = 'b', label = "Call Option Delta")
    plt.plot(stockPrices, putOptionDeltas, color = 'r', label = "Put Option Delta")
    plt.xlabel("Stock Price")
    plt.legend(loc='best')

    callOption = Option(expiryDate, 100.0, "CALL")
    value = callOption.value(valueDate,stockPrice, dividendYield, volatility, interestRate)
    impliedVol = callOption.impliedVolatility(valueDate,value,stockPrice,dividendYield,interestRate)
    print("Implied Vol = ",impliedVol)
