#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main()
{
    Mat src = imread("triangle.jpg");
    Mat gray, edges;
    cvtColor(src, gray, COLOR_BGR2GRAY);
    Canny(gray, edges, 50, 200, 3);
    vector<vector<Point>> contours;
    findContours(edges, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
    for (size_t i = 0; i < contours.size(); i++)
    {
        vector<Point> approx;
        approxPolyDP(contours[i], approx, arcLength(contours[i], true) * 0.02, true);
        if (approx.size() == 3)
        {
            double score = matchShapes(contours[i], approx, CONTOURS_MATCH_I1, 0);
            if (score < 0.1)
            {
                drawContours(src, contours, static_cast<int>(i), Scalar(0, 0, 255), 2);
            }
        }
    }
    imshow("result", src);
    waitKey(0);
    return 0;
}