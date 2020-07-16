#include "motionDetection.h"

using namespace cv;
using namespace std;

int motionDetection(void) {

    namedWindow("Original", WINDOW_AUTOSIZE);
    namedWindow("Difference", WINDOW_AUTOSIZE);

    VideoCapture captRefrnc("gido.mp4")               ;//CAP_DSHOW);
    // Check if external camera opened successfully, otherwise use internal camera
    if (!captRefrnc.isOpened()) {
        VideoCapture captRefrnc(0);
        // Check if camera opened successfully
        if (!captRefrnc.isOpened()) {
            cout << "Error opening video stream or file" << endl;
            return -1;
        }

    }
    Mat frame;
    Mat frame_gray;
    Mat prev_gray;
    Mat diff;
    int counter = 0;

    captRefrnc >> frame;
    //Just for the first time
    cvtColor(frame, prev_gray, COLOR_BGR2GRAY);


    while (1) {
        //Code goes here
        //Get frame from camera

        if (frame.empty())
            break;



        //Exit when Esc key is pressed
        char c = (char)waitKey(25);
        if (c == 27)
            break;

        cvtColor(frame, frame_gray, COLOR_BGR2GRAY);
        //cvtColor(prev, prev_gray, COLOR_BGR2GRAY);

        subtract(frame_gray, prev_gray, diff);
        imshow("Original", frame);
        imshow("Difference", diff);
        prev_gray = frame_gray.clone();

        captRefrnc >> frame;
    }
}