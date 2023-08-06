# -*- coding: utf-8 -*-
"""
Created on Sun Feb 07 14:31:53 2016

@author: Dominic
"""

import math
from scipy.stats import norm

################################################################################

def scale(x,factor):

    for i in range(0,len(x)):
        x[i]=x[i] * factor
        
    return x
    
################################################################################

def normsdist(x, method=0):

    # I allow different implementations
    # This one comes from book by Hull

    if method == 0:
        return phiHull(x)
    else:
        return norm.cdf(x)

################################################################################

def nprime(x):

    x = float(x)
    InvRoot2Pi = 0.3989422804014327
    y = math.exp(-x*x/2.0) * InvRoot2Pi
    return y

################################################################################

def phiHull(x):

    a1 = 0.319381530
    a2 = -0.356563782
    a3 = 1.781477937
    a4 = -1.821255978
    a5 = 1.330274429
    g = 0.2316419

    k = 1.0 / (1.0 + g * math.fabs(x))
    k2 = k * k
    k3 = k2 * k
    k4 = k3 * k
    k5 = k4 * k

    if x >= 0.0:
        c = (a1 * k + a2 * k2 + a3 * k3 + a4 * k4 + a5 * k5)
        phi = 1.0 - c * nprime(x)
    else:
        phi = 1.0 - phiHull(-x)

    return phi

################################################################################

def frange(start, stop, step):
    x = []
    while start <= stop:
        x.append(start)
        start += step

    return x

#################################################################################

if __name__ == "__main__":
   
    import matplotlib.pyplot as plt
    
    xValues = frange(-3.0,3.0,0.10)
    yValues = []

    for x in xValues:

        y = normsdist(float(x))
        yValues.append(y)

   
    plt.plot(xValues, yValues, color = 'b')
    plt.show()
    
    plt.cla

    from timeit import default_timer as timer
    
    start = timer()
    
    for i in xrange(-1000,1000):
        x = float(i)/1000.0
        cdf = normsdist(x,0)
    end = timer()
    
    print (end-start)
    
    for i in xrange(-10000,10000):
        x = float(i)/1000.0
        cdf = normsdist(x,1)
    end = timer()
    
    print (end-start)
