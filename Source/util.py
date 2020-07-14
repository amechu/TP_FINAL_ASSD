import cv2 as cv
import params as prm
import numpy as np

#captureROI
#Recibe: el dispositivo de captura
#Devuelve: las cordenadas de las features referidas al (0,0) de la seleccion, el frame actual en escala de grises
#y la posicion, ancho y altura de la seleccion del usuario
def captureROI(capture_device):

    prev = None
    x, y, w, h, = 0, 0, 0, 0
    prev_gray = [[[]]]
    while prev is None:

        capture_device.read()
        ret, frame = capture_device.read()
        bbox = cv.selectROI("Grupo 3 Visual Tracker", frame, False)
        x = bbox[0]
        y = bbox[1]
        w = bbox[2]
        h = bbox[3]

        if prm.COLOR_ALGORITHM is True:                         #Este if realiza el filtrado de color previo a obtener las features
            selection = np.asarray(frame[y:y + h, x:x + w])
            b, g, r = [], [], []

            yy, xx, col = np.shape(selection)
            for i in range(yy):
                for j in range(xx):
                    b.append(selection[i, j, 0])
                    g.append(selection[i, j, 1])
                    r.append(selection[i, j, 2])
            median_b, median_g, median_r = np.median(b), np.median(g), np.median(r)

            bgr_mask = np.uint8([[[median_b, median_g, median_r]]])
            hsv_mask = cv.cvtColor(bgr_mask, cv.COLOR_BGR2HSV)

            lower_thr = np.array([np.int32(hsv_mask[0, 0, :])[0] - prm.HUE_VAR, np.int32(hsv_mask[0, 0, :])[1] - prm.SAT_VAR, np.int32(hsv_mask[0, 0, :])[2] - prm.VAL_VAR])
            upper_thr = np.array([np.int32(hsv_mask[0, 0, :])[0] + prm.HUE_VAR, np.int32(hsv_mask[0, 0, :])[1] + prm.SAT_VAR, np.int32(hsv_mask[0, 0, :])[2] + prm.VAL_VAR])

            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, lower_thr, upper_thr)
            frame = cv.bitwise_and(frame, frame, mask=mask)

            prev_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            prev = cv.goodFeaturesToTrack(prev_gray[y:y+h, x:x+w], mask=None, **prm.feature_params)     #Se aplica el algoritmo de shi-tomasi

            return prev, prev_gray, x, y, w, h, lower_thr, upper_thr

        prev_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        prev = cv.goodFeaturesToTrack(prev_gray[y:y + h, x:x + w], mask=None, **prm.feature_params)

    return prev, prev_gray, x, y, w, h

#space_translate
#Recibe: posicion en x e y de la seleccion del usuario y posicion de las features referidas a la seleccion
#Devuelve: la posicion de las features referidas al frame original
def space_translate(x, y, prev):
    if prev is None:
        return None
    for i in range(prev.shape[0]):
            prev[i][0][0] = prev[i][0][0] + x
            prev[i][0][1] = prev[i][0][1] + y
    return prev

#calculate_means_and_std
#Recibe: las features
#Devuelve: la media en x, y y la varianza
def calculate_means_and_std(prev):

    prev_x = []
    prev_y = []

    for i in range(prev.shape[0]):
        prev_x.append(prev[i][0][0])
        prev_y.append(prev[i][0][1])

    x_mean = np.mean(np.asarray(prev_x))
    y_mean = np.mean(np.asarray(prev_y))
    var = np.sqrt((np.std(np.asarray(prev_x))**2 + np.std(np.asarray(prev_y))**2))

    return x_mean, y_mean, var

#get_new_box_coordinates
#Recibe: las features, el ancho y altura de la seleccion original
#Devuelve: las nuevas coordenadas de la seleccion para realizar el recalculo de shi-tomasi
def get_new_box_coordinates(prev, h, w):

    SIGMA_INTERVAL = 1

    prev_x = []
    prev_y = []

    for i in range(prev.shape[0]):
        prev_x.append(prev[i][0][0])
        prev_y.append(prev[i][0][1])

    x_mean = np.mean(np.asarray(prev_x))        #Se calcula la media
    y_mean = np.mean(np.asarray(prev_y))

    x_std = np.std(np.asarray(prev_x))          #Se calcula la varianza
    y_std = np.std(np.asarray(prev_y))

    for i in range(len(prev_x)):
        if i >= len(prev_x):
            break
        if abs(prev_x[i] - x_mean) > SIGMA_INTERVAL * x_std:      #Se eliminan outliers segun la constante multiplicativa
            del prev_x[i]                                           #SIGMA_INTERVAL que multiplica la varianza

    for i in range(len(prev_y)):
        if i >= len(prev_y):
            break
        if abs(prev_y[i] - y_mean) > SIGMA_INTERVAL * y_std:
            del prev_y[i]

    x_mean = np.mean(np.asarray(prev_x))        #Se recalcula la media
    y_mean = np.mean(np.asarray(prev_y))

    x = int(x_mean - (w / 2))
    y = int(y_mean - (h / 2))

    return x, y           #Se devuelven las nuevas coordenadas de la seleccion

#recalculateFeatures
#Recibe: las features viejas, el frame actual en escala de grises, el ancho y altura de la seleccion donde calcular shi-tomasi
#Devuelve: las features nuevas y la posicion del area recalculada
def recalculateFeatures(prev, prev_gray, h, w):
    x, y = get_new_box_coordinates(prev, h, w)  # Se busca donde aplicar el algoritmo
    prev = cv.goodFeaturesToTrack(prev_gray[y:y + h, x:x + w], mask=None,
                                  **prm.feature_params)  # Se aplica el algoritmo de shi-tomasi
    prev = space_translate(x, y, prev)  # transformacion de seleccion a ventana

    return prev, x, y

