__author__ = 'Jaap'
import numpy as np
from scipy import interpolate as intp
def getNewPoint(xCur, yCur, xMin, xMax, Npoints = 0, nRough = 0):
    '''determines which point to measure next based on the standard 2-D distance norm sqrt(dx^2,dy^2)
    :returns xCur list with current xValues with one value added
    '''
    #
    if len(xCur) == 0:
        xNext = xMin
    elif len(xCur) == 1:
        xNext = xMax
    elif len(xCur) == 2:
        xNext = xMin + (xMax - xMin) / 2
    else:
        #create numpy arrays of the point list
        xCurA = np.array(xCur)
        yCurA = np.array(yCur)
        yCurA = yCurA[np.argsort(xCurA)]
        xCurA.sort()
        #calculate the distances of each interval
        dis = d(xCurA, yCurA)
        #now measure a point in the middle of the largest distance
        maxDisIndex = np.argmax(dis)
        xNext = xCurA[maxDisIndex] + abs(xCurA[maxDisIndex+1] - xCurA[maxDisIndex]) / 2

    xCur.append(xNext)
    return xCur

def d(xVec, yVec):
    '''calculates the distance norm between every point in the x and y vector
    :returns dis[i] = distance between point i and i-1'''
    xVecNorm = xVec / (np.max(xVec) - np.min(xVec))
    angles = np.arctan(np.diff(yVec) / np.diff(xVec))
    anglesNorm = angles/(np.max(angles) - np.min(angles))


    #calculate the distance norm taken the x-distance y-distance and 2nd order derivative in accoutn
    dis = np.sqrt(np.diff(xVecNorm) ** 2 + np.diff(anglesNorm) ** 2)
    return dis
