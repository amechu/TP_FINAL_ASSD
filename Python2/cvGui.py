import cv2 as cv
import cvui
import numpy as np
import tkinter as tk
from tkinter import filedialog

WINDOW_NAME = "MAGT Video Tracker"

INITIAL_KALMAN_PTM = 1.2
INITIAL_KALMAN_PC = 0.006
INITIAL_KALMAN_MC = 0.4

INITIAL_LK_MR = 4.0

COLORFILTER_LIGHTTHR = 70.0
COLORFILTER_A = 20.0
COLORFILTER_B = 20.0
LIGHTTHR_X = 1.0
LIGHTTHR_MACT = 1.0

SHIT_MAXFEAT = 100.0
SHIT_FEATQUAL = 0.001
SHIT_MINFEAT = 0.01
SHIT_REC = 20.0
SHIT_SPIX = 4.0

class cvGui():

    def __init__(self, *args, **kw):

        #Frames
        self.frame = np.zeros((800, 1280, 3), np.uint8)
        self.source = []

        #Source names    
        self.VideoLoaded = "None"
        self.CurrentSource = "None"
        self.DebugModeString = "Off"
        self.videoName = ""                 
        self.videoPath = ""                  
        self.videoExtension = ""
    
        #Neededs for source
        self.usingCamera = False
        self.usingVideo = False
        #self.capCam = cv.VideoCapture
        self.cap = cv.VideoCapture
    
        #Bools and properties values
        self.DebugMode = [False]
        self.DebugModeChanged = True
    
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
        self.CFPropOnOff = [False]
        self.CFLRPropOnOff = [False]
    
        self.ColorFilterActive = [False]
        self.LightRecalcActive = [False]
    
        self.colorFilter_LihtThr = [COLORFILTER_LIGHTTHR]
        self.colorFilter_a = [COLORFILTER_A]
        self.colorFilter_b = [COLORFILTER_B]
        self.ligtRec_x = [LIGHTTHR_X]
        self.ligtRec_maxT = [LIGHTTHR_MACT]
    
        #Shi - Tomasi Properties
        self.ShiTProp = [False]
        self.ShiTPropOnOff = [False]
    
        self.ShiTPropActive = [False]
    
        self.shit_MaxFeat = [SHIT_MAXFEAT]
        self.shit_FeatQual = [SHIT_FEATQUAL]
        self.shit_MinFeat = [SHIT_MINFEAT]
        self.shit_Rec = [SHIT_REC]
        self.shit_SPix = [SHIT_SPIX]
        
        cv.namedWindow(WINDOW_NAME)
        cvui.init(WINDOW_NAME)

    def onWork(self):
        while True:
            self.frame[:] = (49, 52, 49)

            #FRAMES
            cvui.window(self.frame, 10, 10, 230, 130, "Video Source:")  #Video Source Frame
            cvui.window(self.frame, 10, 150, 230, 605, "Settings:")     #Settings Frame

            #Text
            cvui.printf(self.frame, 20, 35, 0.4, 0xdd97fb, "Current Source:")                      #Video Source
            cvui.printf(self.frame, 20, 50, 0.4, 0xdd97fb, self.CurrentSource)               #Video Source
            cvui.printf(self.frame, 135, 282, 0.4, 0xdd97fb, self.DebugModeString)           #Debug Mode
            if self.verifyInitialCond() :
                cvui.printf(self.frame, 20, 255, 0.4, 0xdd97fb, "Settings Selected By Default")
            else :
                cvui.printf(self.frame, 20, 255, 0.4, 0xdd97fb, "Changes Saved!")

            #Video Source Buttons
            if (cvui.button(self.frame, 20, 70, "Use Video")):
                if (self.openFile()):
                    self.usingCamera = False
                    self.usingVideo = True
                    if(self.initSource()):                                                                #Chequear si se inicia bien
                        self.VideoLoaded = self.videoPath
                        self.CurrentSource = "Video Loaded: " + self.videoName
                    else:
                        self.usingCamera = False
                        self.usingVideo = False

                elif not self.usingCamera:
                    self.CurrentSource = "No Video Loaded"
            
            if (cvui.button(self.frame, 20, 105, "Use Camera")):
                if not self.usingCamera:
                    self.usingVideo = False
                    self.usingCamera = True
                    if (self.initSource()):                                                           #Chequear si se inicia bien
                        self.CurrentSource = "Camera On"
                    else:
                        self.usingVideo = False
                        self.usingCamera = False

            
            if (cvui.button(self.frame, 60, 760, "Reset Settings")):
                self.resetInitialCond()
            
            #Settings Buttons 
            if (cvui.button(self.frame, 20, 180, "Select New Area")):
                pass
                #Hacer algo

            if (cvui.button(self.frame, 20, 215, "Start Tracking")):
                pass
                #Hacer algo

            if (cvui.checkbox(self.frame, 20, 280, "Debug Mode", self.DebugMode)):
                if (self.DebugModeChanged):
                    self.DebugMode[0] = True
                    self.DebugModeString = "On"
                    self.DebugModeChanged = False
            else:
                self.DebugMode[0] = False
                self.DebugModeString = "Off"
                self.DebugModeChanged = True
            
            #Settings Poperties
            if (cvui.checkbox(self.frame, 20, 300, "Kalman", self.KalmanProp)):
                self.LKProp[0] = False
                self.CFProp[0] = False
                self.ShiTProp[0] = False

                cvui.printf(self.frame, 20, 400, 0.4, 0xdd97fb, "Process Time Multiplier")
                cvui.trackbar(self.frame, 20, 415, 210, self.kalman_ptm, 0.0, 2.0)
                cvui.printf(self.frame, 20, 470, 0.4, 0xdd97fb, "Process Covariance")
                cvui.trackbar(self.frame, 20, 485, 210, self.kalman_pc, 0.0, 1.0)
                cvui.printf(self.frame, 20, 540, 0.4, 0xdd97fb, "Measurement Covariance")
                cvui.trackbar(self.frame, 20, 555, 210, self.kalman_mc, 0.0, 1.0)

            if (cvui.checkbox(self.frame, 20, 320, "Lucas-Kanade", self.LKProp)):
                self.KalmanProp[0] = False
                self.CFProp[0] = False
                self.ShiTProp[0] = False
                
                cvui.printf(self.frame, 20, 400, 0.4, 0xdd97fb, "Maximum Recursion")
                cvui.trackbar(self.frame, 20, 415, 210, self.lk_mr, 0.0, 10.0)
            
            if (cvui.checkbox(self.frame, 20, 340, "Color Filter", self.CFProp)):
                self.KalmanProp[0] = False
                self.LKProp[0] = False
                self.ShiTProp[0] = False
                
                if (cvui.checkbox(self.frame, 20, 400, "Color Filter", self.CFPropOnOff)):
                    self.CFLRPropOnOff[0] = False
                    cvui.printf(self.frame, 20, 460, 0.4, 0xdd97fb, "Lightness Threshold")
                    cvui.trackbar(self.frame, 20, 475, 210, self.colorFilter_LihtThr, 0.0, 150.0)
                    cvui.printf(self.frame, 20, 530, 0.4, 0xdd97fb, "A Threshold")
                    cvui.trackbar(self.frame, 20, 545, 210, self.colorFilter_a, 0.0, 30.0)
                    cvui.printf(self.frame, 20, 600, 0.4, 0xdd97fb, "B Threshold")
                    cvui.trackbar(self.frame, 20, 615, 210, self.colorFilter_b, 0.0, 30.0)
                
                if (cvui.checkbox(self.frame, 20, 420, "Lightness Recalculation", self.CFLRPropOnOff)):
                    self.CFPropOnOff[0] = False
                    cvui.printf(self.frame, 20, 460, 0.4, 0xdd97fb, "Every X self.frames")
                    cvui.trackbar(self.frame, 20, 475, 210, self.ligtRec_x, 0.0, 150.0)
                    cvui.printf(self.frame, 20, 530, 0.4, 0xdd97fb, "Maximum Threshold Change")
                    cvui.trackbar(self.frame, 20, 545, 210, self.ligtRec_maxT, 0.0, 30.0)
                
            if (cvui.checkbox(self.frame, 20, 360, "Shi-Tomasi", self.ShiTProp)):
                self.KalmanProp[0] = False
                self.LKProp[0] = False
                self.CFProp[0] = False
                
                cvui.printf(self.frame, 20, 400, 0.4, 0xdd97fb, "Maximum Feature Quantity")
                cvui.trackbar(self.frame, 20, 415, 210, self.shit_MaxFeat, 1.0, 1000.0)
                
                cvui.printf(self.frame, 20, 470, 0.4, 0xdd97fb, "Feature Quality Level")
                cvui.trackbar(self.frame, 20, 485, 210, self.shit_FeatQual, 0.0, 1.0)
                
                cvui.printf(self.frame, 20, 540, 0.4, 0xdd97fb, "Minimum Feature Distance")
                cvui.trackbar(self.frame, 20, 555, 210, self.shit_MinFeat, 0.0, 1.0)
                
                cvui.printf(self.frame, 20, 610, 0.4, 0xdd97fb, "Search Pixel Enlargement")
                cvui.trackbar(self.frame, 20, 625, 210, self.shit_SPix, 0.0, 10.0)
                
                if (cvui.checkbox(self.frame, 20, 670, "Feature Recalculation", self.ShiTPropOnOff)):
                    cvui.printf(self.frame, 20, 690, 0.4, 0xdd97fb, "Every X self.frames")
                    cvui.trackbar(self.frame, 20, 705, 210, self.shit_Rec, 1.0, 100.0)
            
            #On / Off special parameters: CHECK WHEN CALLING CALLBACK
            
            if (cvui.checkbox(self.frame, 140, 340, "CF", self.ColorFilterActive) and (self.CFProp[0])):
                #Verifico si está activado
                cvui.printf(self.frame, 135, 402, 0.4, 0xdd97fb, "%s", "On")    #Printeo un on si está en pantalla su configuración
            elif (self.CFProp[0]):
                cvui.printf(self.frame, 135, 402, 0.4, 0xdd97fb, "%s", "Off")   #Solo printeo un off si está en pantalla su configuración
            
            if (cvui.checkbox(self.frame, 180, 340, "LR", self.LightRecalcActive) and (self.CFProp[0])):
                cvui.printf(self.frame, 200, 422, 0.4, 0xdd97fb, "%s", "On")
            elif (self.CFProp[0]):
                cvui.printf(self.frame, 200, 422, 0.4, 0xdd97fb, "%s", "Off")
            
            if (cvui.checkbox(self.frame, 140, 360, "FR", self.ShiTPropActive) and (self.ShiTProp[0])):
                cvui.printf(self.frame, 200, 672, 0.4, 0xdd97fb, "%s", "On")
            elif (self.ShiTProp[0]):
                cvui.printf(self.frame, 200, 672, 0.4, 0xdd97fb, "%s", "Off")
            
            #Update cvui internal stuff
            cvui.update()
    
            if ((self.usingCamera) or (self.usingVideo)) and (self.callSource()):       #SOURCE
                pass
                #self.source = np.zeros(self.frame.shape, dtype=np.bool)
                #self.source[:100, :100] = True
                #self.source.copyTo(self.frame(cv.Rect(500, 230, self.source.cols, self.source.rows)))
                
            #Show everything on the screen
            cv.imshow(WINDOW_NAME, self.frame)

            #Check if ESC key was pressed
            if ((cv.waitKey(1) == 27) or not (cv.getWindowProperty(WINDOW_NAME, cv.WND_PROP_VISIBLE))):
                break
                
        return True
                    
    def verifyInitialCond(self):
        if ((self.kalman_ptm == INITIAL_KALMAN_PTM) and (self.kalman_pc == INITIAL_KALMAN_PC) and (
                self.kalman_mc == INITIAL_KALMAN_MC) and (self.lk_mr == INITIAL_LK_MR) and
                (self.colorFilter_LihtThr == COLORFILTER_LIGHTTHR) and (self.colorFilter_a == COLORFILTER_A) and (
                        self.colorFilter_b == COLORFILTER_B) and (self.ligtRec_x == LIGHTTHR_X) and
                (self.ligtRec_maxT == LIGHTTHR_MACT) and (self.shit_MaxFeat == SHIT_MAXFEAT) and (
                        self.shit_FeatQual == SHIT_FEATQUAL) and (self.shit_MinFeat == SHIT_MINFEAT) and
                (self.shit_Rec == SHIT_REC) and (self.shit_SPix == SHIT_SPIX) and (self.ColorFilterActive == False) and (
                        self.LightRecalcActive == False) and (self.ShiTPropActive == False)) :
            return True
        elif ((self.colorFilter_LihtThr != COLORFILTER_LIGHTTHR) or (self.colorFilter_a != COLORFILTER_A) or (
                self.colorFilter_b != COLORFILTER_B) or (self.ligtRec_x != LIGHTTHR_X) or
            (self.ligtRec_maxT != LIGHTTHR_MACT) or (self.shit_SPix != SHIT_SPIX)):
            if ((self.ColorFilterActive[0] == False) and (self.LightRecalcActive[0] == False) and (self.ShiTPropActive[0] == False)):
                return True
            else:
                return False
        else :
            return False

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

        self.colorFilter_LihtThr[0] = COLORFILTER_LIGHTTHR
        self.colorFilter_a[0] = COLORFILTER_A
        self.colorFilter_b[0] = COLORFILTER_B
        self.ligtRec_x[0] = LIGHTTHR_X
        self.ligtRec_maxT[0] = LIGHTTHR_MACT

        self.shit_MaxFeat[0] = SHIT_MAXFEAT
        self.shit_FeatQual[0] = SHIT_FEATQUAL
        self.shit_MinFeat[0] = SHIT_MINFEAT
        self.shit_Rec[0] = SHIT_REC
        self.shit_SPix[0] = SHIT_SPIX

        self.ColorFilterActive[0] = False
        self.LightRecalcActive[0] = False
        self.ShiTPropActive[0] = False

    def initSource(self):
        self.source[:] = (49, 52, 49)
        if self.usingCamera:
            self.cap = cv.VideoCapture(0)
        else:
            self.cap = cv.VideoCapture(self.videoPath)

        return self.cap.isOpened()


    def callSource(self) :
        todoPiola, self.source = self.cap.read()
        cv.imshow('tuvi', self.source)
        return todoPiola


def main():
    myGui = cvGui()
    myGui.onWork()

if __name__ == '__main__':
    main()