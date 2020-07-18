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

        self.KM.statePost = np.array([initialPosition[0], initialPosition[1], 0., 0.]).reshape(4, 1)
        self.selectionWidth = initialWidth
        self.selectionHeigth = initialHeight
        self.searchWidth = 0
        self.searchHeight = 0
        self.trackingError = False
        self.prevFrameGray = None
        self.frameCounter = 0
        self.features = 0

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
                self.searchHeight = self.selectionHeigth
                self.searchWidth = self.selectionWidth
                self.KM.correct(*np.mean(self.features, axis=0))

        self.features, self.trackingError = self.LK.updateFeatures(self.prevFrameGray, frameGray)

        if self.trackingError is True:
            return

        if self.frameCounter != 0 and self.frameCounter % self.ST.frameRecalculationNumber == 0:
            mux, muy = np.mean(self.features, axis=0)
            std = np.sqrt(np.power(np.std(self.features, axis = 0), 2), np.power(np.std(self.features, axis=0), 2))
            #falta eliminar outliers de self.features, volver a calcular la media, y aplicar shitomasi al rededor de esa media
            #si se encuentran mierdas con shitomasi, hacer un kalman correct y si no poner trackingError en false.
        else:
            self.KM.correct(*np.mean(self.features, axis=0)) #dudosa implementasion
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




