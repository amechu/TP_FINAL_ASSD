import cv2 as cv
import numpy as np
from ShiTomasi import ShiTomasi
from OpticalFlow import OpticalFlow

class Searcher:
    usualAlgorithmD = dict(
            LK_ST = 0,
            CORR = 1,
    )
    recalcAlgorithmD = dict(
            ST = 0,
            CORR = 1
    )
    missAlgorithmD = dict(
            ST = 0,
            CORR = 1,
    )
    usualAlgorithm = usualAlgorithmD["LK_ST"]
    missAlgorithm = missAlgorithmD["CORR"]
 #   missAlgorithm = missAlgorithmD["ST"]
#    recalcAlgorithm = recalcAlgorithmD["ST"]
    recalcAlgorithm = recalcAlgorithmD["CORR"]

    def __init__(self,firstFrame,selectionHeight_,selectionWidth_,xSelection,ySelection,prevFrameGrayC):
        self.LK = OpticalFlow()
        self.ST = ShiTomasi()
        self.prevFrameGray=prevFrameGrayC
        self.stdMultiplier=1
        self.selectionHeight= selectionHeight_
        self.selectionWidth = selectionWidth_
        self.kernelRGB= firstFrame[int(ySelection-selectionHeight_/2):int(ySelection+selectionHeight_/2) , int(xSelection-selectionWidth_/2):int(xSelection+selectionWidth_/2)]
        self.kernel = cv.cvtColor(self.kernelRGB, cv.COLOR_BGR2HSV)
        self.features=[]
        self.trackingError=False
        self.candidate=None
        self.searchWidth = 0
        self.searchHeight = 0
        self.debug=False
        self.corr_out=None
        self.y, self.x = np.shape(self.prevFrameGray)
        self.MASKCONDITION = selectionWidth_*selectionHeight_*0.8**2
        self.match_method = cv.TM_SQDIFF


    def searchMissing(self,estX,estY,frame,filteredframe):

        if self.missAlgorithm== self.missAlgorithmD["ST"]:
            candidate=[None,None]
            frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  #REVISAR
            self.features, self.trackingError = self.ST.recalculateFeatures(frameGray[int(estY - self.searchHeight / 2): int(estY + self.searchHeight / 2),int(estX - self.searchWidth / 2): int(estX + self.searchWidth / 2)])
            self.features = self.featureTranslate(estX- self.searchWidth / 2,estY - self.searchHeight / 2,self.features)
            if self.trackingError is True:
                self.searchWidth += self.ST.searchEnlargementThreshold
                self.searchHeight += self.ST.searchEnlargementThreshold
            else:
                self.searchHeight = self.selectionHeight
                self.searchWidth = self.selectionWidth
                candidate = np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1])
                self.LK.prevFeatures = self.features


        elif self.missAlgorithm == self.missAlgorithmD["CORR"]:
            frameGray = cv.cvtColor(filteredframe, cv.COLOR_BGR2GRAY)   
            frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = cv.inRange(frame_hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
            frame_hsv = cv.bitwise_and(frame_hsv, frame_hsv, mask)


            self.corr_out = cv.matchTemplate(frame_hsv, self.kernel, method=self.match_method)

            cv.normalize(self.corr_out, self.corr_out, 0, 1, cv.NORM_MINMAX)
            [minval, maxval, minLoc, maxLoc] = cv.minMaxLoc(self.corr_out)
            if (self.match_method == cv.TM_SQDIFF or self.match_method == cv.TM_SQDIFF_NORMED):
                matchLoc = minLoc
            else:
                matchLoc = maxLoc
            candidate = matchLoc

            frame_to_search =frameGray[int(matchLoc[1]): int(matchLoc[1] + self.selectionHeight ),int(matchLoc[0]): int(matchLoc[0] + self.selectionWidth )]

            if np.count_nonzero(filteredframe[int(matchLoc[1]): int(matchLoc[1] + self.selectionHeight ),int(matchLoc[0]): int(matchLoc[0] + self.selectionWidth )])  > self.MASKCONDITION:
                self.features, self.trackingError = self.ST.recalculateFeatures(frame_to_search)
                self.features = self.featureTranslate(int(matchLoc[0]), int(matchLoc[1]), self.features)
                self.LK.prevFeatures = self.features
            else:
                for i in range(10):
                    if(matchLoc[0] > self.selectionWidth/2  and matchLoc[0] < self.x - self.selectionWidth/2 and matchLoc[1] > self.selectionHeight/2  and matchLoc[1] < self.y - self.selectionHeight/2):
                        if (self.match_method == cv.TM_SQDIFF or self.match_method == cv.TM_SQDIFF_NORMED):
                            self.corr_out[int(matchLoc[1]-self.selectionHeight/2): int(matchLoc[1] + self.selectionHeight/2),int(matchLoc[0]-self.selectionWidth/2): int(matchLoc[0] + self.selectionWidth/2)] = 1
                        else:
                            self.corr_out[
                            int(matchLoc[1] - self.selectionHeight / 2): int(matchLoc[1] + self.selectionHeight / 2),
                            int(matchLoc[0] - self.selectionWidth / 2): int(matchLoc[0] + self.selectionWidth / 2)] = 0
                    else:
                        if (self.match_method == cv.TM_SQDIFF or self.match_method == cv.TM_SQDIFF_NORMED):
                            self.corr_out[int(matchLoc[1]): int(matchLoc[1] + self.selectionHeight),
                            int(matchLoc[0]): int(matchLoc[0] + self.selectionWidth)] = 1
                        else:
                            self.corr_out[int(matchLoc[1]): int(matchLoc[1] + self.selectionHeight),
                            int(matchLoc[0]): int(matchLoc[0] + self.selectionWidth)] = 0

                    [minval, maxval, minLoc, maxLoc] = cv.minMaxLoc(self.corr_out)
                    if (self.match_method == cv.TM_SQDIFF or self.match_method == cv.TM_SQDIFF_NORMED):
                        matchLoc = minLoc
                    else:
                        matchLoc = maxLoc
                    frame_to_search = frameGray[int(matchLoc[1]): int(matchLoc[1] + self.selectionHeight),
                                      int(matchLoc[0]): int(matchLoc[0] + self.selectionWidth)]
                    if np.count_nonzero(filteredframe[int(matchLoc[1]): int(matchLoc[1] + self.selectionHeight),
                                        int(matchLoc[0]): int(matchLoc[0] + self.selectionWidth)]) > self.MASKCONDITION:
                        self.features, self.trackingError = self.ST.recalculateFeatures(frame_to_search)
                        self.features = self.featureTranslate(int(matchLoc[0]), int(matchLoc[1]), self.features)
                        self.LK.prevFeatures = self.features
                    else:
                        self.trackingError=True
                    if self.trackingError == False:
                        break

        return candidate

    def search(self,frameCounter,frame,filteredFrame):
        if self.usualAlgorithm== self.usualAlgorithmD["LK_ST"]:
            frameGray = cv.cvtColor(filteredFrame, cv.COLOR_BGR2GRAY)
            # Apply LK algorithm
            self.features, self.trackingError = self.LK.updateFeatures(self.prevFrameGray, frameGray)
            if self.trackingError is False:  # Tracking error?
                # recaulculate features?
                if frameCounter != 0 and frameCounter % self.ST.frameRecalculationNumber == 0:
                    # yes
                    if(self.recalcAlgorithm == self.recalcAlgorithmD["ST"]):
                        medx, medy = np.median(self.features[:, 0, 0]), np.median(self.features[:, 0, 1])
                        std = np.sqrt((np.std(self.features[:, 0, 0])) ** 2 + (np.std(self.features[:, 0, 1])) ** 2)
                        # calculate mean and std of features
                        mask = (self.features[:, 0, 0] < medx + self.stdMultiplier * std + 0.1) & (self.features[:, 0, 0] > medx - self.stdMultiplier * std - 0.1) & (self.features[:, 0, 1] < medy + self.stdMultiplier * std + 0.1) \
                               & (self.features[:, 0, 1] > medy - self.stdMultiplier * std - 0.1)
                        self.features = self.features[mask]
                    # remove outliers.
                        medx, medy = np.median(self.features[:, 0, 0]), np.median(self.features[:, 0, 1])
                        self.features, self.trackingError = self.ST.recalculateFeatures(frameGray[int(medy - self.selectionHeight / 2): int(medy + self.selectionHeight / 2),int(medx - self.selectionWidth / 2): int(medx + self.selectionWidth / 2)])
                        self.features = self.featureTranslate(medx - self.selectionWidth / 2,medy - self.selectionHeight / 2, self.features)
                        self.LK.prevFeatures = self.features
                    elif(self.recalcAlgorithm == self.recalcAlgorithmD["CORR"]):
                        a= self.missAlgorithm
                        self.missAlgorithm = self.missAlgorithmD["CORR"]
                        medx,medy=self.searchMissing(0,0,frame,filteredFrame)
                        self.missAlgorithm = a

                    # apply st algorithm

                    if self.trackingError is False:  # did i find features?
                       # found, then KM correct.
                        self.candidate=np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1])
                 #else would be Features not found.
                else:  # NO, then kalman correct estimate.
                   self.candidate = np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1])
            self.prevFrameGray = frameGray
 #                   self.KM.correct(np.mean(self.features[:, 0, 0]), np.mean(self.features[:, 0, 1]))
 # Cuando vuelvo me fijo si hay tracking error, si es false aplico kalman
        # Recalculate features?
        #           else would be tracking error true



        return self.candidate[0],self.candidate[1]

    @staticmethod
    def featureTranslate(x, y, features):
        if features is None:
            return None
        for i in range(features.shape[0]):
            features[i][0][0] += x
            features[i][0][1] += y
        return features







