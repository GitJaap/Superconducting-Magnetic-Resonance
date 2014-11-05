'''
Created on 29 okt. 2014

@author: Jaap
'''
import os;
import sys;
sys.path.append(os.path.split(os.getcwd())[0]);
from measurement.flread import FileReader
from pylab import *
from algoritms.lev_alg import calcLeverage
print('main is started within QTLab!');

#first load the data from file an example peak is now taken
xvec = np.linspace(10,50,100);
gamma = 0.3; #scale factor
variance = 0.1; #noise variance
x0 = 31; #peak position
#now simulate a lorentzian and plot it for reference
yVec = 1 / (np.math.pi * gamma * (1 + ((xvec - x0)/gamma)*((xvec - x0)/gamma)));
x0 = x0+3;
yVec = yVec +  1 / (np.math.pi * gamma * (1 + ((xvec - x0)/gamma)*((xvec - x0)/gamma)));
#add some white noise
yVec = yVec + variance * np.random.randn( len( yVec));
figure(1);
plot(xvec,yVec);

lev = calcLeverage(yVec);

figure(2)
poi = xvec[lev > max(lev)/10]

plot(xvec,lev);
show();
'''

fr = FileReader('..//resources//res01TopoHanger_pow-10.dat');
data = fr.readColumns([0,3], separator = ' ');

plot(data[0:(len(data[:,0])-1),0],diff(data[:,1]));
lev = calcLeverage(diff(data[:,1]));
figure(2)
plot(data[0:(len(data[:,0])-1),0],lev)
show();
'''