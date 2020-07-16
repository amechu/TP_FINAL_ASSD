#include "ShiTomasi.h"

vector<cv::Point_<double>>& ShiTomasi::getFeatures() {
	return this->features;
}


vector<cv::Point_<double>>& ShiTomasi::recalculateFeatures() {
	return this->features;//(THIS ARE NOT THE NEW FEATURES)
	//TO DO
}