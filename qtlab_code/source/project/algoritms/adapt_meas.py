__author__ = 'Jaap'
import numpy as np
from scipy import interpolate as intp
from matplotlib import pyplot as plt
class AdaptiveAlgoritm:
    '''
    Adaptive algoritm class used for optimized non-equidistant measurements. Measures more points in regions with higher slope than in regions with no slope.
    '''
    def __init__(self, xMin, xMax, yMeasureFunc):
        '''initialize the lists of x and y values
        @param xMin minimum x-value to measure
        @param xMax maximum x-value to measure
        @param yMeasureFunc the main measurement function of the form f(x) which returns a measured y-value for a given x.

        '''
        self.xCur = []
        self.yCur = []
        self.xMin = xMin
        self.xMax = xMax
        self.yMeasureFunc = yMeasureFunc

    def getNewPoint(self, nPoints = 1):
        '''determines which point to measure next based on the standard 2-D distance norm sqrt(dx^2,dy^2)
        :returns the requested point
        '''
        #
        if(len(self.xCur) != len(self.yCur)):
            print('Yvalues not set properly')
        else:
            startIndex = len(self.xCur)
            #now take the N points
            for i in range(0,nPoints):
                if len(self.xCur) == 0:
                    xNext = self.xMin
                elif len(self.xCur) == 1:
                    xNext = self.xMax
                else:
                    #create numpy arrays of the point list
                    xCurA = np.array(self.xCur)
                    yCurA = np.array(self.yCur)
                    yCurA = yCurA[np.argsort(xCurA)]
                    xCurA.sort()
                    #calculate the distances of each interval
                    dis = self.d(xCurA, yCurA)
                    #now measure a point in the middle of the largest distance
                    maxDisIndex = np.argmax(dis)
                    xNext = xCurA[maxDisIndex] + abs(xCurA[maxDisIndex+1] - xCurA[maxDisIndex]) / 2

                self.xCur.append(xNext)
                self.yCur.append(self.yMeasureFunc(xNext))
            return self.xCur[startIndex:]
    
    def d(self, xVec, yVec):
        '''calculates the distance norm between every point in the x and y vector
        :returns dis[i] = distance between point i and i-1'''
        xVecNorm = xVec / (np.max(xVec) - np.min(xVec))
        yVecNorm = yVec / (np.max(yVec) - np.min(yVec))
    
        #calculate the distance norm taken the x-distance y-distance and 2nd order derivative in accoutn
        dis = np.sqrt(np.diff(xVecNorm) ** 2 + np.diff(yVecNorm) ** 2)
        return dis

    def sort(self):
        '''sorts the xCur and yCur list'''
        xCurA = np.array(self.xCur)
        yCurA = np.array(self.yCur)
        self.yCur = yCurA[np.argsort(xCurA)].tolist()
        self.xCur.sort()

    def plotValues(self, mark = 'x'):
        '''plots the current x-values vs current yvalues with the given mark'''
        self.sort()
        plt.figure()
        plt.plot(self.xCur,self.yCur, mark)
        plt.show()


