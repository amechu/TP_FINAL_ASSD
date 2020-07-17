//RECORDAR PONER EL ENVIRONMENT EN X64
#define CVUI_IMPLEMENTATION
#include "cvinclude.h"
#include "Code/FrontEndRelated/cvui.h"
#include "./Code/OldStuff/motionDetectionOld.h"
#include "Code/Tracker/Tracker.h"
<<<<<<< HEAD
//	//capture_test();
//}
>>>>>>> a6bc61cbe377329ac7668242abe3e63191e4f034

#define WINDOW1_NAME "Window 1"
using namespace cv;

int main() {
    //cvui::init(WINDOW1_NAME);
    cv::Mat frame2 = cv::Mat(cv::Size(400, 200), CV_8UC3);
    cv::Mat frame;

    double value = 12.4;
    
<<<<<<< HEAD
    //namedWindow("Original", WINDOW_AUTOSIZE);
=======
    namedWindow("Original", WINDOW_AUTOSIZE);
    //lucasKandale();//Mierda con la que prob� shi tomasi y lucas kanade
>>>>>>> a6bc61cbe377329ac7668242abe3e63191e4f034

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

    Tracker tracker = Tracker(frame, frame2);
    tracker.colorFilter->updateA(50);
    tracker.colorFilter->updateB(50);
    tracker.colorFilter->updateLightness(100);
    Mat res;
    while (true) {
<<<<<<< HEAD
                
=======
        frame2 = cv::Scalar(49, 52, 49);
        cvui::trackbar(frame2, 40, 30, 220, &value, (double)10.0, (double)15.0);




        cvui::imshow(WINDOW1_NAME, frame2);
        std::cout << value << std::endl;
        
        
>>>>>>> a6bc61cbe377329ac7668242abe3e63191e4f034
        captRefrnc >> frame;
        tracker.colorFilter->filterFrame(frame).copyTo(frame);
        
        imshow("Original", frame);
        if (cv::waitKey(20) == 27) {
            break;
        }
    }
    return 0;
}