#pragma once
#include "../cvinclude.h"
#include "../Util/Util.h"

class KalmanFilter
{
public:
	KalmanFilter();
	void predict();
	void correct(Point measurement);
private:
	double statePost[4][1];
	double stateCovMat[4][4];
	double transMat[4][4];

	double measMat[2][4];
	double measCovMat[2][2];


};

