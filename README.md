# ROS-Nodes-and-Development
ROS development tools and Nodes 

## Python
Here you'll find a really simple framework for a GUI to do joint space and cartesian space control. 

## Nodes
### PCDataConversion
This reads in a PointCloud2 message from ROS, converts it to a PCL-happy type, orients the cloud for viewing, adds in some noise to mimick the output of the Google Project Tango and makes the point cloud more sparse again to mimick the Google Tango.

The point cloud it reads in is from a gazebo simulation using a google tango like sensor based loosely on the Kinect-openni gazebo sensor. 

### SLAMsimulation
This reads in the outputs from the PCDataConversion node and delays the output for the correct amount of time that the google tango takes to output each message. The output topics are the same topics the google tango's ROScore sends them to, so this is a full simulation of the google tango that takes out the hardware from being required. 

## Notes
Random notes to self, or install instructions, or Linux tips, as I found appropriate when starting to learn ROS and Linux. 
