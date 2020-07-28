import cv2 as cv
import numpy as np

class HistFilter:
    """
    Color Probabilty distribuiton filter
    """
    def __init__(self):
        self.ranges = [0, 180]
        self.hist = None
        self.mask = None
        self.bins = 64
        self.mask_blur_size = 11 # Applies blur to the whole mask. LPF
        self.kernel_blur_size = 5 # Applies blur to the selection to spread the color. LPF
        self.low_pth = 230

        self.bins_opti = 0
        self.mask_blur_size_opti  = 0
        self.kernel_blur_size_opti = 0
        self.low_pth_opti = 0

        self.selection = None

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
        hist_size = max(bins, 1)
        hsv = src
        if self.kernel_blur_size != 0:
            hsv = cv.medianBlur(hsv, int(self.kernel_blur_size))
        hsv = cv.cvtColor(hsv, cv.COLOR_BGR2HSV)
        self.mask = cv.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))  #((0., 60., 32.))
        # self.mask = cv.medianBlur(self.mask,15)
        self.hist = cv.calcHist([hsv], [0], self.mask, [hist_size], self.ranges)
        cv.normalize(self.hist, self.hist, 0, 255, cv.NORM_MINMAX)
        self.hist = self.hist.reshape(-1)
        return self.hist

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
        EXPERIMENTAL
        Aplica un threshold a una imagen monocromatica para conseguir un
        Parameters
        ----------
        src:

        Returns
        -------

        """
        # thresholded = cv.adaptiveThreshold(src,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,5,2)
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

    def get_histogram_plot(self):
        self.compute_hist(self.selection,self.bins)
        bin_count = self.hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count * bin_w, 3), np.uint8)
        for i in range(bin_count):
            h = int(self.hist[i])
            cv.rectangle(img,
                         (i * bin_w + 2, 255),
                         ((i + 1) * bin_w - 2, 255 - h),
                         (int(180.0 * i / bin_count), 255, 255),
                         -1)
        histogram_plot = cv.cvtColor(img, cv.COLOR_HSV2BGR)
        return histogram_plot

    def get_mask(self, src):
        hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        # mask = cv.inRange(hsv, np.array((0., 60., 0)), np.array((180., 255., 255.)))

        prob = cv.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
        prob &= mask
        mask2 = cv.inRange(prob, self.low_pth, 255)
        cv.imshow("mascara",mask2)
        if self.mask_blur_size != 0:
            mask2 = cv.medianBlur(mask2, int(self.mask_blur_size))
        cv.imshow("mascara pasabajeada",mask2)


        return mask2

    def set_bins(self, num):
        self.bins = num

    def set_mask_blur(self, blur_size):
        if int(blur_size) %2 == 0:
            self.mask_blur_size = int(blur_size)+1
        else:
            self.mask_blur_size = int(blur_size)

    def set_kernel_blur(self, blur_size):
        if int(blur_size) % 2 == 0:
            self.kernel_blur_size = int(blur_size)+1
        else:
            self.kernel_blur_size = int(blur_size)

    def set_low_pth(self, low_pth):
        self.low_pth = low_pth

class MaskingFilter:

    def __init__(self):
        self.maskingType = dict(
            FILTER_OFF=0,
            FILTER_LAB=1,
            FILTER_CSHIFT=2,
        )
        self.LSemiAmp = 50
        self.aSemiAmp = 15
        self.bSemiAmp = 15
        self.ksize = 3
        self.labMaxChange = 1
        self.CIELabRecalculationNumber = 1
        self.labPeriodicRecalculations = False  # NO

        self.mask = self.maskingType["FILTER_CSHIFT"]
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

    def calculateNewMask(self, frame, selection,newColor = False,color= None):
        if self.mask is self.maskingType["FILTER_OFF"]:
            pass
        else:
            if newColor is True:
                medb, medg, medr = color[0], color[1], color[2]
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
            if (newColor is False):
                self.hist_filter.selection = selection
                self.hist_filter.compute_hist(selection, self.hist_filter.bins)

        self.init = False

    def filterFrame(self, frame):
        if self.mask is self.maskingType["FILTER_OFF"]:
            pass
        elif self.mask is self.maskingType["FILTER_LAB"]:
            frameLab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
            mask = cv.inRange(frameLab, self.lowerThreshold, self.upperThreshold)
            if self.ksize > 1:
                mask = cv.medianBlur(mask, self.ksize)
            self.filteredFrame = cv.bitwise_and(frame, frame, mask=mask)
        elif self.mask is self.maskingType["FILTER_CSHIFT"]:
            mask1 = self.hist_filter.get_mask(frame)
            self.filteredFrame = cv.bitwise_and(frame, frame, mask = mask1)
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
        elif self.mask is self.maskingType["FILTER_CSHIFT"]:
            self.hist_filter.compute_hist(self.hist_filter.selection, self.hist_filter.bins)

    # def change_masking_filter(self,mask_type):
    #     if mask_type ==
