#pragma once
#include "../cvinclude.h"
#include <vector>
#include "../Util/Util.h"
#include "ColorFilter.h"
#include "OpticalFlow.h"
#include "ShiTomasi.h"

using namespace std;
class Tracker
{
public:
	Tracker(cv::Mat & actualFrame_, cv::Mat & prevFrame_);
	void Update();
	cv::Point2f getEstimate();
	////Debug Functions
	cv::Point2f getEstimatedVelocity();
	vector<cv::Point2f>& getFeatures();
	cv::Mat& getFilteredFrame();
	cv::Mat& filterFrame(cv::Mat frame);

	cv::KalmanFilter* kalmanFilter;
private:
	double calculateNewColor();
	double calculateNewLightness();
	cv::Mat& actualFrame;
	cv::Mat& prevFrame;
	ColorFilter * colorFilter;
	ShiTomasi* shiTomasi;

	double kalmanDelta = 1.2;
	double processNoiseCovariance = 0.006;
	double measurementNoiseCovariance = 0.4;
	OpticalFlow* opticalFlow;
};