#measureFeatures
#Recibe: bool de error de trackeo, frame actual, features actuales, frame en escala de grises y filtro kalman
#Devuelve: bool de error de trackeo, nuevos features, viejos features ambos en nparray, frame en escala de grises y features nuevas en tipo de dato original
def measureFeatures(error_feature, frame, prev, prev_gray, kalman):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    kalman.predict()

    if prev is None:
        error_feature = True

    if not error_feature:
        next_, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **prm.lk_params)    #Se utiliza el algoritmo de lucas kanade

        if np.any(status):                                  #Se verifica si se perdio al objeto
            error_feature = False
            good_old = prev[status == 1]
            good_new = next_[status == 1]
            (mux, muy, var) = calculate_means_and_std(next_)
            kalman.correct(float(mux), float(muy))          #Se entrega la medicion a kalman
            prev = good_new.reshape(-1, 1, 2)
        else:
            error_feature = True
            good_new = 0
            good_old = 0
            prev = 0
    else:
        error_feature = True
        good_new = 0
        good_old = 0
        prev = 0

    prev_gray = gray.copy()
    return error_feature, good_new, good_old, prev_gray, prev

#drawEstimate
#Recibe: bool de error de trackeo, nuevos features, viejos features ambos en nparray, frame actual, filtro de kalman
#anchos y alturas dinamicos de busqueda, anchos y alturas originales y frame tras filtro de color
def drawEstimate(error, good_new, good_old, frame, kalman, dyn_h, dyn_w, h, w,  frame_debug):
    if prm.COLOR_ALGORITHM is False:
        frame_debug =  frame.copy()
    if not error and prm.DEBUG_MODE is True:
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            if prm.SHOW_FEATURES is True:
                frame_debug = cv.circle(frame_debug, (int(a), int(b)), 3, prm.ft_color, -1)                                     #SE DIBUJAN LOS FEATURES
            cv.putText(frame_debug, "(x, y)=", (18, 60), prm.font, 0.6, (0, 240, 0), 1, cv.LINE_AA)
            cv.putText(frame_debug, np.str(int(kalman.statePost[0][0])), (93, 60), prm.font, 0.6, (0, 220, 0), 1, cv.LINE_AA)
            cv.putText(frame_debug, ', ', (128, 60), prm.font, 0.6, (0, 220, 0), 1, cv.LINE_AA)                                 #SE DIBUJAN LAS COORDENADAS DE LA ESTIMACION
            cv.putText(frame_debug, np.str(int(kalman.statePost[1][0])), (141, 60), prm.font, 0.6, (0, 220, 0), 1, cv.LINE_AA)
    else:
        x = np.int(kalman.statePost[0][0])
        y = np.int(kalman.statePost[1][0])
        if error is True:
            cv.putText(frame, 'Tracking failure', (15, 30), prm.font, 1, (0, 0, 255), 2, cv.LINE_AA)                            #SE INFORMA SI SE PERDIO AL OBJETO
        if prm.DEBUG_MODE is True:
            cv.rectangle(frame_debug, (int(x - (dyn_w/2)), int(y - (dyn_h/2))), (int(x + (dyn_w/2)), int(y + (dyn_h/2))), prm.ROI_color, 4)     #SE DIBUJA AREA DE BUSQUEDA

    if prm.DEBUG_MODE is True:
        if prm.COLOR_ALGORITHM is True:
            cv.putText(frame_debug, 'Color filter ON', (15, 30), prm.font, 0.75, (0, 255, 0), 1, cv.LINE_AA)        #SE INFORMA SI SE ESTA UTILIZANDO FILTRO DE COLOR
        else:
            cv.putText(frame_debug, 'Color filter OFF', (15, 30), prm.font, 0.75, (0, 0, 255), 1, cv.LINE_AA)

    frame = cv.circle(frame, (int(kalman.statePost[0][0]), int(kalman.statePost[1][0])), int(np.sqrt(w**2 + h**2)/2 + 5), prm.kalman_color, 2)      #SE DIBUJA LA ESTIMACION DE KALMAN
    output = cv.add(frame, 0)
    if prm.DEBUG_MODE is True:
        cv.imshow("Grupo 3 Visual Tracker -- DEBUG", frame_debug)
    cv.imshow("Grupo 3 Visual Tracker", output)

#seachObject
#Recibe: Filtro de kalman, anchos y alturas fijos y dinamicos, frame actual y bool de error de trackeo.
#Devuelve: bool de error de trackeo, features encontradas (si las hay), ancho y altura dinamica
def searchObject(kalman, dyn_h, dyn_w, h, w, frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    x = np.int(kalman.statePost[0][0])                          #Se toma como parametro la estimacion de kalman para posicionar el area de busqueda
    y = np.int(kalman.statePost[1][0])
    prev = cv.goodFeaturesToTrack(gray[int(y - (dyn_h/2)):int(y + (dyn_h/2)), int(x - (dyn_w/2)):int(x + (dyn_w/2))],**prm.feature_params)  #Se aplica el algoritmo de shi-tomasi
    if prev is not None:
        error = False
        prev = space_translate(x - (dyn_w/2), y - (dyn_h/2), prev)  #Si se encuentra, se actualiza posicion
        dyn_h, dyn_w = h, w
    else:
        error = True
        dyn_h += prm.SEARCHING_ENLARGEMENT*1.05             #Si no se encuentra se agranda area de busqueda
        dyn_w += prm.SEARCHING_ENLARGEMENT*1.05
    return error, prev, dyn_h, dyn_w