import cv2 as cv


class ShiTomasi:
    maxcorners=20
    qLevel=0.00001
    minDist = 10
    blockSize_ = 5
    frameRecalculationNumber = 20
    searchEnlargementThreshold = 6

    # feature_params = dict(maxCorners=maxcorners,  # Maxima cantidad de features
    #                       qualityLevel=qLevel,
    #                       # Nivel de calidad minimo de cada feature entre 0 y 1. En 0 se devuelven TODAS las features no importa la calidad
    #                       minDistance=minDist,  # Minima distancia entre features
    #                       blockSize=blockSize_)

    def __init__(self):
        pass

    def recalculateFeatures(self, selection): #selection = prev_gray[y:y + h, x:x + w]
        feature_params = dict(maxCorners=int(self.maxcorners),  # Maxima cantidad de features
                              qualityLevel=self.qLevel,
                              # Nivel de calidad minimo de cada feature entre 0 y 1. En 0 se devuelven TODAS las features no importa la calidad
                              minDistance=int(self.minDist),  # Minima distancia entre features
                              blockSize=int(self.blockSize_))
        features = cv.goodFeaturesToTrack(selection, mask=None, **feature_params)
        if features is not None:
            error = False
        else:
            error = True
        return features, error









