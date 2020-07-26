import cv2 as cv
import cvui
import numpy as np
import tkinter as tk
from tkinter import filedialog
import Tracker
import Artist
import MaskingFilter as MF

WINDOW_NAME = "MAGT Video Tracker"

INITIAL_KALMAN_PTM = 1.2
INITIAL_KALMAN_PC = 0.006
INITIAL_KALMAN_MC = 0.4

INITIAL_LK_MR = 4.0

COLORFILTER_ONOFF = False
COLORFILTER_LIGHTTHR = 50.0
COLORFILTER_A = 15.0
COLORFILTER_B = 15.0
MASKBLUR_LAB = 1

CAMSHIFT_ONOFF = False
CAMSHIFT_BIN = 64.0
CAMSHIFT_MB = 11.0
CAMSHIFT_SB = 4.0
CAMSHIFT_LBPT = 200.0

INITIAL_ST_ONOFF = False
SHIT_MAXFEAT = 100.0
SHIT_FEATQUAL = 0.001
SHIT_MINFEAT = 0.01
SHIT_REC = 20.0
SHIT_SPIX = 4.0

MASK_COND = 0.2

MIS_COR = True
MIS_ST = False
REC_COR = True
REC_ST = True

Y_SCREEN = 960
X_SCREEN = 1500 #1310 #1280

STANDAR_WIDTH = 500 #720

WINDOW_VS_X = 10
WINDOW_VS_Y = 10
WINDOW_VS_WIDTH = 230
WINDOW_VS_HEIGHT = 130

WINDOW_SET_X = 10
WINDOW_SET_Y = 150
WINDOW_SET_WIDTH = 230
WINDOW_SET_HEIGHT = Y_SCREEN - WINDOW_SET_Y - WINDOW_VS_Y

WINDOW_SOU_X = WINDOW_VS_X*2 + WINDOW_VS_WIDTH
WINDOW_SOU_Y = WINDOW_VS_Y
WINDOW_SOU_WIDTH = STANDAR_WIDTH + 2*WINDOW_VS_X
WINDOW_SOU_HEIGHT = STANDAR_WIDTH + 2*WINDOW_VS_X

WINDOW_FIL_X = WINDOW_SOU_X + WINDOW_SOU_WIDTH + WINDOW_VS_X
WINDOW_FIL_Y = WINDOW_VS_Y
WINDOW_FIL_WIDTH = WINDOW_SOU_WIDTH #X_SCREEN - WINDOW_FIL_X - WINDOW_SET_X
WINDOW_FIL_HEIGHT = WINDOW_SOU_HEIGHT #Y_SCREEN - WINDOW_FIL_Y - WINDOW_VS_Y

WINDOW_FILS_X = WINDOW_FIL_X + WINDOW_FIL_WIDTH + WINDOW_VS_X
WINDOW_FILS_Y = WINDOW_VS_Y
WINDOW_FILS_WIDTH = X_SCREEN - WINDOW_FILS_X - WINDOW_SET_X
WINDOW_FILS_HEIGHT = WINDOW_SOU_HEIGHT #Y_SCREEN - WINDOW_FIL_Y - WINDOW_VS_Y

WINDOW_TRK_X = WINDOW_SOU_X
WINDOW_TRK_Y = WINDOW_SOU_WIDTH + 2*WINDOW_VS_Y
WINDOW_TRK_WIDTH = X_SCREEN - WINDOW_TRK_X - WINDOW_SET_X  #WINDOW_SOU_WIDTH
WINDOW_TRK_HEIGHT = Y_SCREEN - WINDOW_TRK_Y - WINDOW_VS_Y #WINDOW_VS_HEIGHT

MAX_TRACKERS = 5

