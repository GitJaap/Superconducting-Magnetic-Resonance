'''
Created on 23 okt. 2014

Leverage algoritm function used to determine how different each point is from the
rest of the points, by using singular value decomposition of a symmetric difference matrix

@author: Jaap
'''
from numpy import *
from project.measurement.meas import MeasureFromVecs
from matplotlib.pyplot import *
import pylab as pl

def calcLeverage(yVec, k = 2):
    '''calculates the leverage of each point in the y-vector and outputs that as a vector of the same size by using the first k vectors'''
    #start with creating the difference matrix 
    nPoints = len(yVec)
    #create the distance matrix
    M = zeros((nPoints,nPoints))
    variance = abs(var(yVec))
    for i in range(0,nPoints):
        M[:,i] = abs(yVec-yVec[i])/variance

    #calculate the svd composition
    u, s , v = linalg.svd(M)

    #calculate the leverage of each column to determine the points of interest
    lev = (1/float(k))* sum(abs(v[0:k,:])*abs(v[0:k,:]),0)
    return lev

def getNewPoint(xCur, yCur, xMin, xMax, nPoints, nRough):
    '''
    determines which point to measure next based on the previous points(uses vectors as measurement simulation)
    :returns the list of xValues with one more value added
    '''
    #first convert the lists to arrays for computational simplicity
    xCurA = array(xCur)
    yCurA = array(yCur)
    #check if the list is not empty
    if(len(xCur) == 0):
        xNext = xMin + (xMax - xMin) / nRough
    #First iterate through the rough measurement
    elif(len(xCur) < nRough):
        xNext = xCur[-1] + (xMax-xMin)/nRough
    #now try to find the peak and take points in that region
    elif(len(xCur) == nRough):
        #create global variables to be used by the function when called again
        global weights
        global pointsPerInterval #array of desired points to be measured for each interval
        global intervalCounter
        global pointsInIntervalCounter
        global xRough #store the rough scan x points used for the interval measurements
        global dRough

        weights = zeros(len(xCurA)-1)
        pointsPerInterval = zeros(len(xCurA)-1)
        xRough = xCurA
        dRough = xRough[1]-xRough[0]
        intervalCounter = 0
        pointsInIntervalCounter = 1
        #calculate the leverage on the derivative for each point of the graph.
        lev = calcLeverage(gradient(yCurA),2)
        #determine the weight of each interval using the 6 points around the interval starting at [x3,x4]
        for i in range(2,len(weights)-2):
            weights[i] = (1 / 4) * lev[i-2] + (1 / 2) * lev[i-1] + 2*lev[i] + 2*lev[i+1] + (1 / 2) * lev [i + 2] + (1 / 4) * lev [i + 3]

        #also give the weights at the edges
        weights[0] = lev[0] + lev[1] + (1 / 2) * lev[2] + (1 / 4) * lev[3]
        weights[1] = (1 / 2) * lev[0] + lev[1] + lev[2] + (1 / 2) * lev[3] + (1 / 4) * lev[4]
        weights[-1] = lev[-1] + lev[-2] + (1 / 2) * lev[-3] + (1 / 4) * lev[-4]
        weights[-2] = (1 / 2) * lev[-1] + lev[-2] + lev[-3] + (1 / 2) * lev[-4] + (1 / 4) * lev[-5]
        #normalize the weights
        weights = weights/sum(weights)
        #spread the measurement points according to the weights found.
        for i in range(0,len(weights)):
            pointsPerInterval[i] = round(weights[i]* (nPoints-nRough+1))

        xNext = xRough[0] + dRough / (pointsPerInterval[0]+1)
        print(pointsPerInterval)
        '''
        figure(3)
        plot(xRough[1:]-dRough/2,pointsPerInterval)
        pl.show()
        '''
    #the weights have been calculated so the precise measurement can be started
    if(len(xCur) > nRough):
        #check if one interval has been fully measured
        i = intervalCounter #improve code readability
        j = pointsInIntervalCounter
        if(pointsPerInterval[intervalCounter] > pointsInIntervalCounter):
            xNext = xRough[i] + (dRough / ((pointsPerInterval[i]+1)) * (j+1))
            pointsInIntervalCounter += 1
        else:
            if(i == len(xRough)-1):
                xNext = xRough[-1]
            else:
                xNext = xRough[i+1]+ (dRough / (pointsPerInterval[i] + 1))
                intervalCounter += 1
                pointsInIntervalCounter = 1

    xCur.append(xNext)
    return xCur