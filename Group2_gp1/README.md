# Course: ENPM605 
### Section: 0101
### Professor: Zeid Kootbally
### Assignment: GP 1 (Scenario 3)
### Date: 04/17/2026


## Group Members:
Member 1: Nam Facchetti

UID: 118215693

Member 2: Yossaphat Kulvatunyou

UID: 112362550

## Contributions:
Nam: I worked on the camera_node.py, main_camera_node.py, fusion_node.py, main_fusion_node.py, config_publisher.py, and main_config_publisher.py files. I tried my best to make in-line comments within these files for understanding and reinforce that within the README (in the Design Decisions section). I formatted the package.xml and setup.py files to be properly structured/laid out. In terms of QoS configuration, I handled the configuration for the respective parts I worked on.

Yossaphat: Worked on the lidar_node, logger_node, safety_monitor_node, launch_file, and the entry_point script for the lidar, logger, and safety monitor. Assisted with README updates and handled QoS configuration for the nodes.

## Scenario Summary:
This project implements a multi-node ROS 2 perception pipeline that simulates a simplified autonomous vehicle sensor fusion system. The system integrates asynchronous data streams from a camera and a LiDAR sensor, combines them into a unified perception output, and monitors safety conditions based on the fused data.

The architecture consists of six nodes: a camera node publishing image frame identifiers at 10 Hz, a LiDAR node publishing distance measurements at 5 Hz, a fusion node that synchronizes and combines the latest sensor readings, a safety monitor that evaluates obstacle proximity, a configuration publisher that distributes system parameters using latched QoS, and an optional logger node for recording system output. Communication between nodes is implemented using ROS 2 publishers and subscribers with explicitly defined Quality of Service (QoS) profiles.

A key feature of the system is the use of heterogeneous QoS policies tailored to different data streams. Sensor topics use BEST_EFFORT reliability with a depth of 1 to prioritize low-latency delivery of the most recent data, while fused perception and alert topics use RELIABLE delivery to ensure critical information is not lost. The configuration topic uses TRANSIENT_LOCAL durability, allowing late-joining nodes to receive the most recent system configuration without requiring re-publication.

The fusion node demonstrates concurrent execution using a MultiThreadedExecutor and carefully selected callback groups. Sensor callbacks share a MutuallyExclusiveCallbackGroup to protect shared state (latest camera frame and LiDAR reading), while the publishing timer operates in a ReentrantCallbackGroup to maintain a consistent output rate independent of sensor callback timing.

The system also intentionally includes a QoS mismatch scenario, where a RELIABLE subscriber attempts to connect to a BEST_EFFORT publisher, resulting in no data delivery. This demonstrates the importance of QoS compatibility and provides an opportunity to diagnose communication issues using ROS 2 introspection tools.

Overall, this project illustrates how independent ROS 2 nodes can be composed into a coherent, real-time system that balances performance, reliability, and modularity while leveraging advanced middleware features such as QoS policies, executors, and launch configurations.

## Node Graph:
After following the build instructions below, with one terminal running the command:
- ros2 launch group2_gp1 system.launch.py enable_logger:=true

Use the ROS 2 graph tool to open up the node graph to inspect node and topic connections:
- rqt_graph

