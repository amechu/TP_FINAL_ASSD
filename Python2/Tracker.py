import cv2 as cv
import numpy as np
import KalmanFilter
import ColorFilter
import ShiTomasi
import OpticalFlow


class Tracker:
    LIG_THR_EVERY_FRAMES = 15

    def __init__(self, initialPosition, initialWidth, initialHeight):
        self.LK= OpticalFlow.OpticalFlow()
        self.ST= ShiTomasi.ShiTomasi()
        self.KM = KalmanFilter.KalmanFilter()
        self.ColF=ColorFilter.ColorFilter()

        self.KM.setStatePost(np.array([initialPosition[0], initialPosition[1], 0., 0.]).reshape(4, 1))
        self.selectionWidth = initialWidth
        self.selectionHeight = initialHeight
        self.searchWidth = 0
        self.searchHeight = 0
        self.trackingError = False
        self.prevFrameGray = None
        self.stdMultiplier = 1
        self.frameCounter = 0
        self.features = 0   #Shape = {tuple}: (x, 1, 2)
                                    #Por ejemplo: [[[x1 y1]]\n\n [[x2 y2]]\n\n [[x3 y3]]]
                                    #es decir una matriz de x filas y 1 columna, donde cada elemento
                                    #de la unica columna es una coordenada [x y].
    def update(self, frame):

        self.frameCounter += 1
        self.KM.predict()

        if self.ColF.colorFilterUse is True:
            pass
        #falta toddo lo de filtro de color

        frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if self.trackingError is True:
            self.features, self.trackingError = self.ST.recalculateFeatures(frameGray[self.KM.statePost[1] - self.searchHeight/2 : self.KM.statePost[1] + self.searchHeight/2,
                                                                                                                          self.KM.statePost[0] - self.searchWidth/2 : self.KM.statePost[0] + self.searchWidth/2])
            if self.trackingError is True:
                self.enlargeSearchArea()
                return
            else:
                self.searchHeight = self.selectionHeight
                self.searchWidth = self.selectionWidth
                self.KM.correct(np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1]))

        self.features, self.trackingError = self.LK.updateFeatures(self.prevFrameGray, frameGray)

        if self.trackingError is True:
            return

        if self.frameCounter != 0 and self.frameCounter % self.ST.frameRecalculationNumber == 0:
            medx, medy = np.median(self.features[:, 0, 0]), np.median(self.features[:, 0, 1])
            std = np.sqrt((np.std(self.features[:, 0, 0]))**2 + (np.std(self.features[:, 0, 1]))**2)
            mask = (self.features[:, 0, 0] < medx + self.stdMultiplier * std) & (self.features[:, 0, 0] > medx - self.stdMultiplier * std) & (
                          self.features[:, 0, 1] < medy + self.stdMultiplier * std) & (self.features[:, 0, 1] > medy - self.stdMultiplier * std)
            self.features = self.features[mask]
            mux, muy = np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1])
            self.features, self.trackingError = self.ST.recalculateFeatures(frameGray[muy - self.selectionHeight / 2: muy + self.selectionHeight / 2,
                                                                                                                          mux - self.selectionWidth / 2: mux + self.selectionWidth / 2])
            if self.trackingError is True:
                return
            else:
                self.KM.correct(np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1]))
                return

        else:
            self.KM.correct(np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1]))
            return


    def enlargeSearchArea(self):
        self.searchWidth += self.ST.searchEnlargementThreshold
        self.searchHeight += self.ST.searchEnlargementThreshold

    def getEstimatedPosition(self):
        return self.KM.statePost[0], self.KM.statePost[1]

    def getEstimatedVelocity(self):
        return self.KM.statePost[2], self.KM.statePost[3]

    def getFilteredFrame(self):
        pass

    def filterFrame(self):
        pass




