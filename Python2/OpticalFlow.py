import cv2 as cv
import numpy as np


class OpticalFlow:
    lkWinSize=(15,15)
    lkMaxLevel=5
    lkCriteria= (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT,
                               10,
                               0.03)
    lk_params = dict(winSize=lkWinSize,
                     maxLevel=lkMaxLevel,  # Niveles del arbol maximos
                     criteria=lkCriteria)
    def __init__(self):
        self.prevFeaturesLK = None

    def updateFeatures(self, prevFrameGray, frameGray):

        newFeaturesLK, status, error  = cv.calcOpticalFlowPyrLK(prevFrameGray, frameGray, self.prevFeaturesLK, None, **self.lk_params)

        if np.any(status):  # Se verifica si se perdio al objeto
            error = False
            newFeatures = newFeaturesLK[status == 1]
            self.prevFeaturesLK = newFeatures.reshape(-1, 1, 2)
        else:
            error = True
            newFeatures = 0
            self.prevFeaturesLK = 0

        return newFeatures, error
