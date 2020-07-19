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

    LSemiAmp = 60
    aSemiAmp = 20
    bSemiAmp = 20
    CIELabRecalculationNumber = 1

    def __init__(self):
        self.mask = self.maskingType["FILTER_LAB"]
        self.filteredFrame = None
        #CIE LAB INIT
        self.lowerThreshold = 0
        self.upperThreshold = 0
        self.bgrmask =[0,0,0]
        #CAMSHIFT INIT

        #CORRELATION INIT

    def calculateNewMask(self, frame, selection):
        if self.mask is self.maskingType["FILTER_OFF"]:
            pass
        elif self.mask is self.maskingType["FILTER_LAB"]:

            # medianHue = np.median(cv.cvtColor(selection, cv.COLOR_BGR2HSV)[:,:,0])
            # hue_mask = np.uint8([[[medianHue, 255, 255]]])
            # bgr_mask = cv.cvtColor(hue_mask, cv.COLOR_HSV2BGR)
            # lab_mask = cv.cvtColor(bgr_mask, cv.COLOR_BGR2LAB)
            # L_low = 1
            # a_low = np.clip(np.int32(lab_mask[0, 0, :])[1] - self.aSemiAmp, 1, 255)
            # b_low = np.clip(np.int32(lab_mask[0, 0, :])[2] - self.bSemiAmp, 1, 255)
            # L_high = 255
            # a_high = np.clip(np.int32(lab_mask[0, 0, :])[1] + self.aSemiAmp, 1, 255)
            # b_high = np.clip(np.int32(lab_mask[0, 0, :])[2] + self.bSemiAmp, 1, 255)


            medb, medg, medr = np.median(selection[:, :, 0]), np.median(selection[:, :, 1]), np.median(selection[:, :, 2])
            bgr_mask = np.uint8([[[medb, medg, medr]]])
            self.bgrmask = [medb, medg, medr]
            lab_mask = cv.cvtColor(bgr_mask, cv.COLOR_BGR2LAB)
            L_low = np.clip(np.int32(lab_mask[0, 0, :])[0] - self.LSemiAmp, 1, 255)
            a_low = np.clip(np.int32(lab_mask[0, 0, :])[1] - self.aSemiAmp, 1, 255)
            b_low = np.clip(np.int32(lab_mask[0, 0, :])[2] - self.bSemiAmp, 1, 255)
            L_high = np.clip(np.int32(lab_mask[0, 0, :])[0] + self.LSemiAmp, 1, 255)
            a_high = np.clip(np.int32(lab_mask[0, 0, :])[1] + self.aSemiAmp, 1, 255)
            b_high = np.clip(np.int32(lab_mask[0, 0, :])[2] + self.bSemiAmp, 1, 255)

            self.lowerThreshold = np.array([L_low, a_low, b_low])
            self.upperThreshold = np.array([L_high, a_high, b_high])

        elif self.mask is self.maskingType["FILTER_CSHIFT"]:
            pass
        elif self.mask is self.maskingType["FILTER_CORR"]:
            pass

    def filterFrame(self, frame):
        if self.mask is self.maskingType["FILTER_OFF"]:
            pass
        elif self.mask is self.maskingType["FILTER_LAB"]:

            frameLab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
            mask = cv.inRange(frameLab, self.lowerThreshold, self.upperThreshold)
            self.filteredFrame = cv.bitwise_and(frame, frame, mask=mask)
            hola = 1

        elif self.mask is self.maskingType["FILTER_CSHIFT"]:
            pass
        elif self.mask is self.maskingType["FILTER_CORR"]:
            pass

        return self.filteredFrame

