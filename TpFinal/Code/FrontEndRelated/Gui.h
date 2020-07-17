#pragma once

#include "cvui.h"
#include <opencv2/highgui/highgui_c.h>
#include <windows.h>

#define WINDOW_NAME "MAGT Video Tracker"

#define INITIAL_KALMAN_PTM	1.2
#define INITIAL_KALMAN_PC	0.006
#define INITIAL_KALMAN_MC	0.4

#define INITIAL_LK_MR		4.0

#define COLORFILTER_LIGHTTHR	70.0
#define COLORFILTER_A			20.0
#define COLORFILTER_B			20.0
#define LIGHTTHR_X				1.0
#define LIGHTTHR_MACT			1.0

#define SHIT_MAXFEAT			100.0
#define SHIT_FEATQUAL			0.001
#define SHIT_MINFEAT			0.01
#define SHIT_REC				20.0
#define SHIT_SPIX				4.0

using namespace cv;
using namespace std;

class Gui {
public:
	bool onWork(void);
	Gui();
	~Gui();

private:
	Mat frame;	// = Mat(1280, 1280, CV_8UC3);
	//Mat imok;	// = imread("imok.png");

	int count = 0;

	//Source names
	string VideoLoaded = "None";
	string CurrentSource = "None";
	string DebugModeString = "Off";
	string videoName;
	string videoPath;
	string videoExtension;

	//Bools and properties values
	bool DebugMode = false;
	bool DebugModeChanged = true;

	//Kalman Properties
	bool KalmanProp = false;

	double kalman_ptm = INITIAL_KALMAN_PTM;
	double kalman_pc = INITIAL_KALMAN_PC;
	double kalman_mc = INITIAL_KALMAN_MC;

	//LK Properties
	bool LKProp = false;
	
	double lk_mr = INITIAL_LK_MR;

	//CF Properties
	bool CFProp = false;
	bool CFPropOnOff = false;
	bool CFLRPropOnOff = false;

	bool ColorFilterActive = false;
	bool LightRecalcActive = false;

	double colorFilter_LihtThr = COLORFILTER_LIGHTTHR;
	double colorFilter_a = COLORFILTER_A;
	double colorFilter_b = COLORFILTER_B;
	double ligtRec_x = LIGHTTHR_X;
	double ligtRec_maxT = LIGHTTHR_MACT;

	//Shi-Tomasi Properties
	bool ShiTProp = false;
	bool ShiTPropOnOff = false;

	bool ShiTPropActive = false;

	double shit_MaxFeat = SHIT_MAXFEAT;
	double shit_FeatQual = SHIT_FEATQUAL;
	double shit_MinFeat = SHIT_MINFEAT;
	double shit_Rec = SHIT_REC;
	double shit_SPix = SHIT_SPIX;

	//Functions
	bool openFile(void);
	bool verifyInitialCond(void);
	void resetInitialCond(void);
};