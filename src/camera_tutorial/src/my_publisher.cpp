#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <sstream>
#include <camera_info_manager/camera_info_manager.h>
#include <boost/thread/mutex.hpp>
#include <string>
//#include <system>//for calling terminal changing 
int main(int argc, char** argv)
{ 
  
  //handle camera num
  if(argv[1] == NULL) return 1;
  std::istringstream video_sourceCmd(argv[1]);
  int video_source;
  // Check if it is indeed a number
  if(!(video_sourceCmd >> video_source)) return 1;
  std::string cam_num = argv[1]; 

  //start ros
  ros::init(argc, argv, "camera_publisher" + cam_num);
  ros::NodeHandle nh;
  
  //handle camera info
  std::string camera_info_url = "file:///home/cofphe/catkin_ws/camera_calib/cam"+cam_num+".yaml";
  camera_info_manager::CameraInfoManager cinfo(nh,"cam"+cam_num,camera_info_url);
  //publish info
  sensor_msgs::CameraInfoPtr info_msg (new sensor_msgs::CameraInfo(cinfo.getCameraInfo()));
  ros::Publisher pub2 = nh.advertise<sensor_msgs::CameraInfo>("camera"+cam_num+"/camera_info", 1);

  //publish image
  image_transport::ImageTransport it(nh);
  image_transport::Publisher pub = it.advertise("camera"+cam_num+"/image_raw", 1);
  //cv:capture
  u_int frame_rate_setting = 30;
  u_int width = 640;
  u_int height = 480;
  cv::VideoCapture cap(video_source+cv::CAP_V4L2);
  cap.set(cv::CAP_PROP_FRAME_WIDTH ,width);
  cap.set(cv::CAP_PROP_FRAME_HEIGHT,height);
  cap.set(cv::CAP_PROP_FPS,frame_rate_setting);
  //cap.set(cv::CAP_PROP_AUTO_EXPOSURE, 1);
  //cap.set(cv::CAP_PROP_EXPOSURE, 155);
  std::string v4lcmd = "v4l2-ctl -d /dev/video" + cam_num +" -c auto_exposure=1"; system(v4lcmd.c_str());
  v4lcmd =  "v4l2-ctl -d /dev/video" + cam_num + " -c exposure=150";              system(v4lcmd.c_str());


  if(!cap.isOpened()) return 1;
  cv::Mat frame;
  cv::Mat flippedframe;
  sensor_msgs::ImagePtr msg;

  //set node publishing speed = frame rate
  ros::Rate loop_rate(frame_rate_setting);

  while (nh.ok()) {
    cap >> frame;
    if(!frame.empty()){

      
      info_msg->height = height;
      info_msg->width  = width;
      flip(frame, flippedframe, -1);//flip both x and  y
      msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8",flippedframe).toImageMsg();
      pub.publish(msg);
      pub2.publish(info_msg);
      cv::waitKey(1);
    }
    ros::spinOnce();
    loop_rate.sleep();
  }
}