![alt text](https://private-user-images.githubusercontent.com/257414274/580248945-d2602a15-447c-48ea-983f-309131a5ae1b.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzY0ODE1MTYsIm5iZiI6MTc3NjQ4MTIxNiwicGF0aCI6Ii8yNTc0MTQyNzQvNTgwMjQ4OTQ1LWQyNjAyYTE1LTQ0N2MtNDhlYS05ODNmLTMwOTEzMWE1YWUxYi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNDE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDQxOFQwMzAwMTZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0wMWIxMDM1YTQ3NjllYTA0NzBiYWY1OGQ2MDE2N2U3MDM1YThjNGFiZmI3MmRkMzlhYzY1OGQwOTkyMTlhZWJlJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZwbmcifQ.vIOrjIWyKTFBIry4HlRGGiN6me6PiWLFPROiGRQY0zw)

## Design Decisions:
camera_node: The camera_node publishes simulated image frame IDs at 10 Hz on the /sensors/camera topic using the std_msgs/msg/String message type. A BEST_EFFORT, VOLATILE QoS profile with depth 1 was selected to reflect real-time perception system behavior, where only the most recent sensor data is relevant and older messages can be safely dropped. This minimizes latency and memory usage while ensuring high-frequency data flow. The node uses a timer-based callback to simulate a continuous camera stream, incrementing a frame counter and formatting it as a zero-padded string (for example, frame_0001).

The camera_node uses BEST_EFFORT reliability, which is intentionally incompatible with a RELIABLE subscriber used elsewhere in the system to demonstrate QoS mismatch behavior. This mismatch results in no data delivery, which can be verified using: ros2 topic info /sensors/camera -v

lidar_node: The node uses BEST_EFFORT, VOLATILE QoS profile with depth 1 which was select for the same reason as the camera node. Readings are dropped if the fusion node callback is slow.

fusion_node: MutuallyExclusiveCallbackGroup is used for the camera and LiDAR subscription callbacks to prevent race conditions when updating shared state (_latest_frame, _latest_distance) under a MultiThreadedExecutor. A ReentrantCallbackGroup is used for the fusion publishing timer so it can execute independently of sensor callbacks and maintain a consistent output rate.

Because both sensor topics use a QoS depth of 1, only the most recent message is stored in the queue. If the fusion node processes messages slower than the sensor publishing rate, intermediate messages are dropped. This design prioritizes low latency and ensures that only the most up-to-date sensor data is used for fusion, which is appropriate for real-time perception systems.

The /system/config topic uses TRANSIENT_LOCAL durability so that late-joining nodes (including the fusion node) can immediately receive the latest configuration without requiring re-publication. Although the configuration includes a "fusion_rate" parameter, the fusion node currently operates at a fixed rate defined internally by its timer (5 Hz), and does not dynamically update this rate at runtime.

safety_monitor: It uses RELIABLE, VOLATILE QoS with depth 10 to make sure no alerts are missed. A MutuallyExclusiveCallbackGroup is share between fuse subscriber and alert publisher so there will be no race condition(each take turn). The alert_threshold is a ros parameter which can be overide at launch using argument. It also subscribe to /system/config with TRANSIENT_LOCAL to receive msg even if it start after config publisher. Intentional QoS mismatch is show by subsricing to /sensors/camera with RELIABLE reliability while publisher use BEST_EFFORT, which cause data to not be delievered.

logger: Uses RELIABLE,VOLATILE QoS with depth 10 as well. So no message is lost and the message won't be stored for late joining subscriber. The node is launched when enable_logger is true by the launch file.

config_publisher: TRANSIENT_LOCAL ensures that late-joining subscribers (like fusion_node and safety_monitor) will still receive the last published configuration message. This behavior was verified using: 
- ros2 topic echo /system/config --once 
A late-joining subscriber immediately receives the last published configuration message, demonstrating TRANSIENT_LOCAL durability. This mimics latched behavior. Additionally, A short delay ensures that subscribers have time to connect before publishing. Without this, some nodes might miss the message even with TRANSIENT_LOCAL.

The configuration is published using a one-shot timer with a short delay (0.5 seconds). This ensures that the publisher is fully initialized Subscribers have time to connect and after publishing, the timer is canceled to prevent repeated messages.

A depth of 1 is used because only the most recent configuration is relevant. Older configurations are not needed and should not be buffered.

## Build/Run Instructions:

### Prerequisites
Ensure that ROS 2 (Humble or later) is installed and sourced on your system.
- source /opt/ros/humble/setup.bash

### Workspace Setup
Navigate to your ROS 2 workspace and place the package in the src/ directory:
- cd ~/enpm605_ws/src

Your package structure should look like:
- group2_gp1/

### Build the Package
Return to the workspace root and build the package:
- cd ~/enpm605_ws
- colcon build --packages-select group2_gp1

### Source the Workspace
After building, source the workspace:
- source install/setup.bash

### Run the System (Default Configuration)
Launch the full sensor fusion system:
- ros2 launch group2_gp1 system.launch.py

### Run with Logger Enabled
Enable the optional logger node using the launch argument:
- ros2 launch group2_gp1 system.launch.py enable_logger:=true

### Override Alert Threshold
Change the obstacle detection threshold (in meters):
- ros2 launch group2_gp1 system.launch.py alert_threshold:=5.0

### Verify System Operation
List all active topics and their message types:
- ros2 topic list -t

Monitor fused perception output:
- ros2 topic echo /perception/fused

Monitor safety alerts:
- ros2 topic echo /perception/alerts

Check camera publishing rate (should be about 10 Hz):
- ros2 topic hz /sensors/camera

Inspect QoS settings and detect mismatches:
- ros2 topic info /sensors/camera -v

### Test TRANSIENT_LOCAL Behavior
Verify that late-joining subscribers receive the configuration message:
- ros2 topic echo /system/config --once
This should immediately return the last published configuration.

### Visualize Node Graph
Use the ROS 2 graph tool to inspect node and topic connections:
- rqt_graph

## Known Issues:
To our knowledge at this moment, there are currently no none errors/issues.

One limitation is that fused messages are parsed using string operations rather than structured message types, which may be less robust in larger systems.