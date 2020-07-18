import cv2 as cv
import KalmanFilter
import ColorFilter
import ShiTomasi
import OpticalFlow

class Tracker:
    LIG_THR_EVERY_FRAMES = 15
    SEARCHING_ENLARGEMENT = 4  # Rapidez con la que se agranda el area de busqueda

    def __init__(self):
        self.LK= OpticalFlow.OpticalFlow()
        self.ST= ShiTomasi.ShiTomasi()
        self.KM = KalmanFilter.KalmanFilter()
        self.ColF=ColorFilter.ColorFilter()

    def update(self, prevFrame, frame):
        pass

    def getEstimatedPosition(self):
        return self.KM.statePost[0], self.KM.statePost[1]

    def getEstimatedVelocity(self):
        return self.KM.statePost[2], self.KM.statePost[3]

    def getFeatures(self):
        return self.ST.getFeatures()

    def getFilteredFrame(self):
        pass

    def filterFrame(self):
        pass




