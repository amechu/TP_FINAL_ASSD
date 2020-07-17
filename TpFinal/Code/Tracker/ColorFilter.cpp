#include "ColorFilter.h"
#include "../Util/Util.h"
ColorFilter::ColorFilter() {
	this->lSemiAmplitude = L_THRESHOLD_DEFAULT;
	this->aSemiAmplitude = A_THRESHOLD_DEFAULT;
	this->bSemiAmplitude = B_THRESHOLD_DEFAULT;
	this->lColor = 0;
	this->aColor = 0;
	this->bColor = 0;
	//Falta
}
cv::Mat& ColorFilter::filterFrame(cv::Mat frame) {
	cv::Mat mask(frame.rows,frame.cols, frame.type(), cv::Scalar(0));
	cv::Mat frameLab;

	/*std::array<int, 3> lowerThreshold = { this->lColor - this->lSemiAmplitude, this->aColor - this->aSemiAmplitude, this->bColor - this->bSemiAmplitude };
	std::array<int, 3> upperThreshold = { this->lColor + this->lSemiAmplitude, this->aColor + this->aSemiAmplitude, this->bColor + this->bSemiAmplitude };*/

	//cv::Scalar lowerThreshold(this->lColor - this->lSemiAmplitude, this->aColor - this->aSemiAmplitude, this->bColor - this->bSemiAmplitude);
	//cv::Scalar upperThreshold(this->lColor + this->lSemiAmplitude, this->aColor + this->aSemiAmplitude, this->bColor + this->bSemiAmplitude);


	cv::Scalar lowerThreshold(110, 50, 50);
	cv::Scalar upperThreshold(130, 255, 255);

	//cv::cvtColor(frame, frameLab, cv::COLOR_BGR2Lab); //Alan
	cv::cvtColor(frame, frameLab, cv::COLOR_BGR2HSV);

	cv::inRange(frameLab, lowerThreshold, upperThreshold, mask);
	//cv::bitwise_and(frame, frame, this->filteredFrame, mask); //Alan

	// ¡¡¡NO TOCAR!!!
	cv::Mat temp;
	cv::copyTo(frame, temp, mask);
	this->filteredFrame = temp.clone();
	return this->filteredFrame;
}

cv::Mat& ColorFilter::getFilteredFrame() {
	return this->filteredFrame;
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

void ColorFilter::updateLightnessSemiAmplitude(double lSemiAmplitude_) {
	this->lSemiAmplitude = lSemiAmplitude_;
}

void ColorFilter::updateASemiAmplitude(double aSemiAmplitude_) {
	this->aSemiAmplitude = aSemiAmplitude_;
}

void ColorFilter::updateBSemiAmplitude(double bSemiAmplitude_) {
	this->bSemiAmplitude = bSemiAmplitude_;
}
