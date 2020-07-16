//RECORDAR PONER EL ENVIRONMENT EN X64
#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME "MAGT Video Tracker"

using namespace cv;
using namespace std;

string FileBrowser();

/*int main(void)
{
	Mat frame = Mat(720, 1280, CV_8UC3);
	int count = 0;

	// Init a OpenCV window and tell cvui to use it.
	namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	int hueValue = 0;
	int satValue = 0;
	int lightValue = 0;

	string CurrentSource = "None";
	string DebugModeString = "Off";
	bool DebugMode = false;

	while (true) {
		// Fill the frame with a nice color
		frame = Scalar(49, 52, 49);

		//FRAMES
		cvui::window(frame, 10, 10, 210, 145, "Video Source:");		//Video Source Frame
		cvui::window(frame, 10, 165, 210, 470, "Settings:");		//Settings Frame

		//Text
		cvui::printf(frame, 20, 35, 0.4, 0xdd97fb, "Current Source: %s", CurrentSource.c_str());	//Video Source
		cvui::printf(frame, 135, 205, 0.4, 0xdd97fb, "%s", DebugModeString.c_str());				//Debug Mode
		
		//Video Source Buttons
		if (cvui::button(frame, 20, 50, "Load Video")) {
			CurrentSource =  "Video Loaded";
			count++;
		}
		if(cvui::button(frame, 20, 85, "Use camera")) {
			CurrentSource = "Camera On";
			count++;
		}
		if (cvui::button(frame, 20, 120, "Select Video")) {

			count++;
		}		

		//Settings Buttons
		if (cvui::button(frame, 20, 195, "Debug Mode")) {
			DebugMode = !DebugMode;
			if (DebugMode) {
				DebugModeString = "On";
			}
			else {
				DebugModeString = "Off";
			}
			
			count++;
		}
		if (cvui::button(frame, 20, 230, "Select New Area")) {

			count++;
		}
		if (cvui::button(frame, 20, 265, "Start Tracking")) {

			count++;
		}

		cvui::printf(frame, 20, 300, 0.4, 0xdd97fb, "HUE");
		cvui::trackbar(frame, 20, 315, 165, &hueValue, 0, 50);

		cvui::printf(frame, 20, 375, 0.4, 0xdd97fb, "Saturation");
		cvui::trackbar(frame, 20, 390, 165, &satValue, 0, 100);

		cvui::printf(frame, 20, 450, 0.4, 0xdd97fb, "Lightness");
		cvui::trackbar(frame, 20, 465, 165, &lightValue, 0, 100);

		// Show how many times the button has been clicked.
		// Text at position (250, 90), sized 0.4, in red.
		cvui::printf(frame, 250, 90, 0.4, 0xdd97fb, "Tatometer! \"Se entiende\" count: %d", count);

		

		// Update cvui internal stuff
		cvui::update();

		// Show everything on the screen
		cv::imshow(WINDOW_NAME, frame);

		// Check if ESC key was pressed
		if (cv::waitKey(20) == 27) {
			break;
		}
	}
	return 0;
}
*/


/*
string FileBrowser() {
	wxFileDialog openFileDialog(this, _("Open MIDI file"), "", "", "MIDI files (*.mid)|*.mid", wxFD_OPEN | wxFD_FILE_MUST_EXIST);  //Abro explorador de archivos
	bool addString = true;
	if (openFileDialog.ShowModal() == wxID_CANCEL) {			//Esto está por si se cierra el explorador sin elegir archivos
		return;
	}

	wxFileInputStream input_stream(openFileDialog.GetPath());	//Verifico que todo ande joya

	string pathSelected = openFileDialog.GetPath();				//Path completo

	string stringSelected = pathSelected.substr(pathSelected.find_last_of('\\') + 1);
	stringSelected = stringSelected.substr(stringSelected.find_last_of('\\') + 1, stringSelected.size() - 4);		//Solo el nombre sin el .wav

	if (!input_stream.IsOk()) {
		return NULL;
	}
	else {
		return pathSelected;
	}
}
*/