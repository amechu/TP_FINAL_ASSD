#include "lucasKandaleOld.h"
#include "../Tracker/ShiTomasi.h"
#include "../Tracker/OpticalFlow.h"

//using namespace cv;
//using namespace std;
//
//
//static void help()
//{
//    // print a welcome message, and the OpenCV version
//    cout << "\nThis is a demo of Lukas-Kanade optical flow lkdemo(),\n"
//        "Using OpenCV version " << CV_VERSION << endl;
//    cout << "\nIt uses camera by default, but you can provide a path to video as an argument.\n";
//    cout << "\nHot keys: \n"
//        "\tESC - quit the program\n"
//        "\tr - auto-initialize tracking\n"
//        "\tc - delete all the points\n"
//        "\tn - switch the \"night\" mode on/off\n"
//        "To add/remove a feature point click it\n" << endl;
//}
//
//Point2f point;
//bool addRemovePt = false;
//
//static void onMouse(int event, int x, int y, int /*flags*/, void* /*param*/)
//{
//    if (event == EVENT_LBUTTONDOWN)
//    {
//        point = Point2f((float)x, (float)y);
//        addRemovePt = true;
//    }
//}
//
////int lucasKandale(int argc, char** argv)
//int lucasKandale(void)
//{
//    VideoCapture cap(CAP_DSHOW);
//    TermCriteria termcrit(TermCriteria::COUNT | TermCriteria::EPS, 20, 0.03);
//    Size subPixWinSize(10, 10), winSize(31, 31);
//
//
//    //
//    double fps = cap.get(CAP_PROP_FPS);
//    Size size(
//        (int)cap.get(CAP_PROP_FRAME_WIDTH), (int)cap.get(CAP_PROP_FRAME_HEIGHT)
//    );
//
//    cv::VideoWriter writer;
//    writer.open("Test", writer.fourcc('M', 'J', 'P', 'G'), fps, size);
//
//    const int MAX_COUNT = 500;
//    bool needToInit = false;
//    bool nightMode = false;
//
//    help();
//    //cv::CommandLineParser parser(argc, argv, "{@input|0|}");
//    //string input = parser.get<string>("@input");
//
//    //if (input.size() == 1 && isdigit(input[0]))
//    //    cap.open(input[0] - '0');
//    //else
//    //    cap.open(input);
//    if (!cap.isOpened())
//    {
//        cout << "Could not initialize capturing...\n";
//        return 0;
//    }
//
//    namedWindow("LK Demo", 1);
//    setMouseCallback("LK Demo", onMouse, 0);
//
//    Mat gray, prevGray, image, frame;
//    vector<Point2f> points[2];
//
//    for (;;)
//    {
//        cap >> frame;
//        if (frame.empty())
//            break;
//
//        frame.copyTo(image);
//        cvtColor(image, gray, COLOR_BGR2GRAY);
//
//        if (nightMode)
//            image = Scalar::all(0);
//
//        if (needToInit)
//        {
//            // automatic initialization
//            goodFeaturesToTrack(gray, points[1], MAX_COUNT, 0.01, 10, Mat(), 3, 3, 0, 0.04);
//            cornerSubPix(gray, points[1], subPixWinSize, Size(-1, -1), termcrit);
//            addRemovePt = false;
//        }
//        else if (!points[0].empty())
//        {
//            vector<uchar> status;
//            vector<float> err;
//            if (prevGray.empty())
//                gray.copyTo(prevGray);
//            calcOpticalFlowPyrLK(prevGray, gray, points[0], points[1], status, err, winSize,
//                3, termcrit, 0, 0.001);
//            size_t i, k;
//            for (i = k = 0; i < points[1].size(); i++)
//            {
//                if (addRemovePt)
//                {
//                    if (norm(point - points[1][i]) <= 5)
//                    {
//                        addRemovePt = false;
//                        continue;
//                    }
//                }
//
//                if (!status[i])
//                    continue;
//
//                points[1][k++] = points[1][i];
//                circle(image, points[1][i], 3, Scalar(0, 255, 0), -1, 8);
//            }
//            points[1].resize(k);
//        }
//
//        if (addRemovePt && points[1].size() < (size_t)MAX_COUNT)
//        {
//            vector<Point2f> tmp;
//            tmp.push_back(point);
//            cornerSubPix(gray, tmp, winSize, Size(-1, -1), termcrit);
//            points[1].push_back(tmp[0]);
//            addRemovePt = false;
//        }
//
//        needToInit = false;
//        imshow("LK Demo", image);
//
//        char c = (char)waitKey(10);
//        if (c == 27)
//            break;
//        switch (c)
//        {
//        case 'r':
//            needToInit = true;
//            break;
//        case 'c':
//            points[0].clear();
//            points[1].clear();
//            break;
//        case 'n':
//            nightMode = !nightMode;
//            break;
//        }
//
//        std::swap(points[1], points[0]);
//        cv::swap(prevGray, gray);
//
//        //writer << image;
//    }
//    cap.release();
//    //writer.release();
//    destroyAllWindows();
//
//    return 0;
//}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

