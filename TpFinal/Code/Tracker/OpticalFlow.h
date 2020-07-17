#pragma once
#include "../cvinclude.h"
#include "../Util/Util.h"
#include <vector>
using namespace std;
using namespace cv;
class OpticalFlow
{
public:
	OpticalFlow();
	void updateFeatures(array<vector<cv::Point2f>, 2>& features, cv::Mat& filteredFrame, cv::Mat& prevFilteredFrame);
private:
	vector<double> parameters;
	vector<uchar> status;
	vector<float> err;
	bool trackingError;
	TermCriteria termcrit;
	Size winSize;
};

