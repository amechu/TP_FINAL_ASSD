import cv2 as cv
import numpy as np


class OpticalFlow:


    def __init__(self):
        self.prevFeatures = None
        self.lkMaxLevel = 5
        self.lkWinSize = (15, 15)

        self.lkCriteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT,10,    0.03)
        self.lk_params = dict(winSize=self.lkWinSize,
                         maxLevel=self.lkMaxLevel,  # Niveles del arbol maximos
                         criteria=self.lkCriteria)

    def updateFeatures(self, prevFrameGray, frameGray):
        self.lk_params = dict(winSize=self.lkWinSize,
                              maxLevel=self.lkMaxLevel,  # Niveles del arbol maximos
                              criteria=self.lkCriteria)
        if self.prevFeatures is not None:

            features, status, error  = cv.calcOpticalFlowPyrLK(prevFrameGray, frameGray, self.prevFeatures, None, **self.lk_params)

            if np.any(status):  # Se verifica si se perdio al objeto
                trackerror = False
                good_new = features[status == 1]
                features = good_new.reshape(-1, 1, 2)
                self.prevFeatures=features
            else:
                trackerror = True
                features = None
                self.prevFeatures = None
        else:
            trackerror = True
            features = None
        return features, trackerror