#def correlationAllPic(frame,Kernel):#kernel bgr
#    match_method = cv.TM_SQDIFF
#    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#    kernel = cv.cvtColor(Kernel, cv.COLOR_BGR2HSV)
##    mask = cv.inRange(frame_hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
##    frame_hsv = cv.bitwise_and(frame_hsv, frame_hsv, mask)
 #   corr_out = cv.matchTemplate(frame_hsv, kernel, method=match_method)
 #   cv.normalize(corr_out, corr_out, 0, 1, cv.NORM_MINMAX)
 #   [minval, maxval, minLoc, maxLoc] = cv.minMaxLoc(corr_out)
 #   if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
 ##       matchLoc = minLoc
  #  else:
  ##      matchLoc = maxLoc
   # return [corr_out,matchLoc]


#def correlationSection(frame,x,y,w,h,Kernel): #kernel bgr
#    match_method = cv.TM_SQDIFF
#    frameselected = frame[int(y-h/2):int(y+h/2) , int(x-w/2):int(x+w/2)]
#    kernel = cv.cvtColor(Kernel, cv.COLOR_BGR2HSV)
#    frame_hsv = cv.cvtColor(frameselected, cv.COLOR_BGR2HSV) #aca ya tengo chikito :c

#    mask = cv.inRange(frame_hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
#    frame_hsv = cv.bitwise_and(frame_hsv, frame_hsv, mask)
#    corrOut = cv.matchTemplate(frame_hsv, kernel, method=match_method)

#    cv.normalize(corrOut, corrOut, 0, 1, cv.NORM_MINMAX)
#    [minval, maxval, minLoc, maxLoc] = cv.minMaxLoc(corrOut)
#    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
#        matchLoc = minLoc
 #   else:
 #       matchLoc = maxLoc
 #   RetPoint =  (matchLoc[0]+x-w/2 ,matchLoc[1]+y-h/2)
 #   return [corrOut,RetPoint]
