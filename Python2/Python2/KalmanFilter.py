
import cv2 as cv
import numpy as np

class KalmanFilter:
    dt = 1.2  # delta time para modelo fisico
    INITIAL_STATE_COV = 1
    PROCESS_COV = 0.0006  # process covariance, si es chico entonces la estimacion tiene menos ruido pero es menos precisa, si es grande la estimacion tiene mas ruido pero es mas precisa
    MEAS_NOISE_COV = 0.6  # covarianza de medicion, por ahora fija

    def __init__(self):
        self.kalman = cv.KalmanFilter(4, 2, 0)  #Se inicializa el filtro kalman con 4 variables de estado y 2 variables de medicion

        self.kalman.transitionMatrix = np.array([[1.,    0.,    self.dt, 0.    ],
                                                                      [0.,    1.,    0.,     self.dt],
                                                                      [0.,    0.,    1.,     0.    ],
                                                                      [0.,    0.,    0.,     1.    ]])  # Matriz A

        self.kalman.measurementMatrix = np.array([[1., 0., 0., 0.],
                                                  [0., 1., 0., 0.]])  # Matriz H, donde se dice que solo se mide la posicion y no la velocidad

        self.kalman.processNoiseCov = self.PROCESS_COV * np.identity(4)  # Matriz Q

        self.kalman.measurementNoiseCov = self.MEAS_NOISE_COV * np.identity(2)  # Matriz R

        self.kalman.errorCovPost = np.identity(4) * self.INITIAL_STATE_COV  # Matriz de covarianza inicial

        self.kalman.statePost = np.array([0., 0., 0., 0.]).reshape(4, 1)  # Matriz de estado inicial

        self.trajectory = []


    def predict(self):
        self.kalman.predict()

    def correct(self, measured_x, measured_y):
        self.trajectory.append((int(measured_x), int(measured_y)))
        self.kalman.correct((float(measured_x), float(measured_y)))

    def setStatePost(self, statePost_):
        self.kalman.statePost = statePost_

    def updateParams(self):
        self.kalman.processNoiseCov = self.PROCESS_COV * np.identity(4)  # Matriz Q

        self.kalman.measurementNoiseCov = self.MEAS_NOISE_COV * np.identity(2)  # Matriz R

        self.kalman.transitionMatrix = np.array([[1., 0., self.dt, 0.],
                                                 [0., 1., 0., self.dt],
                                                 [0., 0., 1., 0.],
                                                 [0., 0., 0., 1.]])  # Matriz A




    @property
    def statePost(self):
        return self.kalman.statePost
    
    @property
    def errorCovPost(self):
        return self.kalman.errorCovPost