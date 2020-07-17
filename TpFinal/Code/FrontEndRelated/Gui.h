#pragma once

#include "cvui.h"
#include <windows.h>

#define WINDOW_NAME "MAGT Video Tracker"

using namespace cv;
using namespace std;

class Gui {
public:
	bool onWork(void);
	Gui();
	~Gui();

private:
	Mat frame = Mat(1280, 1280, CV_8UC3);

	int count = 0;

	//Source names
	string VideoLoaded = "None";
	string CurrentSource = "None";
	string DebugModeString = "Off";
	string videoName = NULL;
	string videoPath = NULL;

	//Bools and properties values
	bool DebugMode = false;
	bool DebugModeChanged = true;

	//Kalman Properties
	bool KalmanProp = false;

	double kalman_ptm = 1.2;
	double kalman_pc = 0.006;
	double kalman_mc = 0.4;

	//LK Properties
	bool LKProp = false;
	
	double lk_mr = 4;

	//CF Properties
	bool CFProp = false;
	bool CFPropOnOff = false;
	bool CFLRPropOnOff = false;

	double colorFilter_LihtThr = 70.0;
	double colorFilter_a = 20.0;
	double colorFilter_b = 20.0;
	double ligtRec_x = 1.0;
	double ligtRec_maxT = 1.0;

	//Shi-Tomasi Properties
	bool ShiTProp = false;
	bool ShiTPropOnOff = false;

	double shit_MaxFeat = 100.0;
	double shit_FeatQual = 0.01;
	double shit_MinFeat = 0.01;
	double shit_Rec = 20.0;
	double shit_SPix = 4.0;

	//Functions
	bool openFile(void);
};