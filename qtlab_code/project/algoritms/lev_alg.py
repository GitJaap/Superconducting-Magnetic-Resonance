'''
Created on 23 okt. 2014

Leverage algoritm function used to determine how different each point is from the
rest of the points, by using singular value decomposition of a symmetric difference matrix

@author: Jaap
'''
from numpy import *;
from measurement.meas import MeasureFromVecs
from matplotlib.pyplot import *;

def calcLeverage(yVec, k = 2):
    '''calculates the leverage of each point in the y-vector and outputs that as a vector of the same size by using the first k vectors'''
    #start with creating the difference matrix 
    nPoints = len(yVec);
    #create the distance matrix
    M = zeros((nPoints,nPoints));
    variance = var(yVec);
    for i in range(0,nPoints):
        M[:,i] = abs(yVec-yVec[i])/variance;

    #calculate the svd composition
    u, s , v = linalg.svd(M);

    #calculate the leverage of each column to determine the points of interest
    lev = (1/float(k))* sum(abs(v[0:k,:])*abs(v[0:k,:]),0);
    return lev;

def getNewPoint(xCur,yCur,xStart,xEnd, nPoints, nRough, *yMeasureArguments, **keyArgs):
    '''determines which point to measure next based on the previous points(uses vectors as measurement simulation)'''
    #first convert the lists to arrays for computational simplicity
    xCurA = array(xCur);
    yCurA = array(yCur);
    #check if the list is not empty
    if(len(xCur) == 0):
        xNext = xStart+(xEnd-xStart)/nRough;
    #First iterate through the rough measurement
    elif(len(xCur) < nRough):
        xNext = xCur[-1] + (xEnd-xStart)/nRough;
    #now try to find the peak and take points in that region
    elif(len(xCur) == nRough):
        #create global variables to be used by the function when called again
        global xPeaks
        global nPeaks
        global xStarts;
        global xEnds;
        global counter;
        counter = 0;
        
        #calculate the leveage for each point of the graph.
        lev = calcLeverage(yCurA[:,0],2)
    
        #determine the peaks x-position
        xPeaks = xCurA[where(lev > max(lev)/2)];
        nPeaks = len(xPeaks);
        print('%d peaks have been found ' % nPeaks);
        xStarts = zeros(nPeaks,dtype=float); 
        xEnds = zeros(nPeaks,dtype=float);
        
        #now iterate through all peaks to determine the new measurement ranges
        for i in range(0,nPeaks):
            xStarts[i] = xPeaks[i]-(xEnd-xStart)/nRough*1.5;
            xEnds[i] = xPeaks[i]+(xEnd-xStart)/nRough*1.5;
        #set the new starting position at the first peak encountered    
        xNext = xStarts[0];
    #the peaks have been found so the precise measurement can be started
    if(len(xCur) > nRough):
        #check if one peak has been fully measured
        if(xCurA[-1] >= xEnds[counter]):
            counter =counter + 1;
            xNext = xStarts[counter]
        else:
            xNext = xCurA[-1]+(xEnds[counter]-xStarts[counter])/((nPoints-nRough)/nPeaks);
        
    #check which kind of measurement is required
    if('file' in keyArgs):
        file =  keyArgs['file'];
    else:
        file = False;
    if('vector' in keyArgs):
        vector = keyArgs['vector']
    else:
        vector = False;
        
    #do the measurement as determined in keyargs
    if(file):
        pass;
    elif(vector):
        yNext = MeasureFromVecs([xNext],yMeasureArguments[0],yMeasureArguments[1]);
    else:
        raise Exception('No y measurement specified!')
    yCur.append(yNext);
    xCur.append(xNext);
    return xCur,yCur; 