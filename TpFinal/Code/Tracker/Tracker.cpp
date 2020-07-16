#include "Tracker.h"


Tracker::Tracker(cv::Mat &  actualFrame_, cv::Mat & prevFrame_) :actualFrame(actualFrame_), prevFrame(prevFrame_) {
}

Point Tracker::getEstimate() {

}

Point& Tracker::getEstimatedVelocity() {

}

vector<Point>& Tracker::getFeatures() {

}

void Tracker::Update() {

}

cv::Mat& Tracker::getFilteredMask() {

}

double Tracker::calculateNewColor() {

}

double Tracker::calculateNewLightness() {

}
