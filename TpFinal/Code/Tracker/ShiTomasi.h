#pragma once
#include "../cvinclude.h"
#include "../Util/Util.h"
#include <vector>
using namespace std;
class ShiTomasi
{
public:
	vector<cv::Point_<double>>& getFeatures();
	vector<cv::Point_<double>>& recalculateFeatures(cv::Mat & prevGray);
private:
	vector<cv::Point_<double>> features;
	vector<double> parameters;
};

