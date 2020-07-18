import cv2 as cv
import kalman
import ColorFilter
import ShiTomasi
import OpticalFlow

class Tracker:
    LIG_THR_EVERY_FRAMES = 15
    SEARCHING_ENLARGEMENT = 4  # Rapidez con la que se agranda el area de busqueda

    def __init__(self):
        LK= OpticalFlow
        ST= ShiTomasi
        KM= kalman
        ColF=ColorFilter

    def update(self):
        pass

    def getEstimate(self):
        pass

    def getFeatures(self):
        pass

    def getFilteredFrame(self):
        pass

    def filterFrame(self):
        pass




