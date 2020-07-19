import cv2 as cv


class ShiTomasi:
    maxcorners=5
    qLevel=0.00000001
    minDist = 10
    blockSize_ = 10
    frameRecalculationNumber = 2
    searchEnlargementThreshold = 4

    feature_params = dict(maxCorners=maxcorners,  # Maxima cantidad de features
                          qualityLevel=qLevel,
                          # Nivel de calidad minimo de cada feature entre 0 y 1. En 0 se devuelven TODAS las features no importa la calidad
                          minDistance=minDist,  # Minima distancia entre features
                          blockSize=blockSize_)

    def __init__(self):
        pass

    def recalculateFeatures(self, selection): #selection = prev_gray[y:y + h, x:x + w]
        features = cv.goodFeaturesToTrack(selection, mask=None, **self.feature_params)
        if features is not None:
            error = False
        else:
            error = True
        return features, error







