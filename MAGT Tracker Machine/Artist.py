import cv2 as cv
import numpy as np
class Artist:

    @staticmethod
    def estimate(frame, x, y, width, height, color): #color (255, 255, 255)

        #cv.rectangle(frame, (int(x - (width / 2)), int(y - (height / 2))),
                     #(int(x + (width / 2)), int(y + (height / 2))), color, 2)
        cv.circle(frame, (int(x), int(y)), np.max([int(height/2), int(width/2)]), color, 2)
        return frame

    @staticmethod
    def features(frame, features, color):
        for i in range(np.shape(features)[0]):
            cv.circle(frame, (features[i,0,0], features[i, 0, 1]), 2, color, -1)
        return frame

    @staticmethod
    def trajectory(frame, pointArray, color,persistance=True):
        overlay = frame.copy()
        pointArray = pointArray[-80:] #descomentar esto para que la linea dure como maximo 99 frames
        for i in range(np.shape(pointArray)[0]): #[[x y],[x y],[x y]]
            if not color:
                cv.line(overlay, pointArray[i-1], pointArray[i], (0,0,255), 2)
            else:
                cv.line(overlay, pointArray[i-1], pointArray[i], color, 2)
            if persistance:
                #cv.circle(frame, pointArray[i], 3, color, -1)
                alpha = i/len(pointArray)  # Transparency factor.
                # Following line overlays transparent rectangle over the image
                overlay = cv.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        return overlay

    @staticmethod
    def searchArea(frame, x, y, width, height, color):
        cv.rectangle(frame, (int(x - (width / 2)), int(y - (height / 2))),
                     (int(x + (width / 2)), int(y + (height / 2))), color, 1)
        return frame

    @staticmethod
    def filterMask(frame, lowerThreshold, upperThreshold): #threshold es tipo (255, 255, 255)
        mask = cv.inRange(frame, lowerThreshold, upperThreshold)
        frame = cv.bitwise_and(frame, frame, mask=mask)
        return frame