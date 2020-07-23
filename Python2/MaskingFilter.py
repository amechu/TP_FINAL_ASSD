import cv2 as cv
import numpy as np

class HistFilter:
    """
    Color Probabilty distribuiton filter
    """
    def __init__(self):
        self.ranges = [0, 180]
        self.hist = None


    def compute_hist(self, src, bins=64):
        """
        This function computes the color distribuition probabilty
        for a given BGR image. Often used to compute Kernel histogram

        Parameters
        ----------
        src: source image. MUST be BGR.
        bins: ammounts of bins

        Returns
        -------
        hist: array like wiht size len(bins)
        """

        bins = bins
        hist_size = max(bins, 2)
        hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, np.array((0., 60., 0.)), np.array((180., 255., 255.)))  #((0., 60., 32.))
        hist = cv.calcHist([hsv], [0], mask, [hist_size], self.ranges)
        cv.normalize(hist, hist, 0, 255, cv.NORM_MINMAX)
        self.hist = hist.reshape(-1)
        # self.show_hist(hist)
        return hist

    def get_roi(self, bbox, src):
        """
        Parameters
        ----------
        bbox:array-like
            (x0,y0,w,h)
        src: np.array
            Source image
        Returns
        -------
        Sliced chunk of the desired frame

        """
        x0, y0, width, height = bbox
        return src[y0:y0 + height, x0:x0 + width]

    def apply_hist_mask(self, src, hist):
        """

        Parameters
        ----------
        src: np.array. Image frame
        hist: array-like. Contains Hue probability distribuiton

        Returns
        -------
        Returns image mask
        """
        ch = (0, 0)
        hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
        hue = np.empty(hsv.shape, hsv.dtype)
        cv.mixChannels([hsv], [hue], ch)
        backproj = cv.calcBackProject([hue], [0], self.hist, self.ranges, scale=1)
        return backproj

    def apply_threshold(self, src):
        """
        Aplica un threshold a una imagen monocromatica para conseguir un
        Parameters
        ----------
        src:

        Returns
        -------

        """
        thresholded = cv.inRange(src, np.array(200), np.array(255))
        return thresholded

    def show_hist(self, hist: np.array) -> None:
        """
        Displays Hue histogram

        Parameters
        ----------
        hist: 1-D numpy array
              color probability distribuition of a given selection
        """
        bin_count = hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count * bin_w, 3), np.uint8)
        for i in range(bin_count):
            h = int(hist[i])
            cv.rectangle(img,
                          (i * bin_w + 2, 255),
                          ((i + 1) * bin_w - 2, 255 - h),
                          (int(180.0 * i / bin_count), 255, 255),
                          -1)
        img = cv.cvtColor(img, cv.COLOR_HSV2BGR)
        cv.imshow('hist', img)

    def get_mask(self, src):

        res = self.apply_hist_mask(src, self.hist)
        res = self.apply_threshold(res)
        res = cv.medianBlur(res, 11)
        res = cv.dilate(res, (11, 11))
        return res

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
    CIELabRecalculationNumber = 1
    labPeriodicRecalculations = False # NO

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
        self.hist_filter = HistFilter()

        #CORRELATION INIT

    def calculateNewMask(self, frame, selection):
        if self.mask is self.maskingType["FILTER_OFF"]:
            pass
        else:
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

            #Histogram Filter init
            self.hist_filter.compute_hist(selection)
            self.hist_filter.show_hist(self.hist_filter.hist)

        self.init = False

    def filterFrame(self, frame):
        if self.mask is self.maskingType["FILTER_OFF"]:
            pass
        elif self.mask is self.maskingType["FILTER_LAB"]:
            frameLab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
            mask = cv.inRange(frameLab, self.lowerThreshold, self.upperThreshold)
            self.filteredFrame = cv.bitwise_and(frame, frame, mask=mask)
        elif self.mask is self.maskingType["FILTER_CSHIFT"]:
            mask1 = self.hist_filter.get_mask(frame)
            self.filteredFrame = cv.bitwise_and(frame,frame, mask = mask1)
        elif self.mask is self.maskingType["FILTER_CORR"]:
            pass
        return self.filteredFrame

    def updateMaskFromSettings(self):
        if self.mask is self.maskingType["FILTER_LAB"]:
            L_low = np.clip(np.int32(self.lab_mask[0, 0, :])[0] - self.LSemiAmp, 1, 255)
            a_low = np.clip(np.int32(self.lab_mask[0, 0, :])[1] - self.aSemiAmp, 1, 255)
            b_low = np.clip(np.int32(self.lab_mask[0, 0, :])[2] - self.bSemiAmp, 1, 255)
            L_high = np.clip(np.int32(self.lab_mask[0, 0, :])[0] + self.LSemiAmp, 1, 255)
            a_high = np.clip(np.int32(self.lab_mask[0, 0, :])[1] + self.aSemiAmp, 1, 255)
            b_high = np.clip(np.int32(self.lab_mask[0, 0, :])[2] + self.bSemiAmp, 1, 255)
            self.lowerThreshold = np.array([L_low, a_low, b_low])
            self.upperThreshold = np.array([L_high, a_high, b_high])
        else:
            return

    # def change_masking_filter(self,mask_type):
    #     if mask_type ==
