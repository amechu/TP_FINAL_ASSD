import cv2 as cv
import numpy as np
from KalmanFilter import KalmanFilter
from MaskingFilter import MaskingFilter
from ShiTomasi import ShiTomasi
from OpticalFlow import OpticalFlow
from Searcher import Searcher
from scipy import optimize
from scipy.optimize import Bounds


class Tracker:
    LIG_THR_EVERY_FRAMES = 15

    def __init__(self, initialPosition, initialWidth, initialHeight,frame, parametersNew):

        #########################################

        #########################################
        self.initFrame = frame
        self.initPos = initialPosition
        self.KM = KalmanFilter()
        self.MF= MaskingFilter()
        self.KM.setStatePost(np.array([initialPosition[0], initialPosition[1], 0., 0.]).reshape(4, 1))
        self.selectionWidth = initialWidth
        self.selectionHeight = initialHeight

        self.prevFrameGray = None
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

        self.SC = Searcher(self.initFrame, initialHeight, initialWidth, initialPosition[0], initialPosition[1],cv.cvtColor(frame, cv.COLOR_BGR2GRAY))
        self.SC.features, self.SC.trackingError = self.SC.ST.recalculateFeatures(self.prevFrameGray[int(initialPosition[1] - initialHeight / 2): int(initialPosition[1] + initialHeight / 2),int(initialPosition[0] - initialWidth / 2): int(initialPosition[0] + initialWidth / 2)])
        self.SC.features = self.SC.featureTranslate(initialPosition[0] - initialWidth / 2,initialPosition[1] - initialHeight / 2, self.SC.features)
        self.SC.LK.prevFeatures = self.SC.features

        #x_bounds = [(1, 200), (0, 20), (0, 20), (0, 250)]

        #res = optimize.shgo(self.costChangeParams, x_bounds, options={'disp': True ,'eps' : 5e0})

        #print(res.x)

    def getTrackingError(self):
        return self.SC.trackingError

    def setFilter(self,filterType):
        if filterType in self.MF.maskingType.keys():
            self.MF.mask = self.MF.maskingType[filterType]
        else:
            print("Wrong filter type")

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
                vx, vy = self.getEstimatedVelocity()
                if np.abs(vx) < 5 and np.abs(vy) < 5:
                    medx, medy = np.median(self.SC.features[:, 0, 0]), np.median(self.SC.features[:, 0, 1])
                    std = np.sqrt((np.std(self.SC.features[:, 0, 0])) ** 2 + (np.std(self.SC.features[:, 0, 1])) ** 2)
                    # calculate mean and std of features
                    mask = (self.SC.features[:, 0, 0] < medx + self.SC.stdMultiplier * std + 0.1) & (
                                self.SC.features[:, 0, 0] > medx - self.SC.stdMultiplier * std - 0.1) & (
                                   self.SC.features[:, 0, 1] < medy + self.SC.stdMultiplier * std + 0.1) & (
                                       self.SC.features[:, 0, 1] > medy - self.SC.stdMultiplier * std - 0.1)
                    self.SC.features = self.SC.features[mask]
                    # remove outliers.
                    medx, medy = np.median(self.SC.features[:, 0, 0]), np.median(self.SC.features[:, 0, 1])
                    if (~np.isnan(medx)) and (~np.isnan(medy)):
                        self.MF.calculateNewMask(frame, frame[int(medy - self.selectionHeight / 2): int(
                            medy + self.selectionHeight / 2), int(medx - self.selectionWidth / 2): int(
                            medx + self.selectionWidth / 2)])


            frame = self.MF.filterFrame(frame)
        elif self.MF.mask is self.MF.maskingType["FILTER_CSHIFT"]:
            frame = self.MF.filterFrame(frame)
            #TINCHO



        #Tacking error?
        if self.SC.trackingError is True:
            if self.SC.missAlgorithm == self.SC.missAlgorithmD["ST"]:
                x,y = self.SC.searchMissing(self.KM.statePost[0][0],self.KM.statePost[1][0],frame,frame)
            elif self.SC.missAlgorithm == self.SC.missAlgorithmD["CORR"]:
                x, y = self.SC.searchMissing(self.KM.statePost[0][0], self.KM.statePost[1][0], realframe,frame)
            if self.SC.trackingError is False:
                self.KM.correct(x,y)
        else:
            x,y = self.SC.search(self.frameCounter,realframe,frame)
            if self.SC.trackingError is False:
                self.KM.correct(x,y)



    def updateBGR(self,color):
        self.MF.calculateNewMask(None,None,True,color)

    def changeSettings(self, parametersNew):

        self.KM.dt = parametersNew[0]                 #kalman_ptm
        self.KM.PROCESS_COV = parametersNew[1]        #kalman_pc
        self.KM.MEAS_NOISE_COV = parametersNew[2]     #kalman_mc

        self.SC.LK.lkMaxLevel = int(parametersNew[3])           #lk_mr

        if  parametersNew[4] is False:              #Color Filter OnOff
            self.MF.mask = self.MF.maskingType["FILTER_OFF"]

        self.MF.LSemiAmp = parametersNew[5]  #colorFilter_LihtThr
        self.MF.aSemiAmp = parametersNew[6]     #colorFilter_a
        self.MF.bSemiAmp = parametersNew[7]     #colorFilter_b

        if parametersNew[20] == True and parametersNew[19] == False :
            self.SC.missAlgorithm = self.SC.missAlgorithmD["ST"]
        elif parametersNew[20] == False and parametersNew[19] == True:
            self.SC.missAlgorithm = self.SC.missAlgorithmD["CORR"]
        if parametersNew[22] == True and parametersNew[21] == False:
            self.SC.recalcAlgorithm = self.SC.recalcAlgorithmD["ST"]
        elif parametersNew[22] == False and parametersNew[21] == True:
            self.SC.recalcAlgorithm = self.SC.recalcAlgorithmD["CORR"]
        self.SC.MASKCONDITION = parametersNew[23]

        #= parametersNew[8]     #Light R OnOff
        #= parametersNew[9]    #ligtRec_x)
        #= parametersNew[10]   #ligtRec_maxT

        #= parametersNew[11]    #Cam shift On/Off

        self.SC.ST.maxcorners = int(parametersNew[13])                       #shit_MaxFeat
        self.SC.ST.qLevel = parametersNew[14]                           #shit_FeatQual
        self.SC.ST.minDist = parametersNew[15]                          #shit_MinFeat

        #= parametersNew[16]                #ShiTomasiOn/ Off
        self.SC.ST.frameRecalculationNumber = parametersNew[16]        #shit_SPix

        #self.MF.mask = self.MF.maskingType[parametersNew[??]] #MENSAJE PARA TOMI: tiene que ser un string parametersNew[??] fijate en la clase

        self.MF.hist_filter.set_bins(parametersNew[9])
        self.MF.hist_filter.set_mask_blur(parametersNew[10])
        self.MF.hist_filter.set_kernel_blur(parametersNew[11])
        self.MF.hist_filter.set_low_pth(parametersNew[12])

        self.MF.ksize = parametersNew[24]
        if int(self.MF.ksize) %2 == 0:
            self.MF.ksize = int(self.MF.ksize)+1
        else:
            self.MF.ksize = int(self.MF.ksize)

        self.MF.updateMaskFromSettings()
        self.KM.updateParams()

    def getFilteredFrame(self):
        return self.MF.filteredFrame

    def getCorrFrame(self):
        return self.SC.corr_out

    def getEstimatedPosition(self):
        return self.KM.statePost[0][0], self.KM.statePost[1][0]

    def getEstimatedVelocity(self):
        return self.KM.statePost[2][0], self.KM.statePost[3][0]

    def getTrajectory(self):
        return self.KM.trajectory

    def costChangeParams(self, x): # x = [parametersNew[9], parametersNew[11], parametersNew[12]]

        x[0] = int(x[0])
        x[1] = int(x[1]/25)
        x[2] = int(x[2]/25)
        x[3] = int(x[3])
        self.MF.hist_filter.set_bins(x[0])
        self.MF.hist_filter.set_kernel_blur(x[2])
        self.MF.hist_filter.set_mask_blur(x[1])
        self.MF.hist_filter.set_low_pth(x[3])
        self.MF.updateMaskFromSettings()
        testFrame = self.MF.filterFrame(self.initFrame)

        countTotal = np.count_nonzero(testFrame)
        countInside = np.count_nonzero(testFrame[int(self.initPos[1] - self.selectionHeight / 2): int(self.initPos[1] + self.selectionHeight / 2),int(self.initPos[0] - self.selectionWidth / 2): int(self.initPos[0] + self.selectionWidth / 2)])

        countOutside = countTotal - countInside
        print(countOutside-countInside)
        return countOutside - countInside

    def colorKernelChange(self, bgr):
        b = bgr[0]
        g = bgr[1]
        r = bgr[2]