using namespace cv;
using namespace std;


static void help()
{
    // print a welcome message, and the OpenCV version
    cout << "\nThis is a demo of Lukas-Kanade optical flow lkdemo(),\n"
        "Using OpenCV version " << CV_VERSION << endl;
    cout << "\nIt uses camera by default, but you can provide a path to video as an argument.\n";
    cout << "\nHot keys: \n"
        "\tESC - quit the program\n"
        "\tr - auto-initialize tracking\n"
        "\tc - delete all the points\n"
        "\tn - switch the \"night\" mode on/off\n"
        "To add/remove a feature point click it\n" << endl;
}

Point2f point;
bool addRemovePt = false;

static void onMouse(int event, int x, int y, int /*flags*/, void* /*param*/)
{
    if (event == EVENT_LBUTTONDOWN)
    {
        point = Point2f((float)x, (float)y);
        addRemovePt = true;
    }
}

//int lucasKandale(int argc, char** argv)
int lucasKandale(void)
{
    OpticalFlow lk;
    ShiTomasi st;

    VideoCapture cap(CAP_DSHOW);
    TermCriteria termcrit = lk.getCriteria();
    Size subPixWinSize(10, 10);
    Size winSize = lk.getSize();


    //
    double fps = cap.get(CAP_PROP_FPS);
    Size size(
        (int)cap.get(CAP_PROP_FRAME_WIDTH), (int)cap.get(CAP_PROP_FRAME_HEIGHT)
    );

    cv::VideoWriter writer;
    writer.open("Test", writer.fourcc('M', 'J', 'P', 'G'), fps, size);

    const int MAX_COUNT = 500;
    bool needToInit = false;
    bool nightMode = false;

    help();
    if (!cap.isOpened())
    {
        cout << "Could not initialize capturing...\n";
        return 0;
    }

    namedWindow("LK Demo", 1);
    setMouseCallback("LK Demo", onMouse, 0);

    Mat gray, prevGray, image, frame;
    array<vector<cv::Point2f>, 2> points = st.getFeatures();

    for (;;)
    {
        cap >> frame;
        if (frame.empty())
            break;

        frame.copyTo(image);
        cvtColor(image, gray, COLOR_BGR2GRAY);

        if (nightMode)
            image = Scalar::all(0);

        if (needToInit)
        {

            points = st.recalculateFeatures(gray);
            //goodFeaturesToTrack(gray, points[1], MAX_COUNT, 0.01, 10, Mat(), 3, 3, 0, 0.04);
            cornerSubPix(gray, points[1], subPixWinSize, Size(-1, -1), termcrit);
            addRemovePt = false;
        }
        else if (!points[0].empty())
        {
            vector<uchar> status = lk.getStatus();
            vector<float> err = lk.getError();
            if (prevGray.empty())
                gray.copyTo(prevGray);
            lk.updateFeatures(prevGray, gray, points, status, err, winSize, termcrit);
            //calcOpticalFlowPyrLK(prevGray, gray, points[0], points[1], status,err, winSize,  3, termcrit, 0, 0.001);

            size_t i, k;
            for (i = k = 0; i < points[1].size(); i++)
            {
                if (addRemovePt)
                {
                    if (norm(point - points[1][i]) <= 5)
                    {
                        addRemovePt = false;
                        continue;
                    }
                }

                if (!status[i])
                    continue;

                points[1][k++] = points[1][i];
                circle(image, points[1][i], 3, Scalar(0, 255, 0), -1, 8);
            }
            points[1].resize(k);
        }

        if (addRemovePt && points[1].size() < (size_t)MAX_COUNT)
        {
            vector<Point2f> tmp;
            tmp.push_back(point);
            cornerSubPix(gray, tmp, winSize, Size(-1, -1), termcrit);
            points[1].push_back(tmp[0]);
            addRemovePt = false;
        }

        needToInit = false;
        imshow("LK Demo", image);

        char c = (char)waitKey(10);
        if (c == 27)
            break;
        switch (c)
        {
        case 'r':
            needToInit = true;
            break;
        case 'c':
            points[0].clear();
            points[1].clear();
            break;
        case 'n':
            nightMode = !nightMode;
            break;
        }

        std::swap(points[1], points[0]);
        cv::swap(prevGray, gray);

        //writer << image;
    }
    cap.release();
    //writer.release();
    destroyAllWindows();

    return 0;
}