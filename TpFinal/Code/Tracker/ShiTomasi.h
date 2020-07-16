#pragma once
#include "../cvinclude.h"
#include "../Util/Util.h"
#include <vector>
#include <array>
using namespace std;
class ShiTomasi
{
public:
	array<vector<cv::Point2f>, 2>&  getFeatures();
	array<vector<cv::Point2f>, 2>& recalculateFeatures(cv::Mat & prevGray);
	void setMaxCorners(int mc);
	void setMinDistance(double md);
	void setQualityLevel(double ql);
private:
	array<vector<cv::Point2f>,2>  features;
	vector<double> parameters;
	double qualityLevel = ST_QUALITY_LEVEL_DEFAULT;
	int maxCorners = MAX_CORNERS_DEFAULT;
	double minDistance = ST_MIN_DISTANCE_DEFAULT;
};

