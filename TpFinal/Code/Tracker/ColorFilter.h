#pragma once
#include "../cvinclude.h"
class ColorFilter
{
public:
	ColorFilter();//Todavia no sabemos que poner en el constructor brodanas
	cv::Mat& filterFrame(cv::Mat frame);
	cv::Mat& getFilteredFrame();

	void updateLightness(double lightness);
	void updateA(double a_);
	void updateB(double b_);

	void updateLightnessThreshold(double lThreshold_);
	void updateAThreshold(double aThreshold_);
	void updateBThreshold(double bThreshold_);

private:
	double lThreshold;
	double aThreshold;
	double bThreshold;

	double lColor;
	double aColor;
	double bColor;
	cv::Mat filteredFrame;
};

