
// (C) Steve Macenski - University of Illinois at Urbana Champaign
// BSD License 

// take in transformed point cloud data from Tango sim and pose locations from gazebo model_state
// and output them at the correct rate with the correct message types to mimick the google tango rates/types 

#include <ros/ros.h>
#include <iterator>
#include <stdio.h>
#include <vector>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <iostream>
#include <pcl/point_cloud.h>
#include <pcl/console/parse.h>
#include <pcl/common/transforms.h>
#include <std_msgs/String.h>
#include <sstream>
#include <sensor_msgs/PointCloud2.h> 
#include <pcl_ros/point_cloud.h>
#include <geometry_msgs/PoseStamped.h>
#include <gazebo_msgs/ModelStates.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Header.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/Quaternion.h>



ros::Publisher publish_pose;
ros::Publisher publish_pointClouds; 

void callback_cloud(const sensor_msgs::PointCloud2& input_cloud)
{
	
	ros::Rate loop_rate_cloud(5);
	loop_rate_cloud.sleep(); 	// makes the cloud publishing sleep for a publish rate of 5 hz
	
	//publish
	publish_pointClouds.publish(input_cloud);
}

void callback_pose(const gazebo_msgs::ModelStates& Model_State)
{
	ros::Rate loop_rate_pose(60);
	loop_rate_pose.sleep(); //makes the pose publishing sleep for a publish rate of 60 hz 
	
	geometry_msgs::PoseStamped jackal_pose;
		
	// grab the jackal's pose and orientation for the conversion
	jackal_pose.pose.position  = Model_State.pose[2].position; 
	jackal_pose.pose.orientation = Model_State.pose[2].orientation; 
	
	//grabs the current simulation time and throws to the header for stamped
	ros::Time time = ros::Time::now();
	jackal_pose.header.stamp = time;
	
	jackal_pose.header.seq++;
	
	//publisher
	publish_pose.publish(jackal_pose);
	
	
	
}
int main(int argc, char **argv)
{
	// node initalization
	ros::init(argc, argv, "tangoSim");
	ros::NodeHandle tangoSim;
	
	// sub/publish point clouds
	publish_pointClouds = tangoSim.advertise<sensor_msgs::PointCloud2>("/points", 1);
	ros::Subscriber sub_pointClouds = tangoSim.subscribe("/camera/depth/transformedPoints",1,callback_cloud);
	
	//sub/publish pose estimations 
	publish_pose = tangoSim.advertise<geometry_msgs::PoseStamped>("/android/orientation", 1);
	ros::Subscriber sub_pose = tangoSim.subscribe("/gazebo/model_states",1,callback_pose);
	
	// continue whilest running without error
	while(ros::ok()){
		ros::spinOnce();
	}
}
