#include "Tracker.h"


Tracker::Tracker(cv::Mat &  actualFrame_, cv::Mat & prevFrame_) :actualFrame(actualFrame_), prevFrame(prevFrame_) {
	//Kalman filter init
    this->kalmanFilter = new cv::KalmanFilter(4, 2); //4 Variables de estado, dos de medición.
    this->kalmanFilter->transitionMatrix = (cv::Mat_<double>(4, 4) << 1, 0, this->kalmanDelta, 0,
                                                                     0, 1, 0, this->kalmanDelta,
                                                                     0, 0, 1, 0,
                                                                     0, 0, 0, 1);
    cv::setIdentity(this->kalmanFilter->measurementMatrix);
    cv::setIdentity(this->kalmanFilter->processNoiseCov, cv::Scalar::all(this->processNoiseCovariance));
    cv::setIdentity(this->kalmanFilter->measurementNoiseCov, cv::Scalar::all(this->measurementNoiseCovariance));
    cv::setIdentity(this->kalmanFilter->errorCovPost, cv::Scalar::all(1));
    this->kalmanFilter->statePost = 0;
}

cv::Point_<double> Tracker::getEstimate() {
    return cv::Point_<double>(this->kalmanFilter->statePost.at<double>(0, 0), this->kalmanFilter->statePost.at<double>(0, 1));
}

cv::Point_<double> Tracker::getEstimatedVelocity() {
    return cv::Point_<double>(this->kalmanFilter->statePost.at<double>(0, 2), this->kalmanFilter->statePost.at<double>(0, 3));
}

vector<cv::Point_<double>>& Tracker::getFeatures() {
    return this->shiTomasi->getFeatures();
}

void Tracker::Update() {

}

cv::Mat& Tracker::getFilteredFrame() {
    return this->colorFilter->getFilteredFrame();
}

cv::Mat& Tracker::filterFrame(cv::Mat frame) {
    return this->colorFilter->filterFrame(frame);
}

double Tracker::calculateNewColor() {

}

double Tracker::calculateNewLightness() {

}
