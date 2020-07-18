import cv2 as cv


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
        pass

    def updateFeatures(self,prevFrameGray,frameGray,STFeatures):
        next_, status, error  = cv.calcOpticalFlowPyrLK(prevFrameGray, frameGray, STFeatures, None, **self.lk_params)
        return [next_, status, error ]
