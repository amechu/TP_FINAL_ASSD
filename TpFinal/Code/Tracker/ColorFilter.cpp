#include "ColorFilter.h"
#include "../Util/Util.h"
ColorFilter::ColorFilter() {
	this->lThreshold = L_THRESHOLD_DEFAULT;
	this->aThreshold = A_THRESHOLD_DEFAULT;
	this->bThreshold = B_THRESHOLD_DEFAULT;
	//Falta
}
cv::Mat& ColorFilter::FilteredFrame(cv::Mat frame) {
//FALTA
}

void ColorFilter::updateLightness(double lightness) {
	this->lColor = lightness;
}

void ColorFilter::updateA(double a_) {
	this->aColor = a_;
}
void ColorFilter::updateB(double b_) {
	this->bColor = b_;
}

void ColorFilter::updateLightnessThreshold(double lThreshold_) {
	this->lThreshold = lThreshold_;
}

void ColorFilter::updateAThreshold(double aThreshold_) {
	this->aThreshold = aThreshold_;
}

void ColorFilter::updateBThreshold(double bThreshold_) {
	this->bThreshold = bThreshold_;
}
