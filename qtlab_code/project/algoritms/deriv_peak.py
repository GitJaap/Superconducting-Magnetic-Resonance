'''
Created on 23 okt. 2014

@author: Jaap
'''
from numpy import *;
from measurement.meas import MeasureFromVecs

def getNewPoint(xCur,yCur,xStart,xEnd,yMeasureFunc,nPoints,nRough):
    '''determines which point to measure next based on the previous points(uses vectors as measurement simulation)'''
    #first convert the lists to arrays for computational simplicity
    xCurA = array(xCur);
    yCurA = array(yCur);
    #check if the list is not empty
    if(len(xCur) == 0):
        xNext = xVec[0]+(xVec[-1]-xVec[0])/nRough;
        yNext = MeasureFromVecs(xVec,yVec,[xNext]); #measurement simulation
    #First iterate through the rough measurement
    elif(len(xCur) < nRough):
        xNext = xCur[-1] + (xVec[-1]-xVec[0])/nRough;
        yNext = MeasureFromVecs(xVec,yVec,[xNext]); #measurement simulation
    #now try to find the peak and take points in that region
    elif(len(xCur) == nRough):
        #create an approximate derivative
        yDiff = (yCurA[1:len(yCurA)]-yCurA[0:len(yCurA)-1])/((xVec[-1]-xVec[0])/nRough)
        #get the peak from the current data by determining the average derivative and subtracting all values from that
        yDiff = abs(mean(yDiff)-yDiff);
        xPeak = xCurA[argmax(yDiff)];
        print(xPeak);
        global newXMin;
        global newXMax; 
        newXMin = xPeak-(xVec[-1]-xVec[0])/nRough*2.5;
        newXMax = xPeak+(xVec[-1]-xVec[0])/nRough*2.5;
        xNext = newXMin;
        yNext = MeasureFromVecs(xVec,yVec,[xNext]);
    if(len(xCur) > nRough):
        xNext = xCurA[-1]+(newXMax-newXMin)/(nPoints-nRough);
        yNext = MeasureFromVecs(xVec,yVec,[xNext]);
        
    xCur.append(xNext);
    yCur.append(yNext);
    return xCur,yCur;