#include "OpticalFlow.h"
#include "../Util/Util.h"
using namespace cv;
void OpticalFlow::updateFeatures(array<vector<cv::Point2f>, 2>& features, cv::Mat& filteredFrame, cv::Mat& prevFilteredFrame) {
	calcOpticalFlowPyrLK(prevFilteredFrame, filteredFrame, features[0], features[1], this->status, this->err, this->winSize
		,LK_MAX_LEVEL, this->termcrit, 0, LK_MIN_EIG_VALUE );
}

OpticalFlow::OpticalFlow() {
	this->termcrit = TermCriteria(TermCriteria::COUNT | TermCriteria::EPS, 20, 0.03);
	this->winSize = Size(LK_WIN_SIZE, LK_WIN_SIZE);

}