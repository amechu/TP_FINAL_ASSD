""""""

import cv2 as cv

"""SHI-TOMASI ALGORITHM"""

feature_params = dict(maxCorners=1000,    #Maxima cantidad de features
                      qualityLevel=0.1,   #Nivel de calidad minimo de cada feature entre 0 y 1. En 0 se devuelven TODAS las features no importa la calidad
                      minDistance=0.1,    #Minima distancia entre features
                      blockSize=7)
RECALC_EVERY_FRAMES = 15
"""####################"""
"""LUCAS-KANADE ALGORITHM"""

lk_params = dict(winSize=(15, 15),
                 maxLevel=4,              #Niveles del arbol maximos
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT,
                10,
                0.03))

"""####################"""
"""KALMAN FILTER ALGORITHM"""

dt = 1                  #delta time para modelo fisico
INITIAL_STATE_COV = 1
PROCESS_COV = 0.0006      #process covariance, si es chico entonces la estimacion tiene menos ruido pero es menos precisa, si es grande la estimacion tiene mas ruido pero es mas precisa
MEAS_NOISE_COV = 0.4       #covarianza de medicion, por ahora fija

"""####################"""

ft_color = (0, 255, 0)      #Color de las features
ROI_color = (255, 0, 0)     #Color de la seleccion
kalman_color = (0, 130, 255)#Color de la estimacion de kalman

"""####################"""
HUE_VAR = 8             #Threshold de hue para filtro de color
SAT_VAR = 40            #Threshold de saturacion para filtro de color
VAL_VAR = 40            #Threshold de value para filtro de color

COLOR_ALGORITHM = True     #Activa o no el uso del algoritmo de filtrado de color
DEBUG_MODE = True           #Activa o no la segunda pantalla de debug, puede hacer mas lento al programa
SHOW_FEATURES = True         #Activa o no el mostrar los features cuando debug_mode=true

font = cv.FONT_HERSHEY_SIMPLEX

SEARCHING_ENLARGEMENT = 4   #Rapidez con la que se agranda el area de busqueda