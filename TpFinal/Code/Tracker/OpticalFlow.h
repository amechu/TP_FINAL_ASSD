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
	void updateFeatures(cv::Mat& prevFilteredFrame, cv::Mat& filteredFrame, array<vector<cv::Point2f>, 2>& features, vector<uchar>& status, vector<float>& error, Size& winSize, TermCriteria termcrit);
	vector<uchar>& getStatus();
	Size& getSize();
	TermCriteria& getCriteria();
	vector<float> getError();

private:
	vector<double> parameters;
	vector<uchar> status;
	vector<float> err;
	bool trackingError;
	TermCriteria termcrit;
	Size winSize;
};

