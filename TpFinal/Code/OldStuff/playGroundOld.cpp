#include "playGroundOld.h"

using namespace cv;
using namespace std;

int  capture_test(void) {

	VideoCapture captRefrnc(CAP_DSHOW);
	// Check if external camera opened successfully, otherwise use internal camera
	if (!captRefrnc.isOpened()) {
		VideoCapture captRefrnc(0);
		// Check if camera opened successfully
		if (!captRefrnc.isOpened()) {
			cout << "Error opening video stream or file" << endl;
			return -1;
		}

	}


	namedWindow("Original", WINDOW_AUTOSIZE);
	namedWindow("GRAY", WINDOW_AUTOSIZE);
	namedWindow("Blured", WINDOW_AUTOSIZE);
	namedWindow("DownSampled", WINDOW_AUTOSIZE);

	Mat frame;
	Mat gray;
	Mat blured;
	Mat downSampled;
	while (1) {

		//Code goes here
		//Get frame from camera
		captRefrnc >> frame;
		if (frame.empty())
			break;
		//Change to grayscale
		imshow("Original", frame);

		//cvtColor(frame, gray, COLOR_BGR2GRAY);
		//imshow("GRAY", gray);

		//GaussianBlur(frame, blured, Size(5, 5), 3, 3);
		//imshow("Blured", blured);

		//Downsampling halves the original image, interersting for optimization porpouses
		pyrDown(frame, downSampled);
		imshow("DownSampled", downSampled);

		char c = (char)waitKey(25);
		if (c == 27)
			break;
	}

	// When everything done, release the video capture object
	captRefrnc.release();

	// Closes all the frames
	destroyAllWindows();

	return 0;
}