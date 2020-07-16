#pragma once
#include "../cvinclude.h"
class ColorFilter
{
public:
	ColorFilter();//Todavia no sabemos que poner en el constructor brodanas
	cv::Mat& FilteredFrame(cv::Mat frame);
	void updateHue(double hue);
	void updateLightness(double lightness);
	void updateSaturation(double saturation);

	void updateHueThreshold(double hThreshold_);
	void updateLightnessThreshold(double lThreshold_);
	void updateSaturationThreshold(double sThreshold_);

private:
	double hThreshold;
	double sThreshold;
	double lThreshold;

	double hColor;
	double sColor;
	double lColor;
	cv::Mat filteredFrame;
};

