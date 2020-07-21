import cv2 as cv
import numpy as np


class MaskingFilter:

    maskingType = dict(
            FILTER_OFF = 0,
            FILTER_LAB = 1,
            FILTER_CSHIFT = 2,
            FILTER_CORR = 3
    )
    mask = maskingType["FILTER_LAB"]

    LSemiAmp = 50
    aSemiAmp = 15
    bSemiAmp = 15
    labMaxChange = 1
    CIELabRecalculationNumber = 5
    labPeriodicRecalculations = False

    def __init__(self):
        self.mask = self.maskingType["FILTER_LAB"]
        self.filteredFrame = None
        self.init = True
        #CIE LAB INIT
        self.lowerThreshold = 0
        self.upperThreshold = 0
        self.bgrmask =[0,0,0]
        self.lab_mask = None
        #CAMSHIFT INIT
        #CORRELATION INIT

    def calculateNewMask(self, frame, selection):
        if self.mask is self.maskingType["FILTER_OFF"]:
            pass
        elif self.mask is self.maskingType["FILTER_LAB"]:

            medb, medg, medr = np.median(selection[:, :, 0]), np.median(selection[:, :, 1]), np.median(selection[:, :, 2])
            if ~np.isnan(medb)&~np.isnan(medg)&~np.isnan(medr):
                bgr_mask = np.uint8([[[medb, medg, medr]]])
                self.bgrmask = [medb, medg, medr]
                self.lab_mask = cv.cvtColor(bgr_mask, cv.COLOR_BGR2LAB)

                if self.init is True:
                    L_low = np.clip(np.int32(self.lab_mask[0, 0, :])[0] - self.LSemiAmp, 1, 255)
                    a_low = np.clip(np.int32(self.lab_mask[0, 0, :])[1] - self.aSemiAmp, 1, 255)
                    b_low = np.clip(np.int32(self.lab_mask[0, 0, :])[2] - self.bSemiAmp, 1, 255)
                    L_high = np.clip(np.int32(self.lab_mask[0, 0, :])[0] + self.LSemiAmp, 1, 255)
                    a_high = np.clip(np.int32(self.lab_mask[0, 0, :])[1] + self.aSemiAmp, 1, 255)
                    b_high = np.clip(np.int32(self.lab_mask[0, 0, :])[2] + self.bSemiAmp, 1, 255)
                    self.lowerThreshold = np.array([L_low, a_low, b_low])
                    self.upperThreshold = np.array([L_high, a_high, b_high])
                else:

                    self.lowerThreshold[0] += np.clip(np.clip(np.int32(self.lab_mask[0, 0, :])[0] - self.LSemiAmp, 1, 255) - self.lowerThreshold[0], -self.labMaxChange, self.labMaxChange)
                    self.lowerThreshold[1] += np.clip(np.clip(np.int32(self.lab_mask[0, 0, :])[1] - self.LSemiAmp, 1, 255) - self.lowerThreshold[1], -self.labMaxChange, self.labMaxChange)
                    self.lowerThreshold[2] += np.clip(np.clip(np.int32(self.lab_mask[0, 0, :])[2] - self.LSemiAmp, 1, 255) - self.lowerThreshold[2], -self.labMaxChange, self.labMaxChange)
                    self.upperThreshold[0] += np.clip(np.clip(np.int32(self.lab_mask[0, 0, :])[0] + self.LSemiAmp, 1, 255) - self.upperThreshold[0], -self.labMaxChange, self.labMaxChange)
                    self.upperThreshold[1] += np.clip(np.clip(np.int32(self.lab_mask[0, 0, :])[1] + self.LSemiAmp, 1, 255) - self.upperThreshold[1], -self.labMaxChange, self.labMaxChange)
                    self.upperThreshold[2] += np.clip(np.clip(np.int32(self.lab_mask[0, 0, :])[2] + self.LSemiAmp, 1, 255) - self.upperThreshold[2], -self.labMaxChange, self.labMaxChange)

        elif self.mask is self.maskingType["FILTER_CSHIFT"]:
            pass
        elif self.mask is self.maskingType["FILTER_CORR"]:
            pass
        self.init = False

    def filterFrame(self, frame):
        if self.mask is self.maskingType["FILTER_OFF"]:
            pass
        elif self.mask is self.maskingType["FILTER_LAB"]:

            frameLab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
            mask = cv.inRange(frameLab, self.lowerThreshold, self.upperThreshold)
            self.filteredFrame = cv.bitwise_and(frame, frame, mask=mask)

        elif self.mask is self.maskingType["FILTER_CSHIFT"]:
            pass
        elif self.mask is self.maskingType["FILTER_CORR"]:
            pass
        return self.filteredFrame


    def updateMaskFromSettings(self):
        L_low = np.clip(np.int32(self.lab_mask[0, 0, :])[0] - self.LSemiAmp, 1, 255)
        a_low = np.clip(np.int32(self.lab_mask[0, 0, :])[1] - self.aSemiAmp, 1, 255)
        b_low = np.clip(np.int32(self.lab_mask[0, 0, :])[2] - self.bSemiAmp, 1, 255)
        L_high = np.clip(np.int32(self.lab_mask[0, 0, :])[0] + self.LSemiAmp, 1, 255)
        a_high = np.clip(np.int32(self.lab_mask[0, 0, :])[1] + self.aSemiAmp, 1, 255)
        b_high = np.clip(np.int32(self.lab_mask[0, 0, :])[2] + self.bSemiAmp, 1, 255)
        self.lowerThreshold = np.array([L_low, a_low, b_low])
        self.upperThreshold = np.array([L_high, a_high, b_high])


