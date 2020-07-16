#pragma once
#include "../cvinclude.h"
#include "../Util/Util.h"
#include <vector>
using namespace std;
class OpticalFlow
{
public:
	void updateFeatures(vector<Point>& features, cv::Mat& filteredFrame, cv::Mat& prevFilteredFrame);
private:
	vector<double> parameters;
	bool trackingError;
};

