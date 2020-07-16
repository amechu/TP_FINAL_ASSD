#include "ColorFilter.h"
#include "../Util/Util.h"
ColorFilter::ColorFilter() {
	this->hThreshold = H_THRESHOLD;
	this->lThreshold = L_THRESHOLD;
	this->sThreshold = S_THRESHOLD;
	//Falta
}
cv::Mat& ColorFilter::FilteredFrame(cv::Mat frame) {
//FALTA
}


void ColorFilter::updateHue(double hue) {
	this->hColor = hue;
}
void ColorFilter::updateLightness(double lightness) {
	this->lColor = lightness;
}
void ColorFilter::updateSaturation(double saturation) {
	this->sColor = saturation;
}

void ColorFilter::updateHueThreshold(double hThreshold_) {
	this->hThreshold = hThreshold_;
}
void ColorFilter::updateLightnessThreshold(double lThreshold_) {
	this->lThreshold = lThreshold_;
}
void ColorFilter::updateSaturationThreshold(double sThreshold_) {
	this->sThreshold = sThreshold_;
}
