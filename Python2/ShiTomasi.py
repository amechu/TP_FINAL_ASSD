import cv2 as cv


class ShiTomasi:
    maxcorners=1000
    qLevel=0.00000001
    minDist = 10
    blockSize_ = 10
    RECALC_EVERY_FRAMES = 20

    feature_params = dict(maxCorners=maxcorners,  # Maxima cantidad de features
                          qualityLevel=qLevel,
                          # Nivel de calidad minimo de cada feature entre 0 y 1. En 0 se devuelven TODAS las features no importa la calidad
                          minDistance=minDist,  # Minima distancia entre features
                          blockSize=blockSize_)

    def __init__(self):
        self.features = None

    def getFeatures(self):
        return self.features

    def recalculateFeatures(self, selection): #selection = prev_gray[y:y + h, x:x + w]
        self.features = cv.goodFeaturesToTrack(selection, mask=None, **self.feature_params)
        return self.features







