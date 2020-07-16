import params as prm
import cv2 as cv
import numpy as np

class KalmanFilter:

    def __init__(self):
        self.kalman = cv.KalmanFilter(4, 2, 0)  #Se inicializa el filtro kalman con 4 variables de estado y 2 variables de medicion

        self.kalman.transitionMatrix = np.array([[1.,    0.,    prm.dt, 0.    ],
                                                                      [0.,    1.,    0.,     prm.dt],
                                                                      [0.,    0.,    1.,     0.    ],
                                                                      [0.,    0.,    0.,     1.    ]])  # Matriz A

        self.kalman.measurementMatrix = np.array([[1., 0., 0., 0.],
                                                  [0., 1., 0., 0.]])  # Matriz H, donde se dice que solo se mide la posicion y no la velocidad

        self.kalman.processNoiseCov = prm.PROCESS_COV * np.identity(4)  # Matriz Q

        self.kalman.measurementNoiseCov = prm.MEAS_NOISE_COV * np.identity(2)  # Matriz R

        self.kalman.errorCovPost = np.identity(4) * prm.INITIAL_STATE_COV  # Matriz de covarianza inicial

        self.kalman.statePost = np.array([0., 0., 0., 0.]).reshape(4, 1)  # Matriz de estado inicial



    def predict(self):
        self.kalman.predict()

    def correct(self, measured_x, measured_y):
        self.kalman.correct((measured_x, measured_y))

    @property
    def statePost(self):
        return self.kalman.statePost
    
    @property
    def errorCovPost(self):
        return self.kalman.errorCovPost