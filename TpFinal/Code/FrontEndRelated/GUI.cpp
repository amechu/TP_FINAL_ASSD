#include "Gui.h"

Gui::Gui() {
	
	this->frame = Mat(800, 1280, CV_8UC3);
	
	this->count = 0;

	// Init a OpenCV window and tell cvui to use it..
	namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	this->VideoLoaded = "None";
	this->CurrentSource = "None";
	this->DebugModeString = "Off";

	this->DebugMode = false;
	this->DebugModeChanged = true;

}

Gui::~Gui() {

}

bool Gui::onWork(void) {
	frame = Scalar(49, 52, 49);

	//FRAMES
	cvui::window(frame, 10, 10, 230, 145, "Video Source:");		//Video Source Frame
	cvui::window(frame, 10, 165, 230, 600, "Settings:");		//Settings Frame

	//Text
	cvui::printf(frame, 20, 35, 0.4, 0xdd97fb, "Current Source:");	//Video Source
	cvui::printf(frame, 20, 50, 0.4, 0xdd97fb, "%s", CurrentSource.c_str());	//Video Source
	cvui::printf(frame, 135, 282, 0.4, 0xdd97fb, "%s", DebugModeString.c_str());				//Debug Mode

	//Video Source Buttons
	if (cvui::button(frame, 20, 70, "Use Video")) {
		if (openFile()) {
			VideoLoaded = videoPath;
			CurrentSource = "Video loaded: " + videoName;
		}
		else {
			CurrentSource = "No Video Loaded";
		}
		//count++;
	}
	if (cvui::button(frame, 20, 105, "Use camera")) {
		CurrentSource = "Camera On";
		count++;
	}

	//Settings Buttons
	if (cvui::button(frame, 20, 200, "Select New Area")) {

		count++;
	}
	if (cvui::button(frame, 20, 235, "Start Tracking")) {

		count++;
	}
	if (cvui::checkbox(frame, 20, 280, "Debug Mode", &DebugMode)) {
		if (DebugModeChanged) {
			DebugMode = true;
			DebugModeString = "On";
			count++;
			DebugModeChanged = false;
		}
	}
	else {
		DebugMode = false;
		DebugModeString = "Off";
		DebugModeChanged = true;
	}

	//Settings Poperties
	if (cvui::checkbox(frame, 20, 300, "Kalman", &KalmanProp)) {

		LKProp = false;
		CFProp = false;
		ShiTProp = false;

		cvui::printf(frame, 20, 400, 0.4, 0xdd97fb, "Process Time Multiplier");
		cvui::trackbar(frame, 20, 415, 210, &kalman_ptm, (double)0, (double)2);

		cvui::printf(frame, 20, 470, 0.4, 0xdd97fb, "Process Covariance");
		cvui::trackbar(frame, 20, 485, 210, &kalman_pc, (double)0, (double)1);

		cvui::printf(frame, 20, 540, 0.4, 0xdd97fb, "Measurement Covariance");
		cvui::trackbar(frame, 20, 555, 210, &kalman_mc, (double)0, (double)1);

	}
	if (cvui::checkbox(frame, 20, 320, "Lucas-Kanade", &LKProp)) {
		KalmanProp = false;
		CFProp = false;
		ShiTProp = false;

		cvui::printf(frame, 20, 400, 0.4, 0xdd97fb, "Maximum Recursion");
		cvui::trackbar(frame, 20, 415, 210, &lk_mr, (double)0, (double)10);
	}
	if (cvui::checkbox(frame, 20, 340, "Color Filter", &CFProp)) {
		KalmanProp = false;
		LKProp = false;
		ShiTProp = false;

		if (cvui::checkbox(frame, 20, 400, "Color Filter On/Off", &CFPropOnOff)) {
			CFLRPropOnOff = false;
			cvui::printf(frame, 20, 460, 0.4, 0xdd97fb, "Lightness Threshold");
			cvui::trackbar(frame, 20, 475, 210, &colorFilter_LihtThr, (double)0, (double)150);

			cvui::printf(frame, 20, 530, 0.4, 0xdd97fb, "A Threshold");
			cvui::trackbar(frame, 20, 545, 210, &colorFilter_a, (double)0, (double)30);

			cvui::printf(frame, 20, 600, 0.4, 0xdd97fb, "B Threshold");
			cvui::trackbar(frame, 20, 615, 210, &colorFilter_b, (double)0, (double)30);
		}
		if (cvui::checkbox(frame, 20, 420, "Lightness Recalculation On/Off", &CFLRPropOnOff)) {
			CFPropOnOff = false;
			cvui::printf(frame, 20, 460, 0.4, 0xdd97fb, "Every X Frames");
			cvui::trackbar(frame, 20, 475, 210, &ligtRec_x, (double)0, (double)150);

			cvui::printf(frame, 20, 530, 0.4, 0xdd97fb, "Maximum Threshold Change");
			cvui::trackbar(frame, 20, 545, 210, &ligtRec_maxT, (double)0, (double)30);
		}
	}
	if (cvui::checkbox(frame, 20, 360, "Shi-Tomasi", &ShiTProp)) {
		KalmanProp = false;
		LKProp = false;
		CFProp = false;

		cvui::printf(frame, 20, 400, 0.4, 0xdd97fb, "Maximum Feature Quantity");
		cvui::trackbar(frame, 20, 415, 210, &shit_MaxFeat, (double)1, (double)1000);

		cvui::printf(frame, 20, 470, 0.4, 0xdd97fb, "Feature Quality Level");
		cvui::trackbar(frame, 20, 485, 210, &shit_FeatQual, (double)0, (double)1);

		cvui::printf(frame, 20, 540, 0.4, 0xdd97fb, "Minimum Feature Distance");
		cvui::trackbar(frame, 20, 555, 210, &shit_MinFeat, (double)0, (double)1);

		cvui::printf(frame, 20, 610, 0.4, 0xdd97fb, "Search Pixel Enlargement");
		cvui::trackbar(frame, 20, 625, 210, &shit_SPix, (double)0, (double)10);

		if (cvui::checkbox(frame, 20, 670, "Feature Recalculation On/Off", &ShiTPropOnOff)) {
			cvui::printf(frame, 20, 690, 0.4, 0xdd97fb, "Every X frames");
			cvui::trackbar(frame, 20, 705, 210, &shit_Rec, (double)1, (double)100);
		}
	}

	// Show how many times the button has been clicked.
	// Text at position (250, 90), sized 0.4, in red.
	cvui::printf(frame, 300, 90, 0.4, 0xdd97fb, "Tatometer! \"Se entiende\" count: %d", count);


	// Update cvui internal stuff
	cvui::update();

	// Show everything on the screen
	cv::imshow(WINDOW_NAME, frame);



	// Check if ESC key was pressed
	if (cv::waitKey(20) == 27) {
		return false;
	}
	else {
		return true;
	}

}

bool Gui::openFile(void) {
	const std::wstring title = L"Select a File";
	std::wstring filename(MAX_PATH, L'\0');

	OPENFILENAMEW ofn = { };
	ofn.lStructSize = sizeof(ofn);
	ofn.hwndOwner = NULL;
	ofn.lpstrFilter = L"Video (.mp4)\0*.mp4\0All\0*.*\0";
	ofn.lpstrFile = &filename[0];  // use the std::wstring buffer directly
	ofn.nMaxFile = MAX_PATH;
	ofn.lpstrTitle = title.c_str();
	ofn.Flags = OFN_DONTADDTORECENT | OFN_FILEMUSTEXIST;

	if (GetOpenFileNameW(&ofn)) {

		string s(filename.begin(), filename.end());		//Path completo

		string justName = s.substr(s.find_last_of('\\') + 1);
		justName = justName.substr(justName.find_last_of('\\') + 1, justName.size());		//Solo el nombre sin el formato
		justName = justName.substr(0, justName.find_first_of('\0') - 4);

		this->videoName = justName;
		this->videoPath = s;

		return true;
	}
	return false;
}