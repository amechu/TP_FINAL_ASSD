import cv2 as cv
import numpy as np

import time
import sys

# KCF tracker


def correlationAllPic(frame, a):
    if a==1:
        match_method = cv.TM_CCORR
    else:
        match_method = cv.TM_SQDIFF
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame_hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    frame_hsv = cv.bitwise_and(frame_hsv, frame_hsv, mask)
    corr_out = cv.matchTemplate(frame_hsv, kernel, method=match_method)

    cv.normalize(corr_out, corr_out, 0, 1, cv.NORM_MINMAX)
    [minval, maxval, minLoc, maxLoc] = cv.minMaxLoc(corr_out)
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc = minLoc
    else:
        matchLoc = maxLoc
#    finalMask = cv.inRange(corr_out,0, 0.1)
#    finalMask= np.uint8(finalMask)
    return [corr_out,matchLoc]


def correlationSection(frame,x,y,w,h,Kernel): #Pasas punta izquierda con xy despues h y w
    match_method = cv.TM_SQDIFF
    frameselected = frame[int(y-h/2):int(y+h/2) , int(x-w/2):int(x+w/2)]

    frame_hsv = cv.cvtColor(frameselected, cv.COLOR_BGR2HSV) #aca ya tengo chikito :c

    mask = cv.inRange(frame_hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    frame_hsv = cv.bitwise_and(frame_hsv, frame_hsv, mask)
    corrOut = cv.matchTemplate(frame_hsv, Kernel, method=match_method)

    cv.normalize(corrOut, corrOut, 0, 1, cv.NORM_MINMAX)
    [minval, maxval, minLoc, maxLoc] = cv.minMaxLoc(corrOut)
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc = minLoc
    else:
        matchLoc = maxLoc
    RetPoint =  (matchLoc[0]+x-w/2 ,matchLoc[1]+y-h/2)
#    tinyFinalMask = cv.inRange(corrOut,0, 0.1)
#    finalMask=np.zeros((np.shape(frame)[0],np.shape(frame)[1]))

#    x0 = int(x - w/2)
#    y0 = int(y - h/2)

#    width = int(tinyFinalMask.shape[1])
#    height = int(tinyFinalMask.shape[0])

#    finalMask[y0:y0 + height, x0:x0 + width] = tinyFinalMask
#    finalMask= np.uint8(finalMask)
#    print(finalMask.shape)
#    print(np.shape(frame))
    return [corrOut,RetPoint]
# constant





if __name__ == '__main__':

#    cap = cv.VideoCapture("gido_completo.mp4")
    cap = cv.VideoCapture(0)
    for i in range(20):
        ret, frame = cap.read()
    cv.namedWindow('tracking')
    cv.namedWindow('kernel')
    cv.namedWindow('CORR')
    cv.namedWindow('SQ DIFF')

    first=True
    ret, frame = cap.read()
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame_hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    frame_hsv = cv.bitwise_and(frame_hsv, frame_hsv, mask)
    # Make kernel
    [x,y,w,h] = cv.selectROI('tracking', frame)
    kernel = frame_hsv[y:y+h , x:x+w]
    kernelRGB= frame[y:y+h , x:x+w]
    anchor = [-1,1]
    delta=0
    ddepht=-1
    cv.imshow('kernel',kernelRGB)
    color = (255, 0, 0)
    color2 = (255, 255, 0)

    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
#        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        deltax=w
        deltay=h
        ux=x+(deltax/2.0)
        uy=y+(deltay/2.0)
        [corrSQ, points]= correlationAllPic(frame,0)
        [corrOut, points]= correlationAllPic(frame,1)
   #     [corrOut,points] = correlationSection(frame,ux,uy,deltax+50,deltay+50,kernel)


    #    cv.rectangle(frame,(int(points[0]),int(points[1])),(int(points[0]+deltax) , int(points[1] +deltay)),color,2)

   #     filteredFrame = cv.bitwise_and(frame, frame, mask=finalmask)

        cv.imshow('tracking', frame)
        cv.imshow('CORR', corrOut)
        cv.imshow('SQ DIFF', corrSQ)


        c = cv.waitKey(30) & 0xFF
        if c == 27 or c == ord('q'):
            break



    cap.release()
    cv.destroyAllWindows()


