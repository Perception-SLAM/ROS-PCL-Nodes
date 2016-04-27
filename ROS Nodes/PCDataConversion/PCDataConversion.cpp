
// (C) Steve Macenski - University of Illinois at Urbana Champaign
// BSD License 

// convert PointCloud2 data from the incorrect frame to the correct one by means of rotation matrices 
// add in noise calculated from another script stddev=.0305 to mimic output of Google Tango
// take out some points to have density of that similar to the google tango output. 

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
#include <pcl/conversions.h>
#include <pcl/point_types.h>
#include <pcl/console/time.h>
#include <boost/random.hpp>
#include <boost/random/normal_distribution.hpp> 
#include <pcl/filters/voxel_grid.h>
#include <pcl/common/projection_matrix.h>
#include <gazebo_msgs/ModelStates.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Header.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/Quaternion.h>


// globals
ros::Publisher publish_transformation;
gazebo_msgs::ModelStates state_pose; 

void callback(const sensor_msgs::PointCloud2& input_cloud)
{
	
	// create pointer for source cloud to convert the input cloud to
	pcl::PointCloud<pcl::PointXYZ>::Ptr source_cloud (new pcl::PointCloud<pcl::PointXYZ> ());
	
	// convert input_cloud (PointCloud2) to PCL data type(PointXYZ), source_cloud
	pcl::fromROSMsg(input_cloud, *source_cloud);
		

	//rotation matrix
	Eigen::Matrix4f transformation = Eigen::Matrix4f::Identity();
	transformation(0,0) = 0;//x.x		Rotation		row,column
	transformation(0,1) = 0;//x.y
	transformation(0,2) = 1;//x.z
	transformation(1,0) = -1;//y.x
	transformation(1,1) = 0;//y.y
	transformation(1,2) = 0;//y.z
	transformation(2,0) = 0;//z.x
	transformation(2,1) = -1;//z.y
	transformation(2,2) = 0;//z.z
	
	transformation(0,3) = 0; //translation x
	transformation(1,3) = 0; //translation y
	transformation(2,3) = 0; //translation z
	
	//transformed_cloud pointer
	pcl::PointCloud<pcl::PointXYZ>::Ptr transformed_cloud_XYZ (new pcl::PointCloud<pcl::PointXYZ> ());
	// transformation
	pcl::transformPointCloud (*source_cloud, *transformed_cloud_XYZ, transformation);


	// add noise into the point cloud, cloud currently in pcl::PointCloud<pcl::PointXYZ>::Ptr format
    boost::mt19937 rng; rng.seed (static_cast<unsigned int> (time (0)));
    boost::normal_distribution<> nd (0, 0.0305); // mean, stddev
    boost::variate_generator<boost::mt19937&, boost::normal_distribution<> > var_nor (rng, nd);

    for (size_t point_i = 0; point_i < transformed_cloud_XYZ->points.size (); ++point_i)
    {
      transformed_cloud_XYZ->points[point_i].x += static_cast<float> (var_nor ());
      transformed_cloud_XYZ->points[point_i].y += static_cast<float> (var_nor ());
      transformed_cloud_XYZ->points[point_i].z += static_cast<float> (var_nor ());
    }
	
	// remove some points in the point cloud to reduce fidelity
	pcl::PointCloud<pcl::PointXYZ>::Ptr thinned_cloud (new pcl::PointCloud<pcl::PointXYZ> ());
	
	pcl::VoxelGrid<pcl::PointXYZ> sor;
	sor.setInputCloud (transformed_cloud_XYZ);
	sor.setLeafSize (0.045f, 0.045f, 0.045f);
	sor.filter (*thinned_cloud);
	
	// transforming thinned_cloud to a global frame by taking pose and offsetting in orientation/translation
	
	Eigen::Vector3d translation;  //translation offset
	translation[0] = state_pose.pose[2].position.x; //.x.y.z
	translation[1] = state_pose.pose[2].position.y; 
	translation[2] = state_pose.pose[2].position.z; 

	Eigen::Quaterniond quat;     // orientation offset
	quat.w() = state_pose.pose[2].orientation.w; //.w.x.y.z
	quat.x() = state_pose.pose[2].orientation.x; 
	quat.y() = state_pose.pose[2].orientation.y; 
	quat.z() = state_pose.pose[2].orientation.z;
	
							    // transform using offsets and PCL
	pcl::PointCloud<pcl::PointXYZ>::Ptr rotated_cloud (new pcl::PointCloud<pcl::PointXYZ> ());
	pcl::transformPointCloud(*thinned_cloud, *rotated_cloud, translation, quat);
	

	// storing a global point cloud 
	static pcl::PointCloud<pcl::PointXYZ> global_cloud;
	global_cloud += *rotated_cloud;

	// convert transformed cloud to PointCloud2 for ROS
	sensor_msgs::PointCloud2 transformed_cloud_2;
	pcl::toROSMsg(global_cloud, transformed_cloud_2); //*thinned_cloud
	
	// write the frame to be transformed with respect to and time to header
    transformed_cloud_2.header.stamp = ros::Time::now();
    transformed_cloud_2.header.frame_id = "front_laser";
	
	// publish results
	publish_transformation.publish(transformed_cloud_2);


}

void callback_2(const gazebo_msgs::ModelStates& Model_State)
{
	::state_pose = Model_State; 
}

int main(int argc, char **argv)
{

	ros::init(argc, argv, "PCDataConversion");
	ros::NodeHandle PCDataConversion;

	publish_transformation = PCDataConversion.advertise<sensor_msgs::PointCloud2>("/camera/depth/transformedPoints", 1000);
	ros::Subscriber sub = PCDataConversion.subscribe("/camera/depth/points",1000,callback);
	ros::Subscriber sub_pose = PCDataConversion.subscribe("/gazebo/model_states",1000,callback_2);
	
	while(ros::ok()){
		ros::spinOnce();
	}
}
