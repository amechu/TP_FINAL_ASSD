#include "ShiTomasi.h"
#include "../Util/Util.h"
using namespace cv;

array<vector<cv::Point2f>, 2>& ShiTomasi::getFeatures() {
	return this->features;
}



array<vector<cv::Point2f>, 2>& ShiTomasi::recalculateFeatures(cv::Mat& prevGray) {
	goodFeaturesToTrack(prevGray, this->features[1], this->maxCorners, this->qualityLevel, this->minDistance, cv::Mat(),ST_BLOCK_SIZE, ST_GRADIENT_SIZE, false, ST_K);
	return this->features;
}

void ShiTomasi::setMaxCorners(int mc) {
	this->maxCorners = mc;
}
void ShiTomasi::setMinDistance(double md) {
	this->minDistance = md;
}
void ShiTomasi::setQualityLevel(double ql) {
	this->qualityLevel = ql;
}