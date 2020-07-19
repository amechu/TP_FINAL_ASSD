import cv2 as cv
import numpy as np
import KalmanFilter
import ColorFilter
import ShiTomasi
import OpticalFlow


class Tracker:
    LIG_THR_EVERY_FRAMES = 15

    def __init__(self, initialPosition, initialWidth, initialHeight,frame):
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
        self.prevFrameGray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        self.features, self.trackingError = self.ST.recalculateFeatures(self.prevFrameGray[int(initialPosition[1] - initialHeight / 2): int(initialPosition[1] + initialHeight / 2),int(initialPosition[0] - initialWidth / 2): int(initialPosition[0] + initialWidth / 2)])
        self.features = self.featureTranslate(initialPosition[0]-initialWidth/2, initialPosition[1]-initialHeight/2, self.features)
        self.LK.prevFeatures=self.features


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

        if self.ColF.colorFilterUse is True:
            pass
        #falta toddo lo de filtro de color

        frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #Tacking error?
        if self.trackingError is True:
            #Yes, then apply ST algorithm around estimate
            self.features, self.trackingError = self.ST.recalculateFeatures(frameGray[ int( self.KM.statePost[1][0] - self.searchHeight/2) : int(self.KM.statePost[1][0] + self.searchHeight/2),int(self.KM.statePost[0][0] - self.searchWidth/2 ): int(self.KM.statePost[0][0] + self.searchWidth/2)])
            self.features = self.featureTranslate(self.KM.statePost[0][0]-self.searchWidth/2,self.KM.statePost[1][0]-self.searchHeight/2, self.features)
            #did i find it?
            if self.trackingError is True:
                #No, then enlarge search area
                self.enlargeSearchArea()
            else:
                #shrink search area to original and set tracking error to false, #kalman correct
                self.searchHeight = self.selectionHeight
                self.searchWidth = self.selectionWidth
                self.KM.correct(np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1]))
                self.LK.prevFeatures = self.features
        else:
            #Apply LK algorithm
            self.features, self.trackingError = self.LK.updateFeatures(self.prevFrameGray, frameGray)
            if self.trackingError is False: #Tracking error?
                #recaulculate features?
                if self.frameCounter != 0 and self.frameCounter % self.ST.frameRecalculationNumber == 0:
                    #yes
                    medx, medy = np.median(self.features[:, 0, 0]), np.median(self.features[:, 0, 1])
                    std = np.sqrt((np.std(self.features[:, 0, 0]))**2 + (np.std(self.features[:, 0, 1]))**2)
                    #calculate mean and std of features
                    mask = (self.features[:, 0, 0] < medx + self.stdMultiplier * std + 0.1) & (self.features[:, 0, 0] > medx - self.stdMultiplier * std - 0.1) & (
                            self.features[:, 0, 1] < medy + self.stdMultiplier * std + 0.1) & (self.features[:, 0, 1] > medy - self.stdMultiplier * std - 0.1)
                    self.features = self.features[mask]
                    #remove outliers.
                    medx, medy = np.median(self.features[:, 0, 0]), np.median(self.features[:, 0, 1])
                    self.features, self.trackingError = self.ST.recalculateFeatures(frameGray[int(medy - self.selectionHeight / 2): int(medy + self.selectionHeight / 2),int(medx - self.selectionWidth / 2): int(medx + self.selectionWidth / 2)])
                    self.features = self.featureTranslate(medx- self.selectionWidth / 2, medy - self.selectionHeight / 2, self.features)
                    self.LK.prevFeatures = self.features
                    #apply st algorithm

                    if self.trackingError is False:#did i found features?
                        #found, then KM correct.
                        self.KM.correct(np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1]))
                    #else would be Features not found.
                else:#NO, then kalman correct estimate.
                    self.KM.correct(np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1]))
# Recalculate features?
#           else would be tracking error true
        self.prevFrameGray = frameGray


    def changeSettings(self, parametersNew):

        self.KM.dt = parametersNew[0]                 #kalman_ptm
        self.KM.PROCESS_COV = parametersNew[1]        #kalman_pc
        self.KM.MEAS_NOISE_COV = parametersNew[2]     #kalman_mc

        self.LK.lkMaxLevel = parametersNew[3]           #lk_mr

        #parametersNew[4]              #ColorFilterActive
        #ColorFilter.ColorFilter.LIG_THR_CHANGE = parametersNew[6]  #colorFilter_LihtThr
        #ColorFilter.ColorFilter.
        #parametersNew[7]  # .append(self.colorFilter_a[0])
        #parametersNew[8]  # .append(self.colorFilter_b[0])

        #parametersNew[5]    #.append(self.LightRecalcActive[0])
        #parametersNew[9]    #.append(self.ligtRec_x[0])
        #parametersNew[10]   #.append(self.ligtRec_maxT[0])

        self.ST.maxcorners = parametersNew[12]                       #shit_MaxFeat
        self.ST.qLevel = parametersNew[13]                           #shit_FeatQual
        self.ST.minDist = parametersNew[14]                          #shit_MinFeat
        self.ST.searchEnlargementThreshold = parametersNew[15]       #shit_Rec
        # parametersNew[11]   #.ShiTPropActive
        self.ST.frameRecalculationNumber = parametersNew[16]        #shit_SPix[0]

        self.KM.updateParams()


    def enlargeSearchArea(self):
        self.searchWidth += self.ST.searchEnlargementThreshold
        self.searchHeight += self.ST.searchEnlargementThreshold

    def getEstimatedPosition(self):
        return self.KM.statePost[0][0], self.KM.statePost[1][0]

    def getEstimatedVelocity(self):
        return self.KM.statePost[2][0], self.KM.statePost[3][0]

    def getFilteredFrame(self):
        pass

    def filterFrame(self):
        pass




