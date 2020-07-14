import cv2 as cv
import params as prm
import util as util
import kalman

kalman = kalman.KalmanFilter() #Se inicializa la clase del filtro de Kalman

#cap = cv.VideoCapture(cv.samples.findFile("videoPeq2.mp4"))
cap = cv.VideoCapture(cv.samples.findFile("gido_completo.mp4"))
#cap = cv.VideoCapture(cv.samples.findFile("pendulo_tobi.mp4"))
#cap = cv.VideoCapture(cv.samples.findFile("car.mp4"))   #DESCOMENTAR LINEAS DE ABAJO
#cap = cv.VideoCapture(0)

#for i in range(250):            #DESCOMENTAR PARA EL VIDEO CAR
    # frame = cap.read()         #(tiene un titulo al principio)

lower_thr, upper_thr = [],[]

if prm.COLOR_ALGORITHM is True:
    prev, prev_gray, x, y, w, h, lower_thr, upper_thr = util.captureROI(cap)    #Se captura por primera vez la seleccion del usuario
else:
    prev, prev_gray, x, y, w, h= util.captureROI(cap)
prev = util.space_translate(x, y, prev)                 #Se aplica la trasformacion de las coordenadas de las features del espacio
                                                            #de la seleccion al espacio del frame.
frame_num = 0
error = False
dyn_h = h
dyn_w = w
frame = 0
while cap.isOpened():

    frame_num += 1
    ret, frame_real = cap.read()    #Se lee un frame

    if prm.COLOR_ALGORITHM is True: #Si el filtro de color esta encendido, se calcula la mascara para el frame actual
        frame = frame_real
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, lower_thr, upper_thr)
        frame = cv.bitwise_and(frame, frame, mask=mask)

    if frame_num != 0 and frame_num%prm.RECALC_EVERY_FRAMES == 0 and not error: #Se recalculan cada X frames las features de Shi-Tomasi
        frame_num = 0                                                                #Siempre y cuando se pueda encontrar al objeto
        prev, x, y = util.recalculateFeatures(prev, prev_gray, h, w)

    if error:
        error, prev, new_dyn_h, new_dyn_w =  util.searchObject(kalman, dyn_h, dyn_w, h, w, frame)        #Si no se puede encontrar
        dyn_h, dyn_w = new_dyn_h, new_dyn_w                                                        #al objeto, se realiza una busqueda por cada frame

    if prm.COLOR_ALGORITHM is True:
        error, good_new, good_old, prev_gray, prev= util.measureFeatures(error, frame, prev, prev_gray, kalman)    #Se mide la posicion del objeto
    else:                                                                                                           #recalculando el algoritmo de lucas-kanade
        error, good_new, good_old, prev_gray, prev = util.measureFeatures(error, frame_real, prev, prev_gray, kalman)

    util.drawEstimate(error, good_new, good_old, frame_real, kalman, dyn_h, dyn_w, h, w, frame)     #Se dibuja en la pantalla la estimacion de la ubicacion del objeto

    if cv.waitKey(10) & 0xFF == ord('q'):   #Con la letra Q se cierra
        break
    if cv.waitKey(10) & 0xFF == ord('p'):   #Con la letra P se pausea
        while True:
            if cv.waitKey(10) & 0xFF == ord('p'):
                break
    if  cv.waitKey(10) & 0xFF == ord('r'):#Con la letra R se reselecciona el area
        if prm.COLOR_ALGORITHM is True:
            prev, prev_gray, x, y, w, h, lower_thr, upper_thr = util.captureROI(cap)
        else:
            prev, prev_gray, x, y, w, h = util.captureROI(cap)
        prev = util.space_translate(x, y, prev)
        error = False
        dyn_w = w
        dyn_h = h

cap.release()
cv.destroyAllWindows()
