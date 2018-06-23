#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>
// selectROI is part of tracking API
#include <opencv2/tracking.hpp>
#include "geometry_msgs/Point.h"
#include "image_transport_tutorial/tracking2Dmsg.h"





class imageListener
{
public:

  int iLowH;
  int iHighH;
  int iLowS;
  int iHighS;
  int iLowV;
  int iHighV;
  cv::Rect2d reigion;
  bool reigion_selected;
  int iLastX;
  int iLastY;
  cv::Mat imgLines;
  std::string cam_num;
  image_transport_tutorial::tracking2Dmsg cv_pt;
  ros::Publisher pub;
  imageListener(){
      iLowH = 0;
      iHighH= 255;
      iLowS = 0;      
      iHighS= 255;
      iLowV = 0;      
      iHighV= 50;
      reigion_selected = false;
      iLastX = -1;
      iLastY = -1;
      cv_pt.x = 0.0;
      cv_pt.y = 0.0;


  }
  void imageCallback(const sensor_msgs::ImageConstPtr& msg)
  {
    try
    { 
      //get msg
      cv::Mat imgOriginal = cv_bridge::toCvShare(msg, "bgr8")->image;
      
      //select region if not selected
      while (!reigion_selected) {
        //add whatevery you want to draw for reference in the section below
        //reigion = cv::selectROI("original",imgOriginal,0,0);
        if (cam_num == "1") reigion = cv::Rect( cv::Point(135,133), cv::Point(572,458) );
        else reigion = cv::Rect( cv::Point(187,97), cv::Point(492,400) );
        cv::Mat crop_size_ref = imgOriginal(reigion);
        imgLines = cv::Mat::zeros( reigion.height, reigion.width, CV_8UC3 );
        cv_pt.ny = reigion.height;
        cv_pt.nx = reigion.width;//x is width
        cv::circle(imgLines,  cv::Point(imgLines.cols/2,imgLines.rows/2), 5, cv::Scalar(0,255,0), 3);
        reigion_selected = true;
        //cv::destroyWindow("original");
      }

      //crop image 
      cv::Mat imgHSV;
      cv::Mat imgThresholded;
      cv::Mat imCrop = imgOriginal(reigion);
      //filter color
      cv::cvtColor(imCrop, imgHSV, cv::COLOR_BGR2HSV); //Convert the captured frame from BGR to HSV
      cv::inRange(imgHSV, cv::Scalar(iLowH, iLowS, iLowV), cv::Scalar(iHighH, iHighS, iHighV), imgThresholded); 
      cv::erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(5, 5)) );
      cv::dilate( imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(5, 5)) ); 
      cv::dilate( imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(5, 5)) ); 
      cv::erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(5, 5)) );
      
      //get moment & center
      cv::Moments oMoments = cv::moments(imgThresholded);
      double dM01 = oMoments.m01;
      double dM10 = oMoments.m10;
      double dArea = oMoments.m00;
      if (dArea > 100)
      {
        //calculate the position of the ball
        int posX = dM10 / dArea;
        int posY = dM01 / dArea;        
       // ROS_INFO("ROI pos X = %d Y= %d \n", posX, posY);
        if (iLastX >= 0 && iLastY >= 0 && posX >= 0 && posY >= 0)
        {
         //Draw a red line from the previous point to the current point
          cv::line(imgLines, cv::Point(posX, posY), cv::Point(iLastX, iLastY), cv::Scalar(0,0,255), 2);
          cv_pt.x = posX; cv_pt.y = posY;
          pub.publish(cv_pt);

        }
        iLastX = posX;
        iLastY = posY;

      }


      //cv::imshow("original", imgOriginal);
      cv::imshow("binary", imgThresholded);
      cv::imshow("cropped", imCrop+imgLines);

      cv::waitKey(10);
  } catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("Could not convert from '%s' to 'bgr8'.", msg->encoding.c_str());
    }
  }
};



int main(int argc, char **argv)
{
  //arg input check
  if(argv[1] == NULL) return 1;
  std::istringstream video_sourceCmd(argv[1]);
  int video_source;
  // Check if it is indeed a number
  if(!(video_sourceCmd >> video_source)) return 1;
  


  ros::init(argc, argv, "image_listener");
  ros::NodeHandle nh;
  imageListener image_ls;
  image_ls.cam_num = argv[1]; 
  cv::namedWindow("Control"); //create a window called "Control"


 //Create trackbars in "Control" window
  cvCreateTrackbar("LowH", "Control", &image_ls.iLowH, 179); //Hue (0 - 179)
  cvCreateTrackbar("HighH", "Control", &image_ls.iHighH, 179);
  cvCreateTrackbar("LowS", "Control", &image_ls.iLowS, 255); //Saturation (0 - 255)
  cvCreateTrackbar("HighS", "Control", &image_ls.iHighS, 255);
  cvCreateTrackbar("LowV", "Control", &image_ls.iLowV, 255); //Value (0 - 255)
  cvCreateTrackbar("HighV", "Control", &image_ls.iHighV, 255);
  
  
  cv::namedWindow("binary");
  //cv::namedWindow("original");
  cv::namedWindow("cropped");
  cv::startWindowThread();
  image_transport::ImageTransport it(nh);
  image_transport::Subscriber sub = it.subscribe("camera"+image_ls.cam_num+"/image_raw", 1, &imageListener::imageCallback, &image_ls);
  image_ls.pub = nh.advertise<image_transport_tutorial::tracking2Dmsg>("camera"+image_ls.cam_num+"/cv_image_pos", 1);
  ros::spin();
  //cv::destroyWindow("original");
  cv::destroyWindow("binary");
  cv::destroyWindow("cropped");
}