class cvGui():

    def __init__(self, *args, **kw):

        #Trackers
        self.trackers = []

        #Frames
        self.frame = np.zeros((Y_SCREEN, X_SCREEN, 3), np.uint8)
        self.source = []

        #Source names    
        self.VideoLoaded = "None"
        self.CurrentSource = "None"
        self.videoName = ""                 
        self.videoPath = ""                  
        self.videoExtension = ""

        #Utils for source
        self.sourceX = 0
        self.sourceY = 0
        self.sourceWIDTH = 0
        self.sourceHEIGHT = 0
        self.filterWIDTH = 0
        self.filterHEIGHT = 0

        self.usingCamera = False
        self.usingVideo = False
        self.pause = False

        self.cap = cv.VideoCapture

        #Using Device
        self.deviceID = 0               #0 = open default camera
        self.apiID = cv.CAP_ANY         #0 = autodetect default API
    
        #Kalman Properties
        self.KalmanProp = [False]
    
        self.kalman_ptm = [INITIAL_KALMAN_PTM]
        self.kalman_pc = [INITIAL_KALMAN_PC]
        self.kalman_mc = [INITIAL_KALMAN_MC]
    
        #LK Properties
        self.LKProp = [False]
    
        self.lk_mr = [INITIAL_LK_MR]
    
        #CF Properties
        self.CFProp = [False]
        self.CFPropOnOff = [COLORFILTER_ONOFF]
        self.CFCamShiftOnOff = [CAMSHIFT_ONOFF]

        self.colorFilter_LihtThr = [COLORFILTER_LIGHTTHR]
        self.colorFilter_a = [COLORFILTER_A]
        self.colorFilter_b = [COLORFILTER_B]
        self.maskBlur_lab = [MASKBLUR_LAB]

        self.camShift_bins = [CAMSHIFT_BIN]
        self.camShift_mb = [CAMSHIFT_MB] #Blur sobre toda la mascara
        self.camShift_sb = [CAMSHIFT_SB] #Blur sobre la selección
        self.camShift_lbpt = [CAMSHIFT_LBPT]
    
        #Shi - Tomasi Properties
        self.ShiTProp = [False]
        self.ShiTPropOnOff = [INITIAL_ST_ONOFF]

        self.shit_MaxFeat = [SHIT_MAXFEAT]
        self.shit_FeatQual = [SHIT_FEATQUAL]
        self.shit_MinFeat = [SHIT_MINFEAT]
        self.shit_Rec = [SHIT_REC]
        self.shit_SPix = [SHIT_SPIX]

        #Miss Algorithm
        self.missAlgCorr = [MIS_COR]
        self.missAlgST = [MIS_ST]

        #Recalculation Algorithm
        self.recAlgCorr = [REC_COR]
        self.recAlgST = [REC_ST]

        self.maskCondition = [MASK_COND]

        cv.namedWindow(WINDOW_NAME, cv.WINDOW_NORMAL)
        cvui.init(WINDOW_NAME)

        #Filter Edit
        self.ColorFilter = [False]
        self.CorrFilter = [False]

        self.CamShiftFilter = [False]
        self.Hist = [False]

        self.filterConditions = []

        #Tracker elements
        self.trackerColors = [0xF5741B, 0x6CF12A, 0x2AACF1, 0x972AF1, 0xF12A33]
        self.parameters = []
        self.parametersNew = []
        self.boolForTrackers = []
        self.kernel = []
        self.trackSelectionBGR = [[], [], [], [], []]
        self.lastTracker = -1
        self.deletedTracker = -1
        self.configSelected = []

        self.changeInTrackers = False
        self.trackerAdded = False
        self.trackerChanged = False

        #Video Loaded elements
        self.boolVideoLoaded = False
        self.arrayVideoLoaded = []
        self.filteredFrame = []

        self.lastFrame = []
        self.lastFilterFrame = []
        self.lastEditedFrame = []

        self.replaceRoi = False
        self.coordsRoi = []

        self.ShowShit = [True]
        self.ShowEstimate = [True]
        self.ShowTrajectory = [True]

    def onWork(self):

        selectedT = -1
        self.updateParameters()
        originalParam = self.parameters.copy()

        while True:

            # print(f'LAB: {self.CFCamShiftOnOff}           CamOnOF:{self.CFPropOnOff}')

            self.updateParameters()
            selectedT = self.IsTrackerSelected()

            self.frame[:] = (49, 52, 49)

            # FRAMES
            cvui.window(self.frame, WINDOW_VS_X, WINDOW_VS_Y, WINDOW_VS_WIDTH, WINDOW_VS_HEIGHT, "Load Source:")  # Video Source Frame
            cvui.window(self.frame, WINDOW_SET_X, WINDOW_SET_Y, WINDOW_SET_WIDTH, WINDOW_SET_HEIGHT, "Tracker Settings:")  # Settings Frame
            cvui.window(self.frame, WINDOW_SOU_X, WINDOW_SOU_Y, WINDOW_SOU_WIDTH, WINDOW_SOU_HEIGHT, "Source:")
            cvui.window(self.frame, WINDOW_FIL_X, WINDOW_FIL_Y, WINDOW_FIL_WIDTH, WINDOW_FIL_HEIGHT, "Filter View:")
            cvui.window(self.frame, WINDOW_FILS_X, WINDOW_FILS_Y, WINDOW_FILS_WIDTH, WINDOW_FILS_HEIGHT, "Filter Selection:")
            cvui.window(self.frame, WINDOW_TRK_X, WINDOW_TRK_Y, WINDOW_TRK_WIDTH, WINDOW_TRK_HEIGHT, "Trackers:")

            #Text
            cvui.printf(self.frame, 17, 35, 0.4, 0xdd97fb, "Current Source:")                #Video Source
            cvui.printf(self.frame, 17, 50, 0.4, 0xdd97fb, self.CurrentSource)               #Video Source

            if selectedT == -1:
                cvui.printf(self.frame, 17, 275, 0.4, 0xdd97fb, "No Tracker Selected To Modify")        #0xd11616
            else:
                cvui.printf(self.frame, 17, 275, 0.4, self.trackerColors[selectedT], "Changes Saved For Tracker " + str(selectedT + 1) + "!")

            if self.pause:# and not self.replaceRoi:
                if (self.usingVideo or self.usingCamera):
                    cvui.printf(self.frame, 17, 255, 0.4, 0xdc1076, "Source Paused!")
                else:
                    cvui.printf(self.frame, 17, 255, 0.4, 0xdc1076, "Source Will Be Paused.")
            else:
                if (self.usingVideo or self.usingCamera):
                    cvui.printf(self.frame, 17, 255, 0.4, 0x10dca1, "Source Playing!")
                else:
                    cvui.printf(self.frame, 17, 255, 0.4, 0x10dca1, "Source Will Be Playing.")

            #Video Source Buttons
            if (cvui.button(self.frame, 20, 70, "Use Video")):
                if (self.openFile()):
                    self.usingCamera = False
                    self.usingVideo = True
                    if(self.initSource()):                                                                #Chequear si se inicia bien
                        self.VideoLoaded = self.videoPath
                        self.CurrentSource = "Video Loaded: " + self.videoName
                        selectedT = -1
                        self.pause = True
                    else:
                        self.usingCamera = False
                        self.usingVideo = False

                # elif not self.usingCamera:
                #     self.CurrentSource = "No Video Loaded"

            if (cvui.button(self.frame, 120, 70, "Reload Video") and self.usingVideo):
                self.usingCamera = False
                self.usingVideo = True
                if (self.initSource()):  # Chequear si se inicia bien
                    self.VideoLoaded = self.videoPath
                    self.CurrentSource = "Video Loaded: " + self.videoName
                    selectedT = -1
                    self.pause = True
                else:
                    self.usingCamera = False
                    self.usingVideo = False

            if (cvui.button(self.frame, int((2*WINDOW_SET_X + WINDOW_SET_WIDTH)/2.0) - 60, 105, "Use Camera") and not self.usingCamera):
               self.trackers.clear()
               self.usingVideo = False
               self.usingCamera = True
               if (self.initSource()):                  #Chequear si se inicia bien
                   self.CurrentSource = "Camera On"
                   selectedT = -1
               else:
                   self.usingVideo = False
                   self.usingCamera = False

            #Settings Buttons
            a = len(self.trackers)

            for i in range(a):
                if self.trackerAdded:
                    self.boolForTrackers.append([False])
                    self.trackerAdded = False

                windowWidth = int((WINDOW_TRK_WIDTH - 150) / MAX_TRACKERS)

                xTx = WINDOW_TRK_X + int((WINDOW_TRK_WIDTH - 10) * (i) / MAX_TRACKERS) + 20
                yTx = WINDOW_TRK_Y + 60
                xB = xTx + int(windowWidth/MAX_TRACKERS) #WINDOW_TRK_X - 170 + int(WINDOW_TRK_WIDTH * (i + 1) / MAX_TRACKERS)
                yB = WINDOW_TRK_Y + 80

                windowHeight = int(Y_SCREEN - 2*WINDOW_SOU_Y - yTx + 10)

                xx, yy = self.trackers[i].getEstimatedPosition()
                vx, vy = self.trackers[i].getEstimatedVelocity()
                cvui.window(self.frame, xTx, yTx - 10, windowWidth, windowHeight, "Tracker Number " + str(i + 1))
                cvui.rect(self.frame, xTx + 2, yTx+10, windowWidth-3, windowHeight-20, self.trackerColors[i], self.trackerColors[i])

                checking = []
                for k in range(a):
                    checking.append([False])

                cvui.printf(self.frame, xTx + 25, yTx + 85, 0.4, 0x000000, f'X = {int(xx)}')
                cvui.printf(self.frame, xTx + 125, yTx + 85, 0.4, 0x000000, f'Y = {int(yy)}')
                cvui.printf(self.frame, xTx + 25, yTx + 100, 0.4, 0x000000, f'Vx = {round(vx, 1)}')
                cvui.printf(self.frame, xTx + 125, yTx + 100, 0.4, 0x000000, f'Vy = {round(-vy, 1)}')

                if cvui.checkbox(self.frame, xB, yTx+125, "Select Tracker", self.boolForTrackers[i], 0x000000):
                    for j in range(a):
                        if not j == i:
                            self.boolForTrackers[j] = [False]

                    cvui.printf(self.frame, xB - 5, yTx + 50, 0.4, 0x000000, "Filter displayed is for")
                    cvui.printf(self.frame, xB + 25, yTx + 65, 0.4, 0x000000, "this tracker!")

                w = int(self.kernel[i].shape[1])
                h = int(self.kernel[i].shape[0])
                xFrame = int((windowWidth + 2*(xTx))/2 - w/2)
                yFrame = yTx + 150
                self.frame[yFrame:yFrame + h, xFrame:xFrame + w] = self.kernel[i]
                status = cvui.iarea(xFrame, yFrame, w, h)
                if status == cvui.CLICK:
                    cursor = cvui.mouse(WINDOW_NAME)
                    self.trackSelectionBGR[i] = self.frame[cursor.y, cursor.x]

                if (cvui.button(self.frame, xB+5, yB-5, "Delete Tracker")):
                    self.changeInTrackers = True
                    del self.configSelected[i]
                    del self.boolForTrackers[i]
                    del self.filterConditions[i]
                    del self.trackers[i]
                    del self.kernel[i]
                    self.trackerColors.append(self.trackerColors[i])
                    self.trackSelectionBGR[i] = []
                    del self.trackerColors[i]
                    self.deletedTracker = i
                    selectedT = self.IsTrackerSelected()

                    if len(self.trackers) == 0:
                        self.filterConditions.clear()

                        self.filteredFrame = None
                        self.resetInitialCond()

                        self.ColorFilter[0] = False
                        self.CorrFilter[0] = False
                        self.CamShiftFilter[0] = False
                        self.Hist[0] = False
                        self.CFPropOnOff[0] = False
                        self.CFCamShiftOnOff[0] = False

                        self.ShiTProp[0] = False
                        self.LKProp[0] = False
                        self.KalmanProp[0] = False
                        self.CFProp[0] = False
                    break

            self.trackerChanged = not(selectedT == self.IsTrackerSelected())
            # if self.trackerChanged:
            #     selectedT = self.IsTrackerSelected()

            if a == 0:
                cvui.printf(self.frame, WINDOW_TRK_X + 5, WINDOW_TRK_Y + 30, 0.4, 0x5ed805, "No Trackers Added. Try Selecting A New Area!")
                self.filteredFrame = None
            elif a == 1:
                cvui.printf(self.frame, WINDOW_TRK_X + 5, WINDOW_TRK_Y + 30, 0.4, 0x79d805, "Using 1 Tracker Of 5!")
            elif a == 2:
                cvui.printf(self.frame, WINDOW_TRK_X + 5, WINDOW_TRK_Y + 30, 0.4, 0xa0d805, "Using 2 Tracker Of 5!")
            elif a == 3:
                cvui.printf(self.frame, WINDOW_TRK_X + 5, WINDOW_TRK_Y + 30, 0.4, 0xcfd805, "Using 3 Tracker Of 5!")
            elif a == 4:
                cvui.printf(self.frame, WINDOW_TRK_X + 5, WINDOW_TRK_Y + 30, 0.4, 0xdcce10, "Using 4 Tracker Of 5!")
            else:
                cvui.printf(self.frame, WINDOW_TRK_X + 5, WINDOW_TRK_Y + 30, 0.4, 0xdc2710, "Using 5 Trackers Of 5! No More Trackers Can Be Added.")

            if (cvui.button(self.frame, 20, 215, "Pause Source") and not self.replaceRoi):
                self.pause = not self.pause

            #Settings Poperties
            if cvui.checkbox(self.frame, 20, 300, "Kalman", self.KalmanProp):
                self.LKProp[0] = False
                self.CFProp[0] = False
                self.ShiTProp[0] = False

                if not selectedT == -1:
                    cvui.printf(self.frame, 20, 400, 0.4, 0xdd97fb, "Process Time Multiplier")
                    cvui.trackbar(self.frame, 20, 415, 210, self.kalman_ptm, 0.0, 2.0)

                    cvui.printf(self.frame, 20, 470, 0.4, 0xdd97fb, "Process Covariance")
                    cvui.trackbar(self.frame, 20, 485, 210, self.kalman_pc, 0.0, 0.1, 1, "%0.3Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)

                    cvui.printf(self.frame, 20, 540, 0.4, 0xdd97fb, "Measurement Covariance")
                    cvui.trackbar(self.frame, 20, 555, 210, self.kalman_mc, 0.0, 1.0)

            if cvui.checkbox(self.frame, 20, 320, "Lucas-Kanade", self.LKProp):
                self.KalmanProp[0] = False
                self.CFProp[0] = False
                self.ShiTProp[0] = False

                if not selectedT == -1:
                    cvui.printf(self.frame, 20, 400, 0.4, 0xdd97fb, "Maximum Recursion")    #TOMI HACE ESTO DISCRETO
                    cvui.trackbar(self.frame, 20, 415, 210, self.lk_mr, 0.0, 10.0, 1, "%1.0Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)
                    self.lk_mr[0] = int(self.lk_mr[0])

            if cvui.checkbox(self.frame, 20, 340, "Mask Filter", self.CFProp):
                self.KalmanProp[0] = False
                self.LKProp[0] = False
                self.ShiTProp[0] = False

                if not selectedT == -1:
                    if cvui.checkbox(self.frame, 20, 400, "LAB Color Filter", self.CFPropOnOff):
                        self.CFCamShiftOnOff[0] = False

                        cvui.printf(self.frame, 20, 450, 0.4, 0xdd97fb, "L Semiamplitude")
                        cvui.trackbar(self.frame, 20, 465, 210, self.colorFilter_LihtThr, 0.0, 150.0)

                        cvui.printf(self.frame, 20, 520, 0.4, 0xdd97fb, "A Semiamplitude")
                        cvui.trackbar(self.frame, 20, 535, 210, self.colorFilter_a, 0.0, 200.0)

                        cvui.printf(self.frame, 20, 590, 0.4, 0xdd97fb, "B Semiamplitude")
                        cvui.trackbar(self.frame, 20, 605, 210, self.colorFilter_b, 0.0, 200.0)

                        cvui.printf(self.frame, 20, 660, 0.4, 0xdd97fb, "Mask Blur")
                        cvui.trackbar(self.frame, 20, 675, 210, self.maskBlur_lab, 0.0, 20.0, 1, "%1.0Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)
                        self.maskBlur_lab[0] = int(self.maskBlur_lab[0])

                    if cvui.checkbox(self.frame, 20, 420, "Cam Shift Filter", self.CFCamShiftOnOff):
                        self.CFPropOnOff[0] = False

                        cvui.printf(self.frame, 20, 450, 0.4, 0xdd97fb, "Number Of Bins")
                        cvui.trackbar(self.frame, 20, 465, 210, self.camShift_bins, 1.0, 200.0, 1, "%1.0Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)
                        if self.camShift_bins[0] < 1:
                            self.camShift_bins[0] = 1
                        self.camShift_bins[0] = int(self.camShift_bins[0])

                        cvui.printf(self.frame, 20, 520, 0.4, 0xdd97fb, "Mask Blur")
                        cvui.trackbar(self.frame, 20, 535, 210, self.camShift_mb, 0.0, 20.0, 1, "%1.0Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)
                        self.camShift_mb[0] = int(self.camShift_mb[0])

                        cvui.printf(self.frame, 20, 590, 0.4, 0xdd97fb, "Selection Blur")
                        cvui.trackbar(self.frame, 20, 605, 210, self.camShift_sb, 0.0, 20.0, 1, "%1.0Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)
                        self.camShift_sb[0] = int(self.camShift_sb[0])

                        cvui.printf(self.frame, 20, 660, 0.4, 0xdd97fb, "Lower Bound Prob. Thr.")
                        cvui.trackbar(self.frame, 20, 675, 210, self.camShift_lbpt, 0.0, 254.0, 1, "%1.0Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)
                        self.camShift_lbpt[0] = int(self.camShift_lbpt[0])

                    #Printeo ONS/OFFS
                    if (self.CFPropOnOff[0]):
                        cvui.printf(self.frame, 145, 402, 0.4, 0x10dcA1, "On")
                        cvui.printf(self.frame, 145, 422, 0.4, 0xdc1076, "Off")
                    elif (self.CFCamShiftOnOff[0]):
                        cvui.printf(self.frame, 145, 402, 0.4, 0xdc1076, "Off")
                        cvui.printf(self.frame, 145, 422, 0.4, 0x10dcA1, "On")
                    else:
                        cvui.printf(self.frame, 145, 402, 0.4, 0xdc1076, "Off")
                        cvui.printf(self.frame, 145, 422, 0.4, 0xdc1076, "Off")

            if cvui.checkbox(self.frame, 20, 360, "Shi-Tomasi", self.ShiTProp):
                self.KalmanProp[0] = False
                self.LKProp[0] = False
                self.CFProp[0] = False

                if not selectedT == -1:
                    cvui.printf(self.frame, 20, 400, 0.4, 0xdd97fb, "Maximum Feature Quantity")
                    cvui.trackbar(self.frame, 20, 415, 210, self.shit_MaxFeat, 1.0, 100.0, 1, "%1.0Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)
                    self.shit_MaxFeat[0] = int(self.shit_MaxFeat[0])

                    cvui.printf(self.frame, 20, 470, 0.4, 0xdd97fb, "Feature Quality Level")
                    cvui.trackbar(self.frame, 20, 485, 210, self.shit_FeatQual, 0.0, 1)

                    cvui.printf(self.frame, 20, 540, 0.4, 0xdd97fb, "Minimum Feature Distance")
                    cvui.trackbar(self.frame, 20, 555, 210, self.shit_MinFeat, 0.0, 1.0)

                    cvui.printf(self.frame, 20, 610, 0.4, 0xdd97fb, "Search Pixel Enlargement")
                    cvui.trackbar(self.frame, 20, 625, 210, self.shit_SPix, 0.0, 10.0)

                    if (cvui.checkbox(self.frame, 20, 680, "Feature Recalculation", self.ShiTPropOnOff)):
                        cvui.printf(self.frame, 20, 710, 0.4, 0xdd97fb, "Recalculation Number")
                        cvui.trackbar(self.frame, 20, 725, 210, self.shit_Rec, 1.0, 100.0, 1, "%1.0Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)
                        self.shit_Rec[0] = int(self.shit_Rec[0])
                        cvui.printf(self.frame, 185, 682, 0.4, 0x10dcA1, "%s", "On")
                    else:
                        cvui.printf(self.frame, 185, 682, 0.4, 0xdc1076, "%s", "Off")

            #Show Features
            beforeShowBox = [self.ShowShit[0], self.ShowEstimate[0], self.ShowTrajectory[0]]
            cvui.checkbox(self.frame, WINDOW_SOU_X + 10, WINDOW_SOU_Y + WINDOW_SOU_WIDTH - 27, "Show Features", self.ShowShit)
            cvui.checkbox(self.frame, WINDOW_SOU_X + int(WINDOW_SOU_WIDTH/3), WINDOW_SOU_Y + WINDOW_SOU_WIDTH - 27, "Show Estiamted Pos.", self.ShowEstimate)
            cvui.checkbox(self.frame, WINDOW_SOU_X + int(WINDOW_SOU_WIDTH) - 130, WINDOW_SOU_Y + WINDOW_SOU_WIDTH - 27, "Show Trajectory", self.ShowTrajectory)
            afterShowBox = [self.ShowShit[0], self.ShowEstimate[0], self.ShowTrajectory[0]]
            if not beforeShowBox == afterShowBox:
                self.changeInTrackers = True

            #Filters: Correlation, Cam shift, Color, Histogram

            selectedT = self.IsTrackerSelected()
            if self.lastTracker != selectedT:
                if (selectedT == -1) and ((len(self.boolForTrackers) == 0) or (self.deletedTracker == self.lastTracker)):
                    self.lastTracker = -1
                else:
                    if not (selectedT == -1):
                        self.loadParameters(selectedT)
                        self.lastTracker = selectedT
                    if not len(self.filterConditions) == 0:
                        self.ColorFilter[0] = self.filterConditions[selectedT][0]
                        self.CorrFilter[0] = self.filterConditions[selectedT][1]
                        self.CamShiftFilter[0] = self.filterConditions[selectedT][2]
                        self.Hist[0] = self.filterConditions[selectedT][3]
                        self.CFPropOnOff[0] = self.filterConditions[selectedT][4]
                        self.CFCamShiftOnOff[0] = self.filterConditions[selectedT][5]
            elif not len(self.filterConditions) == 0:
                self.filterConditions[selectedT][0] = self.ColorFilter[0]
                self.filterConditions[selectedT][1] = self.CorrFilter[0]
                self.filterConditions[selectedT][2] = self.CamShiftFilter[0]
                self.filterConditions[selectedT][3] = self.Hist[0]
                self.filterConditions[selectedT][4] = self.CFPropOnOff[0]
                self.filterConditions[selectedT][5] = self.CFCamShiftOnOff[0]

            cvui.rect(self.frame, WINDOW_FIL_X + 5, WINDOW_SOU_Y + 37, WINDOW_SOU_WIDTH - 10, WINDOW_SOU_HEIGHT - 75, 0x5c585a, 0x242223)
            if self.CFPropOnOff[0] and not len(self.filterConditions) == 0:
                if cvui.checkbox(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 30, "Color Filter", self.ColorFilter):
                    self.CamShiftFilter[0] = False
                    self.CorrFilter[0] = False
                    self.Hist[0] = False

                    if not len(self.trackers) == 0:
                        # CORRELATION FILTER
                        cvui.window(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 100, WINDOW_FILS_WIDTH - 20, WINDOW_FILS_WIDTH - 20, "Correlation Filter")
                        cvui.rect(self.frame, WINDOW_FILS_X + 12, WINDOW_FILS_Y + 125, WINDOW_FILS_WIDTH - 25, WINDOW_FILS_WIDTH - 50, 0x5c585a, 0x242223)
                        miniFilter = self.trackers[selectedT].getCorrFrame()
                        if miniFilter is not None:
                            miniFilter = self.rescale_frame_standar(miniFilter, WINDOW_FILS_WIDTH - 27)
                            miniFilter = cv.cvtColor(miniFilter, cv.COLOR_GRAY2BGR) * 255
                            x0 = WINDOW_FILS_X + 14
                            w = WINDOW_FILS_WIDTH - 27
                            h = np.asarray(miniFilter).shape[0]
                            y0 = int(((WINDOW_FILS_Y + 125 + (WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH - 50))/2.0) - h/2)
                            self.frame[y0:y0 + h, x0:x0 + w] = miniFilter
                        else:
                            miniFilter = self.lastFrame.copy()
                            miniFilter = self.rescale_frame_standar(miniFilter, WINDOW_FILS_WIDTH - 27)
                            x0 = WINDOW_FILS_X + 14
                            w = WINDOW_FILS_WIDTH - 27
                            h = np.asarray(miniFilter).shape[0]
                            y0 = int(((WINDOW_FILS_Y + 125 + (WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH - 50))/2.0) - h/2)
                            self.frame[y0:y0 + h, x0:x0 + w] = miniFilter

                if cvui.checkbox(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 50, "Correlation Filter",self.CorrFilter):
                    self.CamShiftFilter[0] = False
                    self.ColorFilter[0] = False
                    self.Hist[0] = False

                    if not len(self.trackers) == 0:
                        # LAB COLOR FILTER
                        cvui.window(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 100, WINDOW_FILS_WIDTH - 20, WINDOW_FILS_WIDTH - 20, "Color Filter")
                        cvui.rect(self.frame, WINDOW_FILS_X + 12, WINDOW_FILS_Y + 125, WINDOW_FILS_WIDTH - 25, WINDOW_FILS_WIDTH - 50, 0x5c585a, 0x242223)
                        self.trackers[selectedT].setFilter("FILTER_LAB")
                        miniFilter = self.trackers[selectedT].getFilteredFrame()
                        miniFilter = self.rescale_frame_standar(miniFilter, WINDOW_FILS_WIDTH - 27)
                        x0 = WINDOW_FILS_X + 14
                        w = WINDOW_FILS_WIDTH - 27
                        h = np.asarray(miniFilter).shape[0]
                        y0 = int(((WINDOW_FILS_Y + 125 + (WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH - 50))/2.0) - h/2)
                        self.frame[y0:y0 + h, x0:x0 + w] = miniFilter

            elif self.CFCamShiftOnOff[0] and not len(self.filterConditions) == 0:
                if cvui.checkbox(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 30, "Cam Shift", self.CamShiftFilter):
                    self.ColorFilter[0] = False
                    self.CorrFilter[0] = False
                    self.Hist[0] = False

                    if not len(self.trackers) == 0:
                        # HISTOGRAM
                        cvui.window(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 100, WINDOW_FILS_WIDTH - 20, WINDOW_FILS_WIDTH - 20, "Histogram")
                        cvui.rect(self.frame, WINDOW_FILS_X + 12, WINDOW_FILS_Y + 125, WINDOW_FILS_WIDTH - 25, WINDOW_FILS_WIDTH - 50, 0x5c585a, 0x242223)
                        miniFilter = self.trackers[selectedT].MF.hist_filter.get_histogram_plot()
                        miniFilter = self.rescale_hist(miniFilter, WINDOW_FILS_WIDTH - 27, WINDOW_FILS_WIDTH - 50)
                        x0 = WINDOW_FILS_X + 14
                        w = WINDOW_FILS_WIDTH - 27
                        h = np.asarray(miniFilter).shape[0]
                        y0 = int(WINDOW_FILS_Y + 125)
                        self.frame[y0:y0 + h, x0:x0 + w] = miniFilter

                        # CORRELATION FILTER
                        cvui.window(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 100 + WINDOW_FILS_WIDTH, WINDOW_FILS_WIDTH - 20, WINDOW_FILS_WIDTH - 20, "Correlation Filter")
                        cvui.rect(self.frame, WINDOW_FILS_X + 12, WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH, WINDOW_FILS_WIDTH - 25, WINDOW_FILS_WIDTH - 50, 0x5c585a, 0x242223)
                        miniFilter2 = self.trackers[selectedT].getCorrFrame()
                        if miniFilter2 is not None:
                            miniFilter2 = self.rescale_frame_standar(miniFilter2, WINDOW_FILS_WIDTH - 27)
                            miniFilter2 = cv.cvtColor(miniFilter2, cv.COLOR_GRAY2BGR) * 255
                            x0 = WINDOW_FILS_X + 14
                            w = WINDOW_FILS_WIDTH - 27
                            h = np.asarray(miniFilter2).shape[0]
                            y0 = int(((WINDOW_FILS_Y + 125 + (WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH - 50))/2.0) - h/2) + WINDOW_FILS_WIDTH
                            self.frame[y0:y0 + h, x0:x0 + w] = miniFilter2
                        else:
                            miniFilter = self.lastFrame.copy()
                            miniFilter = self.rescale_frame_standar(miniFilter, WINDOW_FILS_WIDTH - 27)
                            x0 = WINDOW_FILS_X + 14
                            w = WINDOW_FILS_WIDTH - 27
                            h = np.asarray(miniFilter).shape[0]
                            y0 = int(((WINDOW_FILS_Y + 125 + (WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH - 50))/2.0) - h/2) + WINDOW_FILS_WIDTH
                            self.frame[y0:y0 + h, x0:x0 + w] = miniFilter

                if cvui.checkbox(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 50, "Histogram", self.Hist):
                    self.ColorFilter[0] = False
                    self.CorrFilter[0] = False
                    self.CamShiftFilter[0] = False

                    if not len(self.trackers) == 0:
                        # CORRELATION FILTER
                        cvui.window(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 100, WINDOW_FILS_WIDTH - 20, WINDOW_FILS_WIDTH - 20, "Correlation Filter")
                        cvui.rect(self.frame, WINDOW_FILS_X + 12, WINDOW_FILS_Y + 125, WINDOW_FILS_WIDTH - 25, WINDOW_FILS_WIDTH - 50, 0x5c585a, 0x242223)
                        miniFilter = self.trackers[selectedT].getCorrFrame()
                        if miniFilter is not None:
                            miniFilter = self.rescale_frame_standar(miniFilter, WINDOW_FILS_WIDTH - 27)
                            miniFilter = cv.cvtColor(miniFilter, cv.COLOR_GRAY2BGR) * 255
                            x0 = WINDOW_FILS_X + 14
                            w = WINDOW_FILS_WIDTH - 27
                            h = np.asarray(miniFilter).shape[0]
                            y0 = int(((WINDOW_FILS_Y + 125 + (WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH - 50))/2.0) - h/2)
                            self.frame[y0:y0 + h, x0:x0 + w] = miniFilter

                        else:
                            miniFilter = self.lastFrame.copy()
                            miniFilter = self.rescale_frame_standar(miniFilter, WINDOW_FILS_WIDTH - 27)
                            x0 = WINDOW_FILS_X + 14
                            w = WINDOW_FILS_WIDTH - 27
                            h = np.asarray(miniFilter).shape[0]
                            y0 = int(((WINDOW_FILS_Y + 125 + (WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH - 50))/2.0) - h/2)
                            self.frame[y0:y0 + h, x0:x0 + w] = miniFilter

                        # LAB COLOR FILTER
                        cvui.window(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 100 + WINDOW_FILS_WIDTH, WINDOW_FILS_WIDTH - 20, WINDOW_FILS_WIDTH - 20, "Cam Shift")
                        cvui.rect(self.frame, WINDOW_FILS_X + 12, WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH, WINDOW_FILS_WIDTH - 25, WINDOW_FILS_WIDTH - 50, 0x5c585a, 0x242223)
                        self.trackers[selectedT].setFilter("FILTER_CSHIFT")
                        miniFilter2 = self.trackers[selectedT].getFilteredFrame()
                        miniFilter2 = self.rescale_frame_standar(miniFilter2, WINDOW_FILS_WIDTH - 27)
                        x0 = WINDOW_FILS_X + 14
                        w = WINDOW_FILS_WIDTH - 27
                        h = np.asarray(miniFilter2).shape[0]
                        y0 = int(((WINDOW_FILS_Y + 125 + (WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH - 50))/2.0) - h/2) + WINDOW_FILS_WIDTH
                        self.frame[y0:y0 + h, x0:x0 + w] = miniFilter2

                if cvui.checkbox(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 70, "Correlation Filter", self.CorrFilter):
                    self.CamShiftFilter[0] = False
                    self.ColorFilter[0] = False
                    self.Hist[0] = False

                    if not len(self.trackers) == 0:
                        # LAB COLOR FILTER
                        cvui.window(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 100, WINDOW_FILS_WIDTH - 20, WINDOW_FILS_WIDTH - 20, "Cam Shift")
                        cvui.rect(self.frame, WINDOW_FILS_X + 12, WINDOW_FILS_Y + 125, WINDOW_FILS_WIDTH - 25, WINDOW_FILS_WIDTH - 50, 0x5c585a, 0x242223)
                        self.trackers[selectedT].setFilter("FILTER_CSHIFT")
                        miniFilter2 = self.trackers[selectedT].getFilteredFrame()
                        miniFilter2 = self.rescale_frame_standar(miniFilter2, WINDOW_FILS_WIDTH - 27)
                        x0 = WINDOW_FILS_X + 14
                        w = WINDOW_FILS_WIDTH - 27
                        h = np.asarray(miniFilter2).shape[0]
                        y0 = int(((WINDOW_FILS_Y + 125 + (WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH - 50))/2.0) - h/2)
                        self.frame[y0:y0 + h, x0:x0 + w] = miniFilter2

                        # HISTOGRAM
                        cvui.window(self.frame, WINDOW_FILS_X + 10, WINDOW_FILS_Y + 100 + WINDOW_FILS_WIDTH, WINDOW_FILS_WIDTH - 20, WINDOW_FILS_WIDTH - 20, "Histogram")
                        cvui.rect(self.frame, WINDOW_FILS_X + 12, WINDOW_FILS_Y + 125 + WINDOW_FILS_WIDTH, WINDOW_FILS_WIDTH - 25, WINDOW_FILS_WIDTH - 50, 0x5c585a, 0x242223)
                        miniFilter2 = self.trackers[selectedT].MF.hist_filter.get_histogram_plot()
                        miniFilter2 = self.rescale_hist(miniFilter2, WINDOW_FILS_WIDTH - 27, WINDOW_FILS_WIDTH - 50)
                        x0 = WINDOW_FILS_X + 14
                        w = WINDOW_FILS_WIDTH - 27
                        h = np.asarray(miniFilter2).shape[0]
                        y0 = int(WINDOW_FILS_Y + 125) + WINDOW_FILS_WIDTH
                        self.frame[y0:y0 + h, x0:x0 + w] = miniFilter2

            if not selectedT == -1:
                cvui.printf(self.frame, 20, 775, 0.4, 0xdd97fb, "Missing Algorithm")
                if cvui.checkbox(self.frame, 20, 790, "Correlation", self.missAlgCorr):
                    self.missAlgST[0] = False
                else:
                    self.missAlgST[0] = True

                if cvui.checkbox(self.frame, 150, 790, "ST", self.missAlgST):
                    self.missAlgCorr[0] = False
                else:
                    self.missAlgCorr[0] = True

                cvui.printf(self.frame, 20, 810, 0.4, 0xdd97fb, "Recalculation Algorithm")
                if cvui.checkbox(self.frame, 20, 825, "Correlation", self.recAlgCorr):
                    self.recAlgST[0] = False
                else:
                    self.recAlgST[0] = True

                if cvui.checkbox(self.frame, 150, 825, "ST", self.recAlgST):
                    self.recAlgCorr[0] = False
                else:
                    self.recAlgCorr[0] = True

            
                if (self.missAlgCorr[0] or self.recAlgCorr[0]) and not self.replaceRoi:
                    cvui.printf(self.frame, 20, 850, 0.4, 0xdd97fb, "Mask Correlation")
                    cvui.trackbar(self.frame, 20, 865, 210, self.maskCondition, 0.0, 1.0, 1, "%0.2Lf", cvui.TRACKBAR_HIDE_SEGMENT_LABELS, 1)

            if not self.replaceRoi:
                if (cvui.button(self.frame, 20, 915, "Reset Settings")):
                    self.resetInitialCond()
                if (cvui.button(self.frame, WINDOW_SET_WIDTH + WINDOW_SET_X - 90, 915, "Auto CS")):
                    if not selectedT == -1 and self.CFCamShiftOnOff[0]:
                        params = self.trackers[selectedT].calculate_optimal_params()
                        self.camShift_bins[0] = params["bins"]
                        self.camShift_mb[0] = params["mask_blur"]
                        self.camShift_sb[0] = params["kernel_blur"]
                        self.camShift_lbpt[0] = params["low_pth"]

            alreadyTex = False
            nizu = 0
            for i in range(len(self.trackers)):
                if self.trackers[i].SC.trackingError:
                    if not alreadyTex:
                        cvui.printf(self.frame, WINDOW_SOU_X + 5, WINDOW_SOU_Y + 25, 0.4, 0xdc1076, 'Tracker Error In Tracker:')        #0xdc2710
                        alreadyTex = True
                    cvui.printf(self.frame, WINDOW_SOU_X + 165 + nizu * 10, WINDOW_SOU_Y + 25, 0.4, self.trackerColors[i], f'{i + 1}')
                    nizu += 1


            cvui.rect(self.frame, WINDOW_SOU_X + 5, WINDOW_SOU_Y + 37, WINDOW_SOU_WIDTH - 10, WINDOW_SOU_HEIGHT - 75, 0x5c585a, 0x242223)
            if ((self.usingCamera) or (self.usingVideo)):
                if not (self.pause or self.replaceRoi):
                    if self.callSource():
                        self.frame[self.sourceY:self.sourceY + self.sourceHEIGHT, self.sourceX:self.sourceX + self.sourceWIDTH] = self.source
                    else:
                        self.frame[self.sourceY:self.sourceY + self.sourceHEIGHT, self.sourceX:self.sourceX + self.sourceWIDTH] = self.lastEditedFrame #self.lastFrame
                        #Hubo algún tipo de error al cargar la camara o me quedé sin video
                        #Muestro el último frame que cargué

                    if self.boolVideoLoaded:
                        del self.arrayVideoLoaded[0]
                        if len(self.arrayVideoLoaded) == 0:
                            self.CurrentSource = "Video Ended. Load A New One!"
                            self.boolVideoLoaded = False
                else:
                    if self.changeInTrackers and ((self.usingVideo and not len(self.arrayVideoLoaded) == 0) or self.usingCamera):
                        self.changeInTrackers = False
                        self.callFilterPause()
                    if self.usingVideo and len(self.arrayVideoLoaded) == 0:
                        self.frame[self.sourceY:self.sourceY + self.sourceHEIGHT, self.sourceX:self.sourceX + self.sourceWIDTH] = self.lastEditedFrame #self.lastFrame
                    else:
                        self.frame[self.sourceY:self.sourceY + self.sourceHEIGHT, self.sourceX:self.sourceX + self.sourceWIDTH] = self.source

            if (self.usingVideo or self.usingCamera) and (self.ColorFilter[0] or self.CamShiftFilter[0] or self.CorrFilter[0] or self.Hist[0]):
                self.updateFilterFrame()
                x0 = self.sourceX + WINDOW_SOU_WIDTH + WINDOW_VS_X
                if self.filteredFrame is None:
                    self.frame[self.sourceY:self.sourceY + self.sourceHEIGHT, x0:x0 + self.sourceWIDTH] = self.lastFrame
                else:
                    if self.pause or self.replaceRoi:
                        self.callFilterPause()
                    y0 = int(((WINDOW_SOU_Y + 37) + (WINDOW_SOU_Y + 37 + WINDOW_SOU_HEIGHT - 75))/2 - self.filterHEIGHT/2)
                    self.frame[y0:y0 + self.filterHEIGHT, x0:x0 + self.filterWIDTH] = self.filteredFrame

            #Help Frame
            cvui.rect(self.frame, 210, 182, 20, 20, 0x494949, 0x545454)
            cvui.text(self.frame, 215, 185, "?", 0.6)
            if not cvui.iarea(210, 182, 20, 20) == cvui.OUT:
                cvui.window(self.frame, WINDOW_SOU_X, WINDOW_SET_Y, 500, 300, "Help")
                cvui.rect(self.frame, WINDOW_SOU_X + 9, WINDOW_SET_Y + 33, 3, 3, 0xdd97fb, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 30, "Begin loading a video or turning on the camera. Videos will start paused", 0.4, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 50, "by default.", 0.4, 0xdd97fb)

                cvui.rect(self.frame, WINDOW_SOU_X + 9, WINDOW_SET_Y + 73, 3, 3, 0xdd97fb, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 70, "Add up to 5 different trackers. Tracker Settings will be only available", 0.4, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 90, "when selecting a tracker.", 0.4, 0xdd97fb)

                cvui.rect(self.frame, WINDOW_SOU_X + 9, WINDOW_SET_Y + 113, 3, 3, 0xdd97fb, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 110, "The Filter Selection will be available after selecting a tracker and", 0.4, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 130, "turning on a filter option in Mask FIlter (LAB or Cam Shift).", 0.4, 0xdd97fb)

                cvui.rect(self.frame, WINDOW_SOU_X + 9, WINDOW_SET_Y + 153, 3, 3, 0xdd97fb, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 150, "For the Color Filter you can re-select the mean color of the first", 0.4, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 170, "selection by clicking the kernel that corresponds.", 0.4, 0xdd97fb)

                cvui.rect(self.frame, WINDOW_SOU_X + 9, WINDOW_SET_Y + 193, 3, 3, 0xdd97fb, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 190, "You can configure each tracker with different conditions.", 0.4, 0xdd97fb)

                cvui.rect(self.frame, WINDOW_SOU_X + 9, WINDOW_SET_Y + 213, 3, 3, 0xdd97fb, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 210, "Reset Settings will set settings for the tracker select by default, while", 0.4, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 230, "Auto will stablish the best Cam Shift conditions for the selection.", 0.4, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 250, "Remeber this option is only available when a tracker is selected and", 0.4, 0xdd97fb)
                cvui.text(self.frame, WINDOW_SOU_X + 20, WINDOW_SET_Y + 270, "Cam Shift option is on.", 0.4, 0xdd97fb)


            if ((cvui.button(self.frame, 20, 180, "Add Tracker") and ( (self.usingVideo and not len(self.arrayVideoLoaded) == 0) or self.usingCamera)) or self.replaceRoi):

                if len(self.trackers) < MAX_TRACKERS:
                    self.replaceRoi = True

                    posX = 0
                    posY = 0
                    wid = 0
                    hei = 0

                    status = cvui.iarea(self.sourceX, self.sourceY, self.sourceWIDTH, self.sourceHEIGHT)
                    if status == cvui.CLICK or status == cvui.DOWN:
                        cursorRoi = cvui.mouse(WINDOW_NAME)
                        self.coordsRoi.append(cursorRoi.x)
                        self.coordsRoi.append(cursorRoi.y)

                    if len(self.coordsRoi) == 6:
                        if self.coordsRoi[4] <= int((self.coordsRoi[0] + self.coordsRoi[2])/2.0):
                            self.coordsRoi[0] = self.coordsRoi[4]
                        else:
                            self.coordsRoi[2] = self.coordsRoi[4]

                        if self.coordsRoi[5] <= int((self.coordsRoi[1] + self.coordsRoi[3])/2.0):
                            self.coordsRoi[1] = self.coordsRoi[5]
                        else:
                            self.coordsRoi[3] = self.coordsRoi[5]

                        del self.coordsRoi[5]
                        del self.coordsRoi[4]

                    if not len(self.coordsRoi) == 0 and (self.coordsRoi[0] != 0 or self.coordsRoi[1] != 0):
                        cvui.rect(self.frame, self.coordsRoi[0]-1, self.coordsRoi[1]-1, 3, 3, self.trackerColors[len(self.trackers)], self.trackerColors[len(self.trackers)])

                    if len(self.coordsRoi) == 4:
                        if self.coordsRoi[0] - self.coordsRoi[2] > 0:
                            posX = self.coordsRoi[2]
                            wid = self.coordsRoi[0] - self.coordsRoi[2]
                        else:
                            posX = self.coordsRoi[0]
                            wid = self.coordsRoi[2] - self.coordsRoi[0]

                        if self.coordsRoi[1] - self.coordsRoi[3] > 0:
                            posY = self.coordsRoi[3]
                            hei = self.coordsRoi[1] - self.coordsRoi[3]
                            b = self.coordsRoi[3]
                        else:
                            posY = self.coordsRoi[1]
                            hei = self.coordsRoi[3] - self.coordsRoi[1]
                            b = self.coordsRoi[3]

                        cvui.rect(self.frame, posX, posY, wid, hei, self.trackerColors[len(self.trackers)])
                        if not(b == 0):
                            cvui.rect(self.frame, self.coordsRoi[2] - 1, b - 1, 3, 3, self.trackerColors[len(self.trackers)], self.trackerColors[len(self.trackers)])
                            cvui.rect(self.frame, posX + wid - 1, posY - 1, 3, 3, self.trackerColors[len(self.trackers)], self.trackerColors[len(self.trackers)])
                            cvui.rect(self.frame, posX - 1, posY + hei - 1, 3, 3, self.trackerColors[len(self.trackers)], self.trackerColors[len(self.trackers)])

                    cvui.window(self.frame, WINDOW_SET_X + 5, 845, WINDOW_SET_WIDTH - 10, Y_SCREEN - 845 - WINDOW_VS_Y*2, "Selection Options")
                    cvui.rect(self.frame, WINDOW_SET_X + 7, 867, WINDOW_SET_WIDTH - 14, Y_SCREEN - 867 - WINDOW_VS_Y*2, self.trackerColors[len(self.trackers)], self.trackerColors[len(self.trackers)])
                    asiAndaBienElEnter = (cv.waitKey(1) == 13)
                    if ((cvui.button(self.frame, WINDOW_SET_X + 10, 890, "Ok") or asiAndaBienElEnter)  and (len(self.coordsRoi) >= 4)):
                        if not (wid == 0 or hei == 0):
                            posX = posX - self.sourceX
                            posY = posY - self.sourceY
                            self.changeInTrackers = True
                            self.trackerAdded = True
                            if self.boolVideoLoaded:
                                self.trackers.append(Tracker.Tracker((posX + wid/2, posY + hei/2), wid, hei,self.arrayVideoLoaded[0], self.parameters))
                                toRescale = self.arrayVideoLoaded[0][posY:posY + hei, posX:posX + wid].copy()
                            else:
                                self.trackers.append(Tracker.Tracker((posX + wid/2, posY + hei/2), wid, hei,self.source, self.parameters))
                                toRescale = self.lastFrame[posY:posY + hei, posX:posX + wid].copy()

                            self.trackers[-1].changeSettings(self.makeInitial())
                            self.filterConditions.append([False, False, False, False, COLORFILTER_ONOFF, CAMSHIFT_ONOFF])
                            self.configSelected.append(originalParam)
                            w = int(np.asarray(toRescale).shape[1])
                            h = int(np.asarray(toRescale).shape[0])
                            if w >= h:
                                self.kernel.append(self.rescale_frame_standar(toRescale, int((WINDOW_TRK_WIDTH-150)/MAX_TRACKERS) - 40))
                            else:
                                self.kernel.append(self.rescale_frame_standar2(toRescale, int((WINDOW_TRK_WIDTH - 150) / MAX_TRACKERS) - 40))

                        self.coordsRoi.clear()
                        self.replaceRoi = False

                    if (cvui.button(self.frame, WINDOW_SET_X + 73, 890, "Redo")):
                        self.coordsRoi.clear()
                    if (cvui.button(self.frame, WINDOW_SET_X + 148, 890, "Cancel")):
                        self.coordsRoi.clear()
                        self.replaceRoi = False
            else:
                self.trackerAdded = False

            #Show everything on the screen
            cvui.imshow(WINDOW_NAME, self.frame)

            #Check if ESC key was pressed
            if ((cv.waitKey(1) == 27) or not (cv.getWindowProperty(WINDOW_NAME, cv.WND_PROP_VISIBLE))):
                break

        if (self.usingVideo or self.usingCamera):
            self.cap.release()
        cv.destroyAllWindows()

        return True

    def openFile(self):
        root = tk.Tk()
        root.withdraw()
        file_path = ""
        file_path = filedialog.askopenfilename(initialdir="./", title="Select file", filetypes=(
            ("Video", "*.mp4"), ("Video", "*.wav"), ("Video", "*.avi"), ("all files", "*.*")))
        if (file_path == '') :
            return False
        else:
            self.videoPath = file_path
            justName = file_path.split('/')[-1]  # Con extension
            self.videoName = justName[0:len(justName) - 4]  # Sin extension
            return True

    def resetInitialCond(self):
        self.kalman_ptm[0] = INITIAL_KALMAN_PTM
        self.kalman_pc[0] = INITIAL_KALMAN_PC
        self.kalman_mc[0] = INITIAL_KALMAN_MC

        self.lk_mr[0] = INITIAL_LK_MR

        # self.CFPropOnOff[0] = False                    #Queda mejor sin reestablecer esto
        self.colorFilter_LihtThr[0] = COLORFILTER_LIGHTTHR
        self.colorFilter_a[0] = COLORFILTER_A
        self.colorFilter_b[0] = COLORFILTER_B
        self.maskBlur_lab[0] = MASKBLUR_LAB

        # self.CFCamShiftOnOff[0] = False                    #Queda mejor sin reestablecer esto
        self.camShift_bins[0] = CAMSHIFT_BIN
        self.camShift_mb[0] = CAMSHIFT_MB
        self.camShift_sb[0] = CAMSHIFT_SB
        self.camShift_lbpt[0] = CAMSHIFT_LBPT

        self.shit_MaxFeat[0] = SHIT_MAXFEAT
        self.shit_FeatQual[0] = SHIT_FEATQUAL
        self.shit_MinFeat[0] = SHIT_MINFEAT
        self.shit_Rec[0] = SHIT_REC

        self.ShiTPropOnOff[0] = INITIAL_ST_ONOFF
        self.shit_SPix[0] = SHIT_SPIX

        self.missAlgCorr[0] = [True]
        self.missAlgST[0] = [False]

        self.recAlgCorr[0] = [True]
        self.recAlgST[0] = [False]

        sT = self.IsTrackerSelected()
        if sT != 1:
            self.trackSelectionBGR[sT] = []

        self.maskCondition[0] = MASK_COND

    def initSource(self):
        self.resetInitialCond()
        self.trackers.clear()
        self.kernel.clear()

        self.replaceRoi = False
        self.coordsRoi.clear()

        self.source = []

        self.boolForTrackers.clear()
        self.trackerAdded = False

        self.arrayVideoLoaded.clear()
        self.boolVideoLoaded = False
        self.lastFrame = []
        self.lastEditedFrame = []
        self.lastFilterFrame = []
        self.filteredFrame = None

        self.deletedTracker = -1

        self.KalmanProp[0] = False
        self.LKProp[0] = False
        self.ShiTProp[0] = False
        self.CFProp[0] = False
        self.ColorFilter[0] = False
        self.CorrFilter[0] = False
        self.CamShiftFilter[0] = False
        self.Hist[0] = False
        self.CFPropOnOff[0] = COLORFILTER_ONOFF
        self.CFCamShiftOnOff[0] = CAMSHIFT_ONOFF

        if self.usingCamera:
            self.cap = cv.VideoCapture(0)
            self.pause = False
        else:
            self.cap = cv.VideoCapture(self.videoPath)

        if (self.cap.isOpened()):
            todoPiola, self.source = self.cap.read()

            if todoPiola:
                if self.usingVideo:
                    cvui.window(self.frame, WINDOW_VS_X, WINDOW_VS_Y, X_SCREEN - 2*WINDOW_VS_X, Y_SCREEN - 2*WINDOW_VS_Y, " ")
                    cvui.printf(self.frame, int(X_SCREEN/7), int(Y_SCREEN/4), 5, 0xe9d540, "Loading Video")
                    cvui.printf(self.frame, int(X_SCREEN/7 + 30), int(Y_SCREEN/2), 5, 0xe9d540, "Please Wait...")
                    cvui.imshow(WINDOW_NAME, self.frame)
                    cv.waitKey(1)
                    self.boolVideoLoaded = True
                    if self.loadFullVideo():
                        self.boolVideoLoaded = False
                        self.usingCamera = False
                        self.usingVideo = False
                        self.arrayVideoLoaded.clear()
                    self.lastFrame = self.arrayVideoLoaded[0].copy()
                    self.source = self.arrayVideoLoaded[0].copy()

                else:
                    self.source = self.rescale_frame_standar(self.source, STANDAR_WIDTH)
                    self.lastFrame = self.source.copy()
                    self.sourceWIDTH = int(self.source.shape[1])
                    self.sourceHEIGHT = int(self.source.shape[0])

                a = WINDOW_VS_WIDTH + 2*WINDOW_VS_X
                b = a + WINDOW_SOU_WIDTH
                c = (b+a)/2
                self.sourceX = int(c - self.sourceWIDTH/2)

                a = WINDOW_SOU_Y
                b = WINDOW_SOU_Y + WINDOW_SOU_HEIGHT
                c = (b+a)/2
                self.sourceY = int(c - self.sourceHEIGHT/2)
                return True

        return False

    def callSource(self):
        if self.boolVideoLoaded:
            if len(self.arrayVideoLoaded) == 0:
                todoPiola = False
            else:
                self.source = self.arrayVideoLoaded[0].copy()
                self.lastFrame = self.source.copy()
                todoPiola = True
        else:
            todoPiola, self.source = self.cap.read()

        if todoPiola:
            if self.usingCamera:
                self.source = self.rescale_frame_standar(self.source, STANDAR_WIDTH)
                self.lastFrame = self.source.copy()

            else:
                self.sourceWIDTH = int(self.source.shape[1])
                self.sourceHEIGHT = int(self.source.shape[0])

            selectedTr = self.IsTrackerSelected()
            if selectedTr != -1: # and not self.trackerChanged:
                self.checkParametersChange()

            for tracker in self.trackers:
                tracker.update(self.source)

            self.updateFilterFrame()

            self.updateArtist()

            self.lastEditedFrame = self.source.copy()

        return todoPiola

    def updateArtist(self):
        i = 0
        for tracker in self.trackers:
            r = (self.trackerColors[i] >> 16) & 0xff
            g = (self.trackerColors[i] >> 8) & 0xff
            b = self.trackerColors[i] & 0xff
            if self.ShowTrajectory[0]:
                self.source = Artist.Artist.trajectory(self.source, tracker.getTrajectory(), (b, g, r))
            if tracker.SC.trackingError is False:
                if self.ShowEstimate[0]:
                    self.source = Artist.Artist.estimate(self.source, *tracker.getEstimatedPosition(),
                                                         tracker.selectionWidth, tracker.selectionHeight, (b, g, r))
                if self.ShowShit[0]:
                    self.source = Artist.Artist.features(self.source, tracker.SC.features, (b, g, r))
            else:
                if self.ShowEstimate[0]:
                    self.source = Artist.Artist.estimate(self.source, *tracker.getEstimatedPosition(),
                                                         tracker.selectionWidth, tracker.selectionHeight, (b, g, r))
                self.source = Artist.Artist.searchArea(self.source, *tracker.getEstimatedPosition(),
                                                       tracker.SC.searchWidth, tracker.SC.searchHeight, (b, g, r))
            i += 1

    def callFilterPause(self):
        if self.boolVideoLoaded:
            self.source = self.arrayVideoLoaded[0].copy()
        else:
            self.source = self.lastFrame.copy()

        self.checkParametersChange()

        for tracker in self.trackers:
            tracker.MF.updateMaskFromSettings()

        if not len(self.trackers) == 0:
            filterOfInteres = self.IsTrackerSelected()
            self.lastFilterFrame = self.trackers[filterOfInteres].MF.filterFrame(self.source)
            self.updateFilterFrame()

        self.updateArtist()

        return True

    def updateFilterFrame(self):
        filterOfInteres = self.IsTrackerSelected()
        
        if not len(self.trackers) == 0:
            #LAB COLOR FILTER
            if self.ColorFilter[0] and self.CFPropOnOff[0]:
                self.trackers[filterOfInteres].setFilter("FILTER_LAB")
                self.filteredFrame = self.trackers[filterOfInteres].getFilteredFrame()
            #CAMSHIFT
            elif self.CamShiftFilter[0] and self.CFCamShiftOnOff[0]:
                self.trackers[filterOfInteres].setFilter("FILTER_CSHIFT")
                self.filteredFrame = self.trackers[filterOfInteres].getFilteredFrame()
            #CORRELATION FILTER
            elif self.CorrFilter[0] and (self.CFPropOnOff[0] or self.CFCamShiftOnOff[0]):
                self.filteredFrame = self.trackers[filterOfInteres].getCorrFrame()
                if self.filteredFrame is not None:
                    self.filteredFrame = self.rescale_frame_standar(self.filteredFrame, STANDAR_WIDTH)
                else:
                    self.filteredFrame = None
            #HISTOGRAM
            elif self.Hist[0] and self.CFCamShiftOnOff[0]:
                self.filteredFrame = self.trackers[filterOfInteres].MF.hist_filter.get_histogram_plot()
                self.filteredFrame = self.rescale_hist(self.filteredFrame, STANDAR_WIDTH, self.sourceHEIGHT)
            else:
                self.filteredFrame = None

        if self.CorrFilter[0] and self.filteredFrame is not None:
            self.filterWIDTH = int(len(self.filteredFrame[0, :]))
            self.filterHEIGHT = int(len(self.filteredFrame[:, 0]))
            self.filteredFrame = cv.cvtColor(self.filteredFrame, cv.COLOR_GRAY2BGR)*255
        else:
            self.filterWIDTH = self.sourceWIDTH
            self.filterHEIGHT = self.sourceHEIGHT

    def rescale_frame_standar(self, frame, maxWidth):
        width = int(frame.shape[1])
        height = int(frame.shape[0])
        dim = (maxWidth, int(maxWidth*height/width))
        return cv.resize(frame, dim, interpolation=cv.INTER_AREA)

    def rescale_frame_standar2(self, frame, maxWidth):
        width = int(frame.shape[1])
        height = int(frame.shape[0])
        dim = (int(maxWidth*width/height), maxWidth)
        return cv.resize(frame, dim, interpolation=cv.INTER_AREA)

    def rescale_hist(self, frame, width, height):
        dim = (int(width), int(height))
        return cv.resize(frame, dim, interpolation=cv.INTER_AREA)

    def loadParameters(self, selected):
        self.kalman_ptm[0] = self.configSelected[selected][0]
        self.kalman_pc[0] = self.configSelected[selected][1]
        self.kalman_mc[0] = self.configSelected[selected][2]

        self.lk_mr[0] = self.configSelected[selected][3]

        self.CFPropOnOff[0] = self.configSelected[selected][4]
        self.colorFilter_LihtThr[0] = self.configSelected[selected][5]
        self.colorFilter_a[0] = self.configSelected[selected][6]
        self.colorFilter_b[0] = self.configSelected[selected][7]
        self.maskBlur_lab[0] = self.configSelected[selected][24]

        self.CFCamShiftOnOff[0] = self.configSelected[selected][8]
        self.camShift_bins[0] = self.configSelected[selected][9]
        self.camShift_mb[0] = self.configSelected[selected][10]
        self.camShift_sb[0] = self.configSelected[selected][11]
        self.camShift_lbpt[0] = self.configSelected[selected][12]

        self.shit_MaxFeat[0] = self.configSelected[selected][13]
        self.shit_FeatQual[0] = self.configSelected[selected][14]
        self.shit_MinFeat[0] = self.configSelected[selected][15]
        self.shit_Rec[0] = self.configSelected[selected][16]

        self.ShiTPropOnOff[0] = self.configSelected[selected][17]
        self.shit_SPix[0] = self.configSelected[selected][18]

        self.missAlgCorr[0] = self.configSelected[selected][19]
        self.missAlgST[0] = self.configSelected[selected][20]

        self.recAlgCorr[0] = self.configSelected[selected][21]
        self.recAlgST[0] = self.configSelected[selected][22]

        self.maskCondition[0] = self.configSelected[selected][23]

        if len(self.configSelected[selected]) == 26:
            self.trackSelectionBGR[selected] = self.configSelected[selected][25]

    def updateParameters(self):
        self.parameters.clear()

        self.parameters.append(self.kalman_ptm[0])             #0x
        self.parameters.append(self.kalman_pc[0])              #1x
        self.parameters.append(self.kalman_mc[0])              #2x

        self.parameters.append(self.lk_mr[0])                  #3x

        self.parameters.append(self.CFPropOnOff[0])            #4 (?????)
        self.parameters.append(self.colorFilter_LihtThr[0])    #5X
        self.parameters.append(self.colorFilter_a[0])          #6X
        self.parameters.append(self.colorFilter_b[0])          #7X

        self.parameters.append(self.CFCamShiftOnOff[0])        #8 (???????)
        self.parameters.append(self.camShift_bins[0])          #9x
        self.parameters.append(self.camShift_mb[0])            #10x
        self.parameters.append(self.camShift_sb[0])            #11x
        self.parameters.append(self.camShift_lbpt[0])          #12x

        self.parameters.append(self.shit_MaxFeat[0])           #13x
        self.parameters.append(self.shit_FeatQual[0])          #14x
        self.parameters.append(self.shit_MinFeat[0])           #15x
        self.parameters.append(self.shit_Rec[0])               #16x

        self.parameters.append(self.ShiTPropOnOff[0])          #17
        self.parameters.append(self.shit_SPix[0])              #18

        self.parameters.append(self.missAlgCorr[0])            #19x
        self.parameters.append(self.missAlgST[0])              #20x

        self.parameters.append(self.recAlgCorr[0])             #21x
        self.parameters.append(self.recAlgST[0])               #22x

        self.parameters.append(self.maskCondition[0])          #23x

        self.parameters.append(self.maskBlur_lab[0])        #24

        selected = self.IsTrackerSelected()
        if selected != -1 and (not len(self.trackSelectionBGR[selected]) == 0):
            self.parameters.append(self.trackSelectionBGR[selected])        #25

    def IsTrackerSelected(self):
        filterOfInteres = -1
        for i in range(len(self.boolForTrackers)):
            if self.boolForTrackers[i] == [True]:
                filterOfInteres = i
                break
        return filterOfInteres

    def checkParametersChange(self):

        filterOfInteres = self.IsTrackerSelected()

        changes = False

        if not filterOfInteres == -1:
            self.parametersNew.clear()

            self.parametersNew.append(self.kalman_ptm[0])           #0
            self.parametersNew.append(self.kalman_pc[0])           #1
            self.parametersNew.append(self.kalman_mc[0])           #2

            self.parametersNew.append(self.lk_mr[0])           #3

            self.parametersNew.append(self.CFPropOnOff[0])                  #4       #
            self.parametersNew.append(self.colorFilter_LihtThr[0])           #5
            self.parametersNew.append(self.colorFilter_a[0])           #6
            self.parametersNew.append(self.colorFilter_b[0])           #7

            self.parametersNew.append(self.CFCamShiftOnOff[0])           #8          #
            self.parametersNew.append(self.camShift_bins[0])           #9
            self.parametersNew.append(self.camShift_mb[0])           #10
            self.parametersNew.append(self.camShift_sb[0])           #11
            self.parametersNew.append(self.camShift_lbpt[0])           #12

            self.parametersNew.append(self.shit_MaxFeat[0])           #13
            self.parametersNew.append(self.shit_FeatQual[0])           #14
            self.parametersNew.append(self.shit_MinFeat[0])           #15
            self.parametersNew.append(self.shit_Rec[0])           #16

            self.parametersNew.append(self.ShiTPropOnOff[0])           #17      #
            self.parametersNew.append(self.shit_SPix[0])           #18

            self.parametersNew.append(self.missAlgCorr[0])           # 19
            self.parametersNew.append(self.missAlgST[0])         # 20

            self.parametersNew.append(self.recAlgCorr[0])       # 21
            self.parametersNew.append(self.recAlgST[0])         # 22

            self.parametersNew.append(self.maskCondition[0])       # 23

            self.parametersNew.append(self.maskBlur_lab[0])  # 24

            sT = self.IsTrackerSelected()
            if sT != -1 and (not len(self.trackSelectionBGR[sT]) == 0):
                self.parametersNew.append(self.trackSelectionBGR[sT])
                if len(self.parametersNew) == 26:
                    if len(self.parameters) == 26:
                        if not (self.parametersNew[25][0] == self.parameters[25][0] and self.parametersNew[25][1] == self.parameters[25][1] and self.parametersNew[25][2] == self.parameters[25][2]):
                            changes = True  # Tracker BGR
                            self.trackers[sT].colorKernelChange(self.parametersNew[25])
                            self.trackers[sT].updateBGR(self.parametersNew[25])
                    else:
                        changes = True  # Tracker BGR
                        self.trackers[sT].colorKernelChange(self.parametersNew[25])
                        self.trackers[sT].updateBGR(self.parametersNew[25])

            if not(self.parametersNew[0] == self.parameters[0] and self.parametersNew[1] == self.parameters[1] and self.parametersNew[2] == self.parameters[2]) :
                changes = True         #Chequeo Kalman
                self.trackers[sT].updateKalman(self.parametersNew[0], self.parametersNew[1], self.parametersNew[2])

            if not(self.parametersNew[3] == self.parameters[3]):
                changes = True         #Chequeo Lucas-Kanade
                self.trackers[sT].updateLK(self.parametersNew[3])

            if not(self.parametersNew[4] == self.parameters[4]):
                changes = True        #Color Filter On/Off
                self.trackers[sT].updateColorFilter(self.parametersNew[4], self.parametersNew[5], self.parametersNew[6], self.parametersNew[7], self.parametersNew[24])
            elif not ((self.parametersNew[5] == self.parameters[5]) and (self.parametersNew[6] == self.parameters[6]) and (self.parametersNew[7] == self.parameters[7]) and (self.parametersNew[24] == self.parameters[24])):
                changes = True      #Chequeo Params de CF
                self.trackers[sT].updateColorFilter(self.parametersNew[4], self.parametersNew[5], self.parametersNew[6], self.parametersNew[7], self.parametersNew[24])

            if not(self.parametersNew[8] == self.parameters[8]):
                changes = True        #Cam Shift On/Off
                self.trackers[sT].updateCamShift(self.parametersNew[8], self.parametersNew[9], self.parametersNew[10], self.parametersNew[11], self.parametersNew[12])
            elif not(self.parametersNew[9] == self.parameters[9] and self.parametersNew[10] == self.parameters[10] and self.parametersNew[11] == self.parameters[11] and self.parametersNew[12] == self.parameters[12]):       #BINS
                changes = True
                self.trackers[sT].updateCamShift(self.parametersNew[8], self.parametersNew[9], self.parametersNew[10], self.parametersNew[11], self.parametersNew[12])

            if not(self.parametersNew[13] == self.parameters[13] and self.parametersNew[14] == self.parameters[14] and self.parametersNew[15] == self.parameters[15] and self.parametersNew[16] == self.parameters[16]):
                changes = True         #Chequeo Shi-Tomasi
                self.trackers[sT].updateShiT(self.parametersNew[13], self.parametersNew[14], self.parametersNew[15], self.parametersNew[16], self.parametersNew[17], self.parametersNew[18])

            if not(self.parametersNew[17] == self.parameters[17]):
                changes = True        #Shi-Tomasi On/Off
                self.trackers[sT].updateShiT(self.parametersNew[13], self.parametersNew[14], self.parametersNew[15], self.parametersNew[16], self.parametersNew[17], self.parametersNew[18])
            elif not(self.parametersNew[18] == self.parameters[18]):
                changes = True   #Chequeo Params Shi
                self.trackers[sT].updateShiT(self.parametersNew[13], self.parametersNew[14], self.parametersNew[15], self.parametersNew[16], self.parametersNew[17], self.parametersNew[18])

            if not(self.parametersNew[19] == self.parameters[19] and self.parametersNew[20] == self.parameters[20] and  self.parametersNew[21] == self.parameters[21] and  self.parametersNew[22] == self.parameters[22]):
                changes = True      #Missing and Search algorithm
                self.trackers[sT].updateMissinSearch(self.parametersNew[19], self.parametersNew[20], self.parametersNew[21], self.parametersNew[22])

            if not(self.parametersNew[23] == self.parameters[23]):
                changes = True      #Mask condition
                self.trackers[sT].updateMaskCond(self.parametersNew[23])

        if changes:
            self.configSelected[filterOfInteres] = self.parametersNew.copy()
            self.lastTracker = filterOfInteres

        return changes

    def loadFullVideo(self):

        todoPiola, someCrazyShit = self.cap.read()

        if someCrazyShit.shape[1] >= someCrazyShit.shape[0]:
            while todoPiola:
                someCrazyShit = self.rescale_frame_standar(someCrazyShit, STANDAR_WIDTH)
                self.arrayVideoLoaded.append(someCrazyShit)
                todoPiola, someCrazyShit = self.cap.read()
        else:
            while todoPiola:
                someCrazyShit = self.rescale_frame_standar2(someCrazyShit, WINDOW_SOU_HEIGHT - 80)
                self.arrayVideoLoaded.append(someCrazyShit)
                todoPiola, someCrazyShit = self.cap.read()

        self.sourceWIDTH = int(self.arrayVideoLoaded[0].shape[1])
        self.sourceHEIGHT = int(self.arrayVideoLoaded[0].shape[0])

        return todoPiola

    def makeInitial(self):
        vect = []
        vect.append(INITIAL_KALMAN_PTM)  # 0
        vect.append(INITIAL_KALMAN_PC)  # 1
        vect.append(INITIAL_KALMAN_MC)  # 2

        vect.append(INITIAL_LK_MR)  # 3

        vect.append(COLORFILTER_ONOFF)  # 4       # self.CFPropOnOff[0] == COLORFILTER_ONOFF = False
        vect.append(COLORFILTER_LIGHTTHR)  # 5
        vect.append(COLORFILTER_A)  # 6
        vect.append(COLORFILTER_B)  # 7

        vect.append(CAMSHIFT_ONOFF)  # 8          # self.CFCamShiftOnOff[0] == CAMSHIFT_ONOFF = False
        vect.append(CAMSHIFT_BIN)  # 9
        vect.append(CAMSHIFT_MB)  # 10
        vect.append(CAMSHIFT_SB)  # 11
        vect.append(CAMSHIFT_LBPT)  # 12

        vect.append(SHIT_MAXFEAT)  # 13
        vect.append(SHIT_FEATQUAL)  # 14
        vect.append(SHIT_MINFEAT)  # 15
        vect.append(SHIT_REC)  # 16

        vect.append(INITIAL_ST_ONOFF)  # 17            # self.ShiTPropOnOff[0] == INITIAL_ST_ONOFF = Flase
        vect.append(SHIT_SPIX)  # 18

        vect.append(MIS_COR)  # 19                        # self.missAlgCorr[0] == MIS_COR = True
        vect.append(MIS_ST)  # 20                          # self.missAlgST[0] == MIS_ST = False

        vect.append(REC_COR)  # 21                         # self.recAlgCorr[0] == REC_COR = True
        vect.append(REC_ST)  # 22                          # self.recAlgST[0] == REC_ST = True

        vect.append(MASK_COND)  # 23

        vect.append(0)  # 24
        return vect

def main():
    myGui = cvGui()
    myGui.onWork()


if __name__ == '__main__':
    main()