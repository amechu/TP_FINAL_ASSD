#pragma once
#include <array>
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

	void updateLightnessSemiAmplitude(double lSemiAmplitude_);
	void updateASemiAmplitude(double aSemiAmplitude_);
	void updateBSemiAmplitude(double bSemiAmplitude_);

private:
	double lSemiAmplitude;
	double aSemiAmplitude;
	double bSemiAmplitude;

	double lColor;
	double aColor;
	double bColor;
	
	bool done = false;
	cv::Mat filteredFrame;
	
};

