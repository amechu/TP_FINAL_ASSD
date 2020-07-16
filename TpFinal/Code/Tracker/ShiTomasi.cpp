#include "ShiTomasi.h"

vector<cv::Point_<double>>& ShiTomasi::getFeatures() {
	return this->features;
}


vector<cv::Point_<double>>& ShiTomasi::recalculateFeatures(cv::Mat& prevGray) {
	goodFeaturesToTrack(gray, points[1], MAX_COUNT, 0.01, 10, cv::Mat(), 3, 3, 0, 0.04);

	return this->features;//(THIS ARE NOT THE NEW FEATURES)
	//TO DO
}