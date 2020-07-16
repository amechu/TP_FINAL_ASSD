//RECORDAR PONER EL ENVIRONMENT EN X64
#define CVUI_IMPLEMENTATION
#include "../FrontEndRelated/cvui.h"
#include "motionDetectionOld.h"
//#include "lucasKandaleOld.h"
//#include "playGroundOld.h"
//int main(void) {	
//	motionDetection();
//	//lucasKandale();
//	//capture_test();
//}

#define WINDOW1_NAME "Window 1"
using namespace cv;

int main() {
    cvui::init(WINDOW1_NAME);
    cv::Mat frame2 = cv::Mat(cv::Size(400, 200), CV_8UC3);
    cv::Mat frame;
    double value = 12.4;
    
    namedWindow("Original", WINDOW_AUTOSIZE);

    VideoCapture captRefrnc(CAP_DSHOW);
    // Check if external camera opened successfully, otherwise use internal camera
    if (!captRefrnc.isOpened()) {
        VideoCapture captRefrnc(0);
        // Check if camera opened successfully
        if (!captRefrnc.isOpened()) {
            std::cout << "Error opening video stream or file" << std::endl;
            return -1;
        }

    }


    while (true) {
        frame2 = cv::Scalar(49, 52, 49);
        cvui::trackbar(frame2, 40, 30, 220, &value, (double)10.0, (double)15.0);

        cvui::imshow(WINDOW1_NAME, frame2);
        std::cout << value << std::endl;
        
        
        captRefrnc >> frame;
        cvui::text(frame, 50, 50, std::to_string(value),2,0xFF0000);

        imshow("Original", frame);
        if (cv::waitKey(20) == 27) {
            break;
        }

    }
    return 0;
}