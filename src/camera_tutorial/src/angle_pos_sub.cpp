#include <ros/ros.h>
#include <math.h>
//#include <cmath>
#include <algorithm> //array ops such as copy
#include <array>
#include "image_transport_tutorial/tracking2Dmsg.h"
#include <visualization_msgs/Marker.h>
#include <geometry_msgs/Point.h>

class analyzerListener
{
	public:
		std::array<double, 3> top_cam_pos;
		std::array<double, 3> top_ray_dir;
		std::array<double, 3> bom_cam_pos;
		std::array<double, 3> bom_ray_dir;

		double L;
		double H;
		double D;
		double a;

		double top_cam_dist;
		double bom_cam_dist;

		double top_tantheta_x;
		double top_tantheta_y;
		double bom_tantheta;

		ros::Publisher pub;
		ros::Publisher pub2;
		visualization_msgs::Marker points;

  	analyzerListener(){

		L = 8.65 / 100.0; //cm-->m
		H = 6.48 / 100.0;
		D = 12.2 / 100.0;
		a = 12.18-5.2 / 100.0;

		top_cam_dist = L / 2.0 + D;
		bom_cam_dist = H / 2.0 + a + L/2.0 + D;

		top_tantheta_x = L/2.0 / top_cam_dist;
		top_tantheta_y = H/2.0 / top_cam_dist;

		bom_tantheta = L/2.0 / bom_cam_dist;//x y same for bottom camera
		//pub;
		 std::array<double, 3> top_cam_pos = {0, -top_cam_dist, 0};
		 this->top_cam_pos  = top_cam_pos;
		 print_vec(this->top_cam_pos);
		 std::array<double, 3> bom_cam_pos = {0, 0, -bom_cam_dist};
		 this->bom_cam_pos  = bom_cam_pos;

  	}
  void pub_location(){
  	std::array<double, 3> A = top_cam_pos;
  	std::array<double, 3> a = top_ray_dir;
  	std::array<double, 3> B = bom_cam_pos;
  	std::array<double, 3> b = bom_ray_dir;
  	std::array<double, 3> c = {B[0]-A[0], B[1]-A[1], B[2]-A[2]};
 //  	print_vec(A);
 //  	print_vec(a);
	// print_vec(B);
 //  	print_vec(b);
 //  	print_vec(c);
 //  	std::cout<<dot(a,b)<<std::endl; 
 //  	std::cout<<dot(b,c)<<std::endl; 
 //  	std::cout<<dot(a,c)<<std::endl; 
 //  	std::cout<<dot(b,b)<<std::endl; 
 //  	std::cout<<dot(a,a)*dot(b,b) - dot(a,b)*dot (a,b)<<std::endl; 


  	double D_coeff = (( -dot(a,b)*dot(b,c) + dot(a,c)*dot(b,b) )) / (( dot(a,a)*dot(b,b) - dot(a,b)*dot (a,b) ));
  	double E_coeff = (( dot(a,b)*dot(a,c)  - dot(b,c)*dot(a,a) )) / (( dot(a,a)*dot(b,b) - dot(a,b)*dot (a,b) ));
  	
  	double D_x = A[0] + a[0] * D_coeff;
  	double D_y = A[1] + a[1] * D_coeff;
  	double D_z = A[2] + a[2] * D_coeff;

  	double E_x = B[0] + b[0] * E_coeff;
  	double E_y = B[1] + b[1] * E_coeff;
  	double E_z = B[2] + b[2] * E_coeff;

  	//std::cout << "D =" <<" "<< D_x << " "<< D_y << " "<<D_z<<std::endl;
  	//std::cout << "E =" <<" "<< E_x << " "<< E_y << " "<<E_z<<std::endl;

	points.header.frame_id = "/my_frame";
	points.header.stamp = ros::Time::now();
	points.ns  = "pos";
	points.action = visualization_msgs::Marker::ADD;
	points.pose.orientation.w = 1.0;
	points.id = 0;
	points.type = visualization_msgs::Marker::POINTS;
	points.scale.x = 0.06; points.scale.y = 0.06;
	points.color.g = 1.0f; points.color.a = 1.0;
	geometry_msgs::Point p;
	if(std::isfinite(D_x) && std::isfinite(D_y) && std::isfinite(D_z) ){
	p.x = 100.* 0.5 * (D_x + E_x);
	p.y = 100.* 0.5 * (D_y + E_y);
	p.z = 100.* 0.5 * (D_z + E_z);
	}
	points.points.push_back(p);
	pub.publish(points);
	pub2.publish(p);

  }
  void print_vec(std::array<double, 3> c){
  	std::cout << "x = "<<c[0]<< "y = "<<c[1]<< "z = "<<c[2]<<std::endl;
  }
  double norm (std::array<double, 3> vec){
  	return std::sqrt(std::pow(vec[0],2)+std::pow(vec[1],2)+std::pow(vec[2],2));
  }
  double dot (std::array<double, 3> a, std::array<double, 3> b){
  	return a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
  }
  void top_cam_callback(const image_transport_tutorial::tracking2DmsgConstPtr& msg){
  	//top
	double px_L_half = msg->nx / 2.0; 
	double px_x      =  msg->x - px_L_half ;
	double tan_top_x_ang = top_tantheta_x * px_x / px_L_half;
	double px_H_half = msg->ny / 2.0; 
	double px_y      = px_H_half- msg->y;//reversed bacuse top in positive axis
	double tan_top_y_ang = top_tantheta_y * px_y / px_H_half;
	std::array<double, 3>  top_ray_dir = {tan_top_x_ang, 1, tan_top_y_ang};
	double norm_dir = norm(top_ray_dir);
	for (int i = 0; i < 3; i ++ ){
	this->top_ray_dir[i] = top_ray_dir[i]/ norm_dir ;
	}
	pub_location();
  }

  void bom_cam_callback(const image_transport_tutorial::tracking2DmsgConstPtr& msg){
  	//bom
   	double px_L_half = (msg->nx + msg -> ny) / 4.0; //average x and y so its more accurate 
	double px_x      =  msg->x - px_L_half ;
	double tan_bom_x_ang = bom_tantheta * px_x / px_L_half;
	double px_y      = px_L_half - msg->y;//same as top cam
	double tan_bom_y_ang = bom_tantheta * px_y / px_L_half;
	std::array<double, 3>  bom_ray_dir = {tan_bom_x_ang, tan_bom_y_ang, 1};
	double norm_dir = norm(bom_ray_dir);
	for (int i = 0; i < 3; i ++ ){
	this->bom_ray_dir[i] = bom_ray_dir[i]/ norm_dir ;
		// std::cout << i <<" "<<this->bom_ray_dir[i]<<" norm = "<<norm_dir<<std::endl;
	}
	pub_location();
  }
};



int main(int argc, char **argv)
{
  //arg input chec
  ros::init(argc, argv, "angle_pos_sub");
  ros::NodeHandle nh;
  analyzerListener ana_ls;//
  ros::Subscriber sub1 = nh.subscribe("camera1/cv_image_pos", 1,  &analyzerListener::top_cam_callback, &ana_ls);
  ros::Subscriber sub2 = nh.subscribe("camera2/cv_image_pos", 1,  &analyzerListener::bom_cam_callback, &ana_ls);
  //image_ls.pub = nh.advertise<geometry_msgs::Point>("camera"+cam_num+"/cv_image_pos", 1);
  ana_ls.pub = nh.advertise<visualization_msgs::Marker>("visualization_marker", 10);
  ana_ls.pub2 = nh.advertise<geometry_msgs::Point>("particle_pos", 10);

  ros::spin();
}

