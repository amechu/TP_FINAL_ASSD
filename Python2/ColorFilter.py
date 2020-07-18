import cv2 as cv


class ColorFilter:
    hSemiAmp = 0
    SemiAmp = 0
    vSemiAmp = 0
    LIG_THR_CHANGE = 1

    def __init__(self):
        self.filteredFrame = 0
        self.H = 0
        self.S = 0
        self.V = 0

    def calculateNewMask(self, selection):
        pass

    def filterFrame(self, frame):
        pass


