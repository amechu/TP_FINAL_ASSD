//RECORDAR PONER EL ENVIRONMENT EN X64
#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW1_NAME "Window 1"
using namespace cv;

int main() {
    cvui::init(WINDOW1_NAME);
    cv::Mat frame2 = cv::Mat(cv::Size(400, 200), CV_8UC3);
    cv::Mat frame;
    double value = 12.4;

    namedWindow("Original", WINDOW_AUTOSIZE);

}