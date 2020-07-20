import cv2 as cv
import numpy as np
from KalmanFilter import KalmanFilter
from MaskingFilter import MaskingFilter
from ShiTomasi import ShiTomasi
from OpticalFlow import OpticalFlow
from Searcher import Searcher

class Tracker:
    LIG_THR_EVERY_FRAMES = 15

    def __init__(self, initialPosition, initialWidth, initialHeight,frame):

        #########################################

        #########################################
        frameReal = frame
        self.KM = KalmanFilter()
        self.MF= MaskingFilter()
        self.KM.setStatePost(np.array([initialPosition[0], initialPosition[1], 0., 0.]).reshape(4, 1))
        self.selectionWidth = initialWidth
        self.selectionHeight = initialHeight

        self.prevFrameGray = None
        self.stdMultiplier = 1
        self.frameCounter = 0  #Shape = {tuple}: (x, 1, 2)
                                    #Por ejemplo: [[[x1 y1]]\n\n [[x2 y2]]\n\n [[x3 y3]]]
                                    #es decir una matriz de x filas y 1 columna, donde cada elemento
                                    #de la unica columna es una coordenada [x y].
        if self.MF.mask is not self.MF.maskingType["FILTER_OFF"]:
            self.MF.calculateNewMask(frame, frame[int(initialPosition[1] - initialHeight / 2): int(
            initialPosition[1] + initialHeight / 2), int(initialPosition[0] - initialWidth / 2): int(
            initialPosition[0] + initialWidth / 2)])
            frame = self.MF.filterFrame(frame)

        self.prevFrameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        self.SC = Searcher(frameReal, initialHeight, initialWidth, initialPosition[0], initialPosition[1],cv.cvtColor(frame, cv.COLOR_BGR2GRAY))
        self.SC.features, self.SC.trackingError = self.SC.ST.recalculateFeatures(self.prevFrameGray[int(initialPosition[1] - initialHeight / 2): int(initialPosition[1] + initialHeight / 2),int(initialPosition[0] - initialWidth / 2): int(initialPosition[0] + initialWidth / 2)])
        self.SC.features = self.SC.featureTranslate(initialPosition[0]-initialWidth/2, initialPosition[1]-initialHeight/2, self.SC.features)
        self.SC.LK.prevFeatures=self.SC.features



    def featureTranslate(self,x, y, features):
        if features is None:
            return None
        for i in range(features.shape[0]):
            features[i][0][0] += x
            features[i][0][1] += y
        return features


    def update(self, frame):

        self.frameCounter += 1
        self.KM.predict()
        realframe=frame
        if self.MF.mask is self.MF.maskingType["FILTER_LAB"]:
            if self.frameCounter != 0 and self.frameCounter % self.MF.CIELabRecalculationNumber == 0 and self.MF.labPeriodicRecalculations is True and self.SC.trackingError is False:
                medx, medy = np.median(self.SC.features[:, 0, 0]), np.median(self.SC.features[:, 0, 1])
                std = np.sqrt((np.std(self.SC.features[:, 0, 0])) ** 2 + (np.std(self.SC.features[:, 0, 1])) ** 2)
                # calculate mean and std of features
                mask = (self.SC.features[:, 0, 0] < medx + self.stdMultiplier * std + 0.1) & (
                            self.SC.features[:, 0, 0] > medx - self.stdMultiplier * std - 0.1) & (
                               self.SC.features[:, 0, 1] < medy + self.stdMultiplier * std + 0.1) & (
                                   self.SC.features[:, 0, 1] > medy - self.stdMultiplier * std - 0.1)
                self.SC.features = self.SC.features[mask]
                # remove outliers.
                medx, medy = np.median(self.SC.features[:, 0, 0]), np.median(self.SC.features[:, 0, 1])
                if np.isnan(medx) is False and np.isnan(medy) is False:
                    self.MF.calculateNewMask(frame, frame[int(medy - self.selectionHeight / 2): int(
                        medy + self.selectionHeight / 2), int(medx - self.selectionWidth / 2): int(
                        medx + self.selectionWidth / 2)])
            frame = self.MF.filterFrame(frame)

        elif self.MF.mask is self.MF.maskingType["FILTER_CSHIFT"]:
            pass

        elif self.MF.mask is self.MF.maskingType["FILTER_CORR"]:
            pass

        frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #Tacking error?
        if self.SC.trackingError is True:
            if self.SC.missAlgorithm == self.SC.missAlgorithmD["ST"]:
                x,y = self.SC.searchMissing(self.KM.statePost[0][0],self.KM.statePost[1][0],frame)
            elif self.SC.missAlgorithm == self.SC.missAlgorithmD["CORR"]:
                x, y = self.SC.searchMissing(self.KM.statePost[0][0], self.KM.statePost[1][0], realframe)
            if self.SC.trackingError is False:
                self.KM.correct(x,y)
        else:
            x,y = self.SC.search(self.frameCounter,frame)
            if self.SC.trackingError is False:
                self.KM.correct(x,y)




    def changeSettings(self, parametersNew):

        self.KM.dt = parametersNew[0]                 #kalman_ptm
        self.KM.PROCESS_COV = parametersNew[1]        #kalman_pc
        self.KM.MEAS_NOISE_COV = parametersNew[2]     #kalman_mc

        self.SC.LK.lkMaxLevel = parametersNew[3]           #lk_mr

        # = parametersNew[4]              #Color Filter OnOff
        #ColorFilter.ColorFilter.LIG_THR_CHANGE = parametersNew[5]  #colorFilter_LihtThr
        #= parametersNew[6]     #colorFilter_a
        #= parametersNew[7]     #colorFilter_b

        #= parametersNew[8]     #Light R OnOff
        #= parametersNew[9]    #ligtRec_x)
        #= parametersNew[10]   #ligtRec_maxT

        #= parametersNew[11]    #Cam shift On/Off

        self.SC.ST.maxcorners = parametersNew[12]                       #shit_MaxFeat
        self.SC.ST.qLevel = parametersNew[13]                           #shit_FeatQual
        self.SC.ST.minDist = parametersNew[14]                          #shit_MinFeat
        self.SC.ST.searchEnlargementThreshold = parametersNew[15]       #shit_Rec

        #= parametersNew[16]                #ShiTomasiOn/ Off
        self.SC.ST.frameRecalculationNumber = parametersNew[17]        #shit_SPix

        #self.MF.mask = self.MF.maskingType[parametersNew[??]] #MENSAJE PARA TOMI: tiene que ser un string parametersNew[??] fijate en la clase

        self.KM.updateParams()




    def getEstimatedPosition(self):
        return self.KM.statePost[0][0], self.KM.statePost[1][0]

    def getEstimatedVelocity(self):
        return self.KM.statePost[2][0], self.KM.statePost[3][0]

    def getTrajectory(self):
        return self.KM.trajectory



