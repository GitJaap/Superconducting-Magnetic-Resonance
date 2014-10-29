'''
Created on 29 okt. 2014

@author: Jaap
'''
import os;
from measurement.flread import FileReader
from pylab import *
print('main is started within QTLab!');

flr = FileReader('..//resources//res01TopoHanger_pow-10.dat');
readData = flr.readColumns([0,3],separator = ' ');

readData[:,1] = readData[:,1] - np.mean(readData[:,1]);
plot(readData[:,0],readData[:,1]);
show();


execfile(os.path.join(os.path.split(os.getcwd())[0],'algoritms/animateAlgoritms.py'));