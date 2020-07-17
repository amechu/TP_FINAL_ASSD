#include "OpticalFlow.h"
#include "../Util/Util.h"
using namespace cv;
void OpticalFlow::updateFeatures(cv::Mat& prevFilteredFrame, cv::Mat& filteredFrame,array<vector<cv::Point2f>, 2>& features, vector<uchar>& status, vector<float>& error, Size& winSize, TermCriteria termcrit) {
	calcOpticalFlowPyrLK(prevFilteredFrame, filteredFrame, features[0], features[1], status, error, winSize,LK_MAX_LEVEL, termcrit, 0, LK_MIN_EIG_VALUE );
}

OpticalFlow::OpticalFlow() {
	this->termcrit = TermCriteria(TermCriteria::COUNT | TermCriteria::EPS, 20, 0.03);
	this->winSize = Size(LK_WIN_SIZE, LK_WIN_SIZE);

}
vector<uchar>& OpticalFlow::getStatus() {
	return this->status;
}
Size& OpticalFlow::getSize() {
	return this->winSize;
}


TermCriteria& OpticalFlow::getCriteria() {
	return this->termcrit;
}


vector<float> OpticalFlow::getError() {
	return this->err;
}