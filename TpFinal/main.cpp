#include "cvinclude.h"
#include "Code/FrontEndRelated/cvui.h"
#include "Code/Tracker/Tracker.h"

using namespace std;
int main(void) {
	cv::Mat frame2 = cv::Mat(cv::Size(400, 200), CV_8UC3);
	cv::Mat& hay = frame2;
	Tracker tracker = Tracker(hay,hay);	
	tracker.kalmanFilter->predict();
	cout << "hola" << endl;
}