#pragma once
#include "../cvinclude.h"
#include <vector>
#include <array>
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
	array<vector<cv::Point2f>, 2>& getFeatures();
	cv::Mat& getFilteredFrame();
	cv::Mat& filterFrame(cv::Mat frame);

	ColorFilter* colorFilter;//DEBUG cambiar a private
private:
	cv::Mat& actualFrame;
	cv::Mat& prevFrame;

	ShiTomasi* shiTomasi;
	cv::KalmanFilter* kalmanFilter;
	double kalmanDelta = 1.2;
	double processNoiseCovariance = 0.006;
	double measurementNoiseCovariance = 0.4;
	OpticalFlow* opticalFlow;
};

