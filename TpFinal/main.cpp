#include "cvinclude.h"
#include "Code/FrontEndRelated/cvui.h"
#include "Code/Tracker/Tracker.h"

using namespace std;
int main(void) {
	cv::Mat hola = cv::Mat(1, 1, 1);
	cv::Mat& hay = hola;
	Tracker tracker = Tracker(hay,hay);

}