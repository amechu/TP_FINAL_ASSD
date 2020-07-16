#pragma once
#include "../cvinclude.h"
#include "../Util/Util.h"
#include <vector>
using namespace std;
class ShiTomasi
{
public:
	vector<Point>& getFeatures();
	vector<Point>& recalculateFeatures();
private:
	vector<Point> features;
	vector<double> parameters;
};

