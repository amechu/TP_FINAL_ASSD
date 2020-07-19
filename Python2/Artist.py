import cv2 as cv
import numpy as np
class Artist:

    @staticmethod
    def estimate(frame, x, y, width, height, color): #color (255, 255, 255)

        cv.rectangle(frame, (int(x - (width / 2)), int(y - (height / 2))),
                     (int(x + (width / 2)), int(y + (height / 2))), color, 4)
        return frame

    @staticmethod
    def features(frame, features):
        for i in range(np.shape(features)[0]):
            cv.circle(frame, (features[i,0,0], features[i, 0, 1]), 3, (0, 255, 0), -1)
        return frame

    @staticmethod
    def trajectory(frame, pointArray):

        for i in range(np.shape(pointArray)[0]): #[[x y],[x y],[x y]]
            cv.circle(frame, pointArray[i], 3, (0, 0, 255), -1)
        return frame

    @staticmethod
    def searchArea(frame, x, y, width, height, color):
        cv.rectangle(frame, (int(x - (width / 2)), int(y - (height / 2))),
                     (int(x + (width / 2)), int(y + (height / 2))), color, 4)
        return frame

    @staticmethod
    def filterMask(frame, lowerThreshold, upperThreshold): #threshold es tipo (255, 255, 255)
        mask = cv.inRange(frame, lowerThreshold, upperThreshold)
        frame = cv.bitwise_and(frame, frame, mask=mask)
        return frame