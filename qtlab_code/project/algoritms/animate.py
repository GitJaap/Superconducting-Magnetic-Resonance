'''
Created on 23 okt. 2014

@author: Jaap
'''
import numpy
from pylab import *

import matplotlib.pyplot as plt
import matplotlib.animation as ani;
from measurement.interpol import linInterpolate2D, linInterpolate1D
from measurement.flread import FileReader
from measurement.meas import MeasureFromFile
from algoritms import deriv_peak
from algoritms import lev_alg;

def animateAlg(xStart, xEnd, nPoints = 1000, algGetNewPointFunc = lev_alg.getNewPoint, nRough = 0, *yMeasureArgs, **keyArgs):
    '''runs the given algoritm and plots the points taken one by one
    @param xStart: Starting x-coordinate of the measurement
    @param xEnd: Highest x-coordinate of the measurement
    @param nPoints: Total amount of points to be taken in the measurement
    @param algGetNewPointFunc: function which is called every iteration to get the next x,y values from 
    @param nRough: Points taken for a rough initial scan  '''
    
    
    fig, ax = plt.subplots();
    line, = ax.plot(linspace(xStart,xEnd,nPoints),ones(nPoints), 'x');
    xCur = []; #current measured points x values
    yCur = []; #current measured points y value
    
    #check which kind of measurement is required
    if('file' in keyArgs):
        fileIn =  keyArgs['file'];
    else:
        fileIn = False;
    if('vector' in keyArgs):
        vectorIn = keyArgs['vector']
    else:
        vectorIn = False;

    def animate(i,xCur,yCur):
        xCur, yCur = algGetNewPointFunc(xCur, yCur, xStart, xEnd, nPoints, nRough, yMeasureArgs[0],yMeasureArgs[1], file = fileIn, vector = vectorIn,);
        line.set_xdata(xCur);
        line.set_ydata(yCur);
        return line;
    #animate the measurement protocol in a figure
    ani.FuncAnimation(fig, animate, np.arange(0,nPoints), interval = 1, repeat = False, fargs = [xCur,yCur]);
    show();








#first load the data from file an example peak is now taken
xvec = np.linspace(10,50,10000);
gamma = 0.1; #scale factor
variance = 0.3; #noise variance
x0 = 31; #peak position
#now simulate a lorentzian and plot it for reference
yvec = 1 / (np.math.pi * gamma * (1 + ((xvec - x0)/gamma)*((xvec - x0)/gamma)));
x0 = 40;
yvec = yvec+ 1 / (np.math.pi * gamma * (1 + ((xvec - x0)/gamma)*((xvec - x0)/gamma)));
x0 = 16;
yvec = yvec+ 1 / (np.math.pi * gamma * (1 + ((xvec - x0)/gamma)*((xvec - x0)/gamma)));
x0 = 46;
yvec = yvec+ 1 / (np.math.pi * gamma * (1 + ((xvec - x0)/gamma)*((xvec - x0)/gamma)));

#add some normal noise
yvec = yvec + variance * np.random.randn( len( yvec));
figure(1);
plot(xvec,yvec);
xMin = min(xvec); #minimum value of the region of interest
xMax = max(xvec); #maximum value of the region of interest
nPoints = 400; #total points to measure
nRough = 80; #amount of points used for rough estimate

animateAlg(xvec[0], xvec[-1], nPoints, lev_alg.getNewPoint, nRough, xvec, yvec, vector = True );