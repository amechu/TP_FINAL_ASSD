#pragma once
#include "../cvinclude.h"
#include <vector>
#include "../Util/Util.h"
#include "ColorFilter.h"
#include "KalmanFilter.h"
#include "OpticalFlow.h"
#include "ShiTomasi.h"

using namespace std;
class Tracker
{
public:
	Tracker(cv::Mat & actualFrame_, cv::Mat & prevFrame_);
	void Update();
	Point getEstimate();
	////Debug Functions
	Point& getEstimatedVelocity();
	vector<Point>& getFeatures();
	cv::Mat& getFilteredMask();

private:
	double calculateNewColor();
	double calculateNewLightness();
	cv::Mat& actualFrame;
	cv::Mat& prevFrame;
	ColorFilter * colorFilter;
	ShiTomasi* shiTomasi;
	KalmanFilter* kalmanFilter;
	OpticalFlow* opticalFlow;
};

