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
        self.prevFeatures = None

    def updateFeatures(self, prevFrameGray, frameGray):

        if self.prevFeatures is not None:

            features, status, error  = cv.calcOpticalFlowPyrLK(prevFrameGray, frameGray, self.prevFeatures, None, **self.lk_params)

            if np.any(status):  # Se verifica si se perdio al objeto
                error = False
            else:
                error = True
                features = None
                self.prevFeatures = None
        else:
            error = True
            features = None
        return features, error
